"""키움 REST API 클라이언트 - 토큰 관리, 공통 HTTP 요청"""

from __future__ import annotations

import asyncio
import logging
import time
from typing import Any

import httpx

from .config import KiwoomConfig

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
            headers={"api-id": "au10001"},
        )
        resp.raise_for_status()
        body = resp.json()

        # 키움 API 응답 구조: return_code=0이면 성공
        if body.get("return_code") != 0:
            msg = body.get("return_msg", "Unknown error")
            raise RuntimeError(f"토큰 발급 실패: [{body.get('return_code')}:{msg}]")

        self._token = body.get("token", "")
        self._token_expires = time.time() + 86_400  # 24시간
        logger.info("토큰 발급 성공 (만료: 24h 후)")
        return self._token

    async def _ensure_token(self) -> None:
        """토큰 만료 시 재발급"""
        if time.time() >= self._token_expires - 300:  # 5분 여유
            await self._issue_token()

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
            "Content-Type": "application/json;charset=UTF-8",
        }

    async def get(
        self,
        endpoint: str,
        *,
        tr_id: str | None = None,
        **params: Any,
    ) -> dict[str, Any]:
        """GET 요청 (시세/조회용)"""
        await self._ensure_token()
        assert self._http is not None

        headers = self._auth_headers()
        if tr_id:
            headers["api-id"] = tr_id

        resp = await self._http.get(endpoint, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()

    async def post(
        self,
        endpoint: str,
        *,
        tr_id: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """POST 요청 (주문용)"""
        await self._ensure_token()
        assert self._http is not None

        headers = self._auth_headers()
        if tr_id:
            headers["api-id"] = tr_id

        resp = await self._http.post(endpoint, headers=headers, json=data or {})
        resp.raise_for_status()
        return resp.json()


    async def post_list(
        self,
        endpoint: str,
        *,
        tr_id: str | None = None,
        data: dict[str, Any] | None = None,
        list_key: str = "list",
    ) -> dict[str, Any]:
        """POST 요청 (리스트 조회용) - cont-yn/next-key 헤더 자동 처리
        
        여러 페이지가 있으면 자동으로 모두 합쳐서 반환.
        응답 구조: {list_key: [...], cont_yn, next_key}
        """
        await self._ensure_token()
        assert self._http is not None

        all_items = []
        cont_yn = "N"
        next_key = ""

        while True:
            headers = {
                "Content-Type": "application/json;charset=UTF-8",
                "authorization": f"Bearer {self._token}",
                "cont-yn": cont_yn,
                "next-key": next_key,
            }
            if tr_id:
                headers["api-id"] = tr_id

            resp = await self._http.post(endpoint, headers=headers, json=data or {})
            resp.raise_for_status()
            body = resp.json()


            page_items = body.get(list_key, [])
            all_items.extend(page_items)

            cont_yn = body.get("cont_yn", "N")
            next_key = body.get("next_key", "") or ""
            if cont_yn != "Y" or not next_key:
                break

            # Rate limit safety
            await asyncio.sleep(0.1)


        return {list_key: all_items}
