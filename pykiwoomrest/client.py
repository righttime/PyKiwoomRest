"""키움 REST API 클라이언트 - 토큰 관리, 공통 HTTP 요청"""

from __future__ import annotations

import asyncio
import logging
import time
from typing import Any

import httpx

from .config import KiwoomConfig
from .exceptions import KiwoomAPIError

logger = logging.getLogger("pykiwoomrest")


class KiwoomClient:
    """키움 REST API 클라이언트

    Usage:
        config = KiwoomConfig.from_env()
        client = KiwoomClient(config)
        await client.init()  # 토큰 발급

        # 시세 조회
        data = await client.get("/api/dostk/stkinfo", tr_id="ka10001", stk_cd="005930")

        await client.close()
    """

    def __init__(self, config: KiwoomConfig) -> None:
        self.config = config
        self._token: str = ""
        self._token_expires: float = 0.0
        self._http: httpx.AsyncClient | None = None

    async def init(self) -> None:
        """HTTP 클라이언트 초기화 + 토큰 발급"""
        self._http = httpx.AsyncClient(
            base_url=self.config.base_url,
            timeout=30.0,
        )
        await self._issue_token()

    async def close(self) -> None:
        """리소스 정리"""
        if self._http:
            await self._http.aclose()
            self._http = None

    async def __aenter__(self) -> KiwoomClient:
        await self.init()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    @property
    def token(self) -> str:
        return self._token

    # ── 토큰 관리 ──────────────────────────────────

    async def _issue_token(self) -> str:
        """OAuth2 토큰 발급 (유효 1일)"""
        assert self._http is not None

        resp = await self._http.post(
            "/oauth2/token",
            json={
                "grant_type": "client_credentials",
                "appkey": self.config.api_key,
                "secretkey": self.config.secret_key,
            },
        )
        resp.raise_for_status()
        body = resp.json()

        self._token = body["token"]
        self._token_expires = time.time() + 86_400  # 24시간
        logger.info("토큰 발급 성공 (만료: 24h 후)")
        return self._token

    async def _ensure_token(self) -> None:
        """토큰 만료 시 재발급"""
        if time.time() >= self._token_expires - 300:  # 5분 여유
            await self._issue_token()

    # ── Rate Limiting ─────────────────────────────

    _last_request_time: float = 0.0
    _min_interval: float = 0.05  # 50ms = 20 req/sec

    async def _rate_limit(self) -> None:
        """초당 20회 제한"""
        now = time.time()
        elapsed = now - self._last_request_time
        if elapsed < self._min_interval:
            await asyncio.sleep(self._min_interval - elapsed)
        self._last_request_time = time.time()

    # ── Response Handling ─────────────────────────

    @staticmethod
    def _handle_response(resp: httpx.Response, headers: dict) -> dict[str, Any]:
        """응답 처리 + 연속조회 헤더 보존"""
        body = resp.json()

        # 에러 체크
        return_code = str(body.get("return_code", "0"))
        if return_code != "0":
            raise KiwoomAPIError(
                return_code=return_code,
                return_msg=body.get("return_msg", "Unknown error"),
                response=body,
            )

        # 연속조회 정보 보존
        cont_yn = resp.headers.get("cont-yn")
        next_key = resp.headers.get("next-key")
        if cont_yn:
            body["_cont_yn"] = cont_yn
            body["_next_key"] = next_key

        return body

    # ── Pagination ────────────────────────────────

    async def request_all(
        self,
        endpoint: str,
        tr_id: str,
        data_key: str | None = None,
        **params: Any,
    ) -> dict[str, Any]:
        """연속조회 자동 처리 (모든 페이지 조회)"""
        result: dict[str, Any] = {}
        all_items: list[dict] = []
        cont_yn: str | None = None
        next_key: str | None = None

        while True:
            hdrs = self._auth_headers()
            hdrs["api_id"] = tr_id
            if cont_yn:
                hdrs["cont-yn"] = cont_yn
            if next_key:
                hdrs["next-key"] = next_key

            await self._rate_limit()
            assert self._http is not None
            resp = await self._http.post(endpoint, headers=hdrs, json=params)
            body = self._handle_response(resp, hdrs)

            # 데이터 누적
            if data_key and data_key in body:
                items = body[data_key]
                if isinstance(items, list):
                    all_items.extend(items)
                else:
                    if not result:
                        result = body
                    break
            else:
                result.update(body)

            cont_yn = body.pop("_cont_yn", None)
            next_key = body.pop("_next_key", None)
            if not cont_yn:
                break

        if data_key and all_items:
            result[data_key] = all_items

        return result

    async def revoke_token(self) -> None:
        """토큰 폐기"""
        assert self._http is not None
        resp = await self._http.post(
            "/oauth2/revoke",
            data={"token": self._token},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        resp.raise_for_status()
        self._token = ""
        self._token_expires = 0.0
        logger.info("토큰 폐기 완료")

    # ── HTTP 요청 ──────────────────────────────────

    def _auth_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json;charset=utf-8",
        }

    async def get(
        self,
        endpoint: str,
        *,
        tr_id: str | None = None,
        **params: Any,
    ) -> dict[str, Any]:
        """조회 요청 (키움 REST API는 전부 POST 기반)"""
        await self._ensure_token()
        assert self._http is not None

        headers = self._auth_headers()
        if tr_id:
            headers["api-id"] = tr_id

        await self._rate_limit()
        resp = await self._http.post(endpoint, headers=headers, json=params)
        return self._handle_response(resp, headers)

    async def post(
        self,
        endpoint: str,
        *,
        tr_id: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """주문/갱신 요청"""
        await self._ensure_token()
        assert self._http is not None

        headers = self._auth_headers()
        if tr_id:
            headers["api-id"] = tr_id

        await self._rate_limit()
        resp = await self._http.post(endpoint, headers=headers, json=data or {})
        return self._handle_response(resp, headers)
