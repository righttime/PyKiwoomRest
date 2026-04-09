"""계좌 조회 & 주문 — /api/dostk/acnt, /api/dostk/ordr"""

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

    # ── 계좌 조회 (/api/dostk/acnt) ──────────────

    async def deposit(self) -> dict[str, Any]:
        """kt00001 — 예수금상세현황요청"""
        return await self._client.get("/api/dostk/acnt", tr_id="kt00001", **self._acct_params())

    async def daily_estimated_deposit(self, **kw: Any) -> dict[str, Any]:
        """kt00002 — 일별추정예탁자산현황요청"""
        return await self._client.get("/api/dostk/acnt", tr_id="kt00002", **self._acct_params(**kw))

    async def estimated_asset(self, **kw: Any) -> dict[str, Any]:
        """kt00003 — 추정자산조회요청"""
        return await self._client.get("/api/dostk/acnt", tr_id="kt00003", **self._acct_params(**kw))

    async def account_summary(self) -> dict[str, Any]:
        """kt00004 — 계좌평가현황요청 (총 평가금액, 수익률)"""
        return await self._client.get("/api/dostk/acnt", tr_id="kt00004", **self._acct_params())

    async def holdings(self) -> dict[str, Any]:
        """kt00005 — 체결잔고요청 (보유 종목별 잔고)"""
        return await self._client.get("/api/dostk/acnt", tr_id="kt00005", **self._acct_params())

    async def order_execution_detail(self, **kw: Any) -> dict[str, Any]:
        """kt00007 — 계좌별주문체결내역상세요청"""
        return await self._client.get("/api/dostk/acnt", tr_id="kt00007", **self._acct_params(**kw))

    async def next_day_settlement(self, **kw: Any) -> dict[str, Any]:
        """kt00008 — 계좌별익일결제예정내역요청"""
        return await self._client.get("/api/dostk/acnt", tr_id="kt00008", **self._acct_params(**kw))

    async def order_execution_status(self, **kw: Any) -> dict[str, Any]:
        """kt00009 — 계좌별주문체결현황요청"""
        return await self._client.get("/api/dostk/acnt", tr_id="kt00009", **self._acct_params(**kw))

    async def withdrawable_amount(self, **kw: Any) -> dict[str, Any]:
        """kt00010 — 주문인출가능금액요청"""
        return await self._client.get("/api/dostk/acnt", tr_id="kt00010", **self._acct_params(**kw))

    async def orderable_qty_by_margin(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """kt00011 — 증거금율별주문가능수량조회요청"""
        return await self._client.get("/api/dostk/acnt", tr_id="kt00011", **self._acct_params(stk_cd=stk_cd, **kw))

    async def orderable_qty_by_credit(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """kt00012 — 신용보증금율별주문가능수량조회요청"""
        return await self._client.get("/api/dostk/acnt", tr_id="kt00012", **self._acct_params(stk_cd=stk_cd, **kw))

    async def margin_detail(self, **kw: Any) -> dict[str, Any]:
        """kt00013 — 증거금세부내역조회요청"""
        return await self._client.get("/api/dostk/acnt", tr_id="kt00013", **self._acct_params(**kw))

    async def comprehensive_transaction_history(self, **kw: Any) -> dict[str, Any]:
        """kt00015 — 위탁종합거래내역요청"""
        return await self._client.get("/api/dostk/acnt", tr_id="kt00015", **self._acct_params(**kw))

    async def daily_return_detail(self, **kw: Any) -> dict[str, Any]:
        """kt00016 — 일별계좌수익률상세현황요청"""
        return await self._client.get("/api/dostk/acnt", tr_id="kt00016", **self._acct_params(**kw))

    async def today_account_status(self, **kw: Any) -> dict[str, Any]:
        """kt00017 — 계좌별당일현황요청"""
        return await self._client.get("/api/dostk/acnt", tr_id="kt00017", **self._acct_params(**kw))

    async def evaluation_balance_detail(self, **kw: Any) -> dict[str, Any]:
        """kt00018 — 계좌평가잔고내역요청"""
        return await self._client.get("/api/dostk/acnt", tr_id="kt00018", **self._acct_params(**kw))

    # ── 계좌 조회 (/api/dostk/acnt, ka*) ──────────

    async def account_number_inquiry(self, **kw: Any) -> dict[str, Any]:
        """ka00001 — 계좌번호조회"""
        return await self._client.get("/api/dostk/acnt", tr_id="ka00001", **kw)

    async def daily_balance_return_rate(self, **kw: Any) -> dict[str, Any]:
        """ka01690 — 일별잔고수익률"""
        return await self._client.get("/api/dostk/acnt", tr_id="ka01690", **self._acct_params(**kw))

    async def realized_profit_by_date(self, **kw: Any) -> dict[str, Any]:
        """ka10072 — 일자별종목별실현손익요청_일자"""
        return await self._client.get("/api/dostk/acnt", tr_id="ka10072", **self._acct_params(**kw))

    async def realized_profit_by_period(self, **kw: Any) -> dict[str, Any]:
        """ka10073 — 일자별종목별실현손익요청_기간"""
        return await self._client.get("/api/dostk/acnt", tr_id="ka10073", **self._acct_params(**kw))

    async def daily_realized_profit(self, **kw: Any) -> dict[str, Any]:
        """ka10074 — 일자별실현손익요청"""
        return await self._client.get("/api/dostk/acnt", tr_id="ka10074", **self._acct_params(**kw))

    async def unfilled_orders(self, **kw: Any) -> dict[str, Any]:
        """ka10075 — 미체결요청"""
        return await self._client.get("/api/dostk/acnt", tr_id="ka10075", **self._acct_params(**kw))

    async def filled_orders(self, **kw: Any) -> dict[str, Any]:
        """ka10076 — 체결요청"""
        return await self._client.get("/api/dostk/acnt", tr_id="ka10076", **self._acct_params(**kw))

    async def today_realized_profit_detail(self, **kw: Any) -> dict[str, Any]:
        """ka10077 — 당일실현손익상세요청"""
        return await self._client.get("/api/dostk/acnt", tr_id="ka10077", **self._acct_params(**kw))

    async def account_return_rate(self, **kw: Any) -> dict[str, Any]:
        """ka10085 — 계좌수익률요청"""
        return await self._client.get("/api/dostk/acnt", tr_id="ka10085", **self._acct_params(**kw))

    async def unfilled_split_order_detail(self, **kw: Any) -> dict[str, Any]:
        """ka10088 — 미체결 분할주문 상세"""
        return await self._client.get("/api/dostk/acnt", tr_id="ka10088", **self._acct_params(**kw))

    async def today_trading_journal(self, **kw: Any) -> dict[str, Any]:
        """ka10170 — 당일매매일지요청"""
        return await self._client.get("/api/dostk/acnt", tr_id="ka10170", **self._acct_params(**kw))

    # ── 주문 (/api/dostk/ordr) ────────────────────

    async def buy(
        self, stk_cd: str, qty: int, price: int | None = None,
        dmst_stex_tp: str = "01", **kw: Any,
    ) -> dict[str, Any]:
        """kt10000 — 매수주문

        Args:
            stk_cd: 종목코드 (6자리)
            qty: 주문수량
            price: 지정가 (None이면 시장가)
            dmst_stex_tp: 거래소구분 (01=KRX, 81=NXT, 12=SOR)
        """
        trde_tp = "00" if price else "03"  # 00=지정가, 03=시장가
        data = self._acct_params(
            dmst_stex_tp=dmst_stex_tp,
            stk_cd=stk_cd,
            ord_qty=str(qty),
            trde_tp=trde_tp,
            **kw,
        )
        if price:
            data["ord_uv"] = str(price)
        logger.warning("📈 매수: %s %d주 %s", stk_cd, qty, f"{price}원" if price else "시장가")
        return await self._client.post("/api/dostk/ordr", tr_id="kt10000", data=data)

    async def sell(
        self, stk_cd: str, qty: int, price: int | None = None,
        dmst_stex_tp: str = "01", **kw: Any,
    ) -> dict[str, Any]:
        """kt10001 — 매도주문"""
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
        logger.warning("📉 매도: %s %d주 %s", stk_cd, qty, f"{price}원" if price else "시장가")
        return await self._client.post("/api/dostk/ordr", tr_id="kt10001", data=data)

    async def modify_order(self, org_ord_no: str, **kw: Any) -> dict[str, Any]:
        """kt10002 — 정정주문"""
        data = self._acct_params(org_ord_no=org_ord_no, **kw)
        logger.warning("✏️ 정정: 주문번호 %s", org_ord_no)
        return await self._client.post("/api/dostk/ordr", tr_id="kt10002", data=data)

    async def cancel_order(self, org_ord_no: str, **kw: Any) -> dict[str, Any]:
        """kt10003 — 취소주문"""
        data = self._acct_params(org_ord_no=org_ord_no, **kw)
        logger.warning("❌ 취소: 주문번호 %s", org_ord_no)
        return await self._client.post("/api/dostk/ordr", tr_id="kt10003", data=data)
