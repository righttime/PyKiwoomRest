"""신용 주문 — /api/dostk/crdordr"""

from __future__ import annotations

import logging
from typing import Any

from .client import KiwoomClient

logger = logging.getLogger("pykiwoomrest.credit")


class CreditAPI:
    """신용 매매 API"""

    def __init__(self, client: KiwoomClient, account_no: str | None = None) -> None:
        self._client = client
        self._account_no = account_no or client.config.account_no

    def _acct_params(self, **extra: Any) -> dict[str, Any]:
        params: dict[str, Any] = {"acct_no": self._account_no}
        params.update(extra)
        return params

    async def margin_buy_order(
        self, stk_cd: str, qty: int, price: int | None = None,
        dmst_stex_tp: str = "01", **kw: Any,
    ) -> dict[str, Any]:
        """kt10006 — 신용 매수주문"""
        trde_tp = "00" if price else "03"
        data = self._acct_params(
            dmst_stex_tp=dmst_stex_tp,
            stk_cd=stk_cd,
            ord_qty=str(qty),
            trde_tp=trde_tp,
            **kw,
        )
        if price:
            data["ord_uv"] = str(price)
        logger.warning("📈 신용매수: %s %d주", stk_cd, qty)
        return await self._client.post("/api/dostk/crdordr", tr_id="kt10006", data=data)

    async def margin_sell_order(
        self, stk_cd: str, qty: int, price: int | None = None,
        dmst_stex_tp: str = "01", **kw: Any,
    ) -> dict[str, Any]:
        """kt10007 — 신용 매도주문"""
        trde_tp = "00" if price else "03"
        data = self._acct_params(
            dmst_stex_tp=dmst_stex_tp,
            stk_cd=stk_cd,
            ord_qty=str(qty),
            trde_tp=trde_tp,
            **kw,
        )
        if price:
            data["ord_uv"] = str(price)
        logger.warning("📉 신용매도: %s %d주", stk_cd, qty)
        return await self._client.post("/api/dostk/crdordr", tr_id="kt10007", data=data)

    async def margin_modify_order(self, org_ord_no: str, **kw: Any) -> dict[str, Any]:
        """kt10008 — 신용 정정주문"""
        data = self._acct_params(org_ord_no=org_ord_no, **kw)
        return await self._client.post("/api/dostk/crdordr", tr_id="kt10008", data=data)

    async def margin_cancel_order(self, org_ord_no: str, **kw: Any) -> dict[str, Any]:
        """kt10009 — 신용 취소주문"""
        data = self._acct_params(org_ord_no=org_ord_no, **kw)
        return await self._client.post("/api/dostk/crdordr", tr_id="kt10009", data=data)
