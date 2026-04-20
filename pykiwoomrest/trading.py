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
        """kt10000 - 매수주문"""
        order_type = "00" if price else "03"
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
        """kt10001 - 매도주문"""
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

    async def cancel_order(
        self,
        orig_ord_no: str,
        stk_cd: str,
        qty: int | None = None,
    ) -> dict[str, Any]:
        """kt10003 - 주문취소"""
        data = self._acct_params(
            dmst_stex_tp="KRX",
            orig_ord_no=orig_ord_no,
            stk_cd=stk_cd,
        )
        if qty is not None:
            data["cncl_qty"] = str(qty)
        else:
            data["cncl_qty"] = "0"  # 전량 취소
        logger.warning("❌ 주문취소: %s %s", orig_ord_no, stk_cd)
        return await self._client.post(
            "/api/dostk/ordr", tr_id="kt10003", data=data
        )

    async def modify_order(
        self,
        orig_ord_no: str,
        stk_cd: str,
        mdfy_qty: int,
        mdfy_price: int,
    ) -> dict[str, Any]:
        """kt10002 - 주문정정"""
        data = self._acct_params(
            dmst_stex_tp="KRX",
            orig_ord_no=orig_ord_no,
            stk_cd=stk_cd,
            mdfy_qty=str(mdfy_qty),
            mdfy_uv=str(mdfy_price),
            mdfy_cond_uv="",
        )
        logger.warning("🔁 주문정정: %s %s %d주 → %d원", orig_ord_no, stk_cd, mdfy_qty, mdfy_price)
        return await self._client.post(
            "/api/dostk/ordr", tr_id="kt10002", data=data
        )

    async def unfulfilled_orders(
        self,
        all_stk_tp: str = "0",
        trde_tp: str = "0",
        stk_cd: str = "",
    ) -> dict[str, Any]:
        """ka10075 - 미체결조회

        Args:
            all_stk_tp: 전체종목구분 0:전체, 1:종목
            trde_tp:    매매구분    0:전체, 1:매도, 2:매수
            stk_cd:     종목코드 (all_stk_tp=1일 때 필수)
        """
        data = self._acct_params(
            all_stk_tp=all_stk_tp,
            trde_tp=trde_tp,
            stk_cd=stk_cd,
            stex_tp="0",
        )
        logger.debug("🔍 미체결조회: all_stk_tp=%s trde_tp=%s stk_cd=%s", all_stk_tp, trde_tp, stk_cd)
        return await self._client.post(
            "/api/dostk/acnt", tr_id="ka10075", data=data
        )
