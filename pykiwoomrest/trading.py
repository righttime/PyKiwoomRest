"""매수/매도 주문, 계좌 조회 (kt0xxxx, kt1xxxx TR)"""

from __future__ import annotations

import logging
from typing import Any

from .client import KiwoomClient

logger = logging.getLogger("pykiwoomrest.trading")


class TradingAPI:
    """매매 & 계좌 API"""

    def __init__(self, client: KiwoomClient, account_no: str | None = None) -> None:
        self._client = client
        self._account_no = account_no or client.config.account_no

    def _acct_params(self, **extra: Any) -> dict[str, Any]:
        params: dict[str, Any] = {"acct_no": self._account_no}
        params.update(extra)
        return params

    # ── 계좌 조회 ──────────────────────────────────

    async def deposit(self) -> dict[str, Any]:
        """kt00001 - 예수금상세현황"""
        return await self._client.get(
            "/api/dostk/acnt", tr_id="kt00001", **self._acct_params()
        )

    async def account_summary(self) -> dict[str, Any]:
        """kt00004 - 계좌평가현황 (총 평가금액, 수익률)"""
        return await self._client.get(
            "/api/dostk/acnt", tr_id="kt00004", **self._acct_params()
        )

    async def holdings(self) -> dict[str, Any]:
        """kt00005 - 체결잔고 (보유 종목별 잔고)"""
        return await self._client.get(
            "/api/dostk/acnt", tr_id="kt00005", **self._acct_params()
        )

    # ── 주문 ───────────────────────────────────────

    async def buy(
        self,
        stk_cd: str,
        qty: int,
        price: int | None = None,
    ) -> dict[str, Any]:
        """kt10000 - 매수주문

        Args:
            stk_cd: 종목코드 (6자리)
            qty: 주문수량
            price: 지정가 (None이면 시장가)
        """
        order_type = "00" if price else "03"  # 00=지정가, 03=시장가
        data = self._acct_params(
            stk_cd=stk_cd,
            ord_qty=str(qty),
            ord_tp=order_type,
        )
        if price:
            data["ord_prc"] = str(price)

        logger.warning("📈 매수주문: %s %d주 %s", stk_cd, qty, f"{price}원" if price else "시장가")
        return await self._client.post(
            "/api/dostk/acnt", tr_id="kt10000", data=data
        )

    async def sell(
        self,
        stk_cd: str,
        qty: int,
        price: int | None = None,
    ) -> dict[str, Any]:
        """kt10001 - 매도주문

        Args:
            stk_cd: 종목코드 (6자리)
            qty: 주문수량
            price: 지정가 (None이면 시장가)
        """
        order_type = "00" if price else "03"
        data = self._acct_params(
            stk_cd=stk_cd,
            ord_qty=str(qty),
            ord_tp=order_type,
        )
        if price:
            data["ord_prc"] = str(price)

        logger.warning("📉 매도주문: %s %d주 %s", stk_cd, qty, f"{price}원" if price else "시장가")
        return await self._client.post(
            "/api/dostk/acnt", tr_id="kt10001", data=data
        )
