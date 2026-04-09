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

    async def deposit(self, qry_tp: str = "3", **kw: Any) -> dict[str, Any]:
        """kt00001 — 예수금상세현황요청

        Args:
            qry_tp: 조회구분 (2:일반조회, 3:추정조회)
        """
        return await self._client.get("/api/dostk/acnt", tr_id="kt00001", **self._acct_params(qry_tp=qry_tp, **kw))

    async def daily_estimated_deposit(self, start_dt: str, end_dt: str, **kw: Any) -> dict[str, Any]:
        """kt00002 — 일별추정예탁자산현황요청

        Args:
            start_dt: 시작조회기간 (YYYYMMDD)
            end_dt: 종료조회기간 (YYYYMMDD)
        """
        return await self._client.get(
            "/api/dostk/acnt", tr_id="kt00002",
            **self._acct_params(start_dt=start_dt, end_dt=end_dt, **kw),
        )

    async def estimated_asset(self, qry_tp: str = "0", **kw: Any) -> dict[str, Any]:
        """kt00003 — 추정자산조회요청

        Args:
            qry_tp: 상장폐지조회구분 (0:전체, 1:상장폐지종목제외)
        """
        return await self._client.get(
            "/api/dostk/acnt", tr_id="kt00003",
            **self._acct_params(qry_tp=qry_tp, **kw),
        )

    async def account_summary(
        self, qry_tp: str = "0", dmst_stex_tp: str = "KRX", **kw: Any,
    ) -> dict[str, Any]:
        """kt00004 — 계좌평가현황요청 (총 평가금액, 수익률)

        Args:
            qry_tp: 상장폐지조회구분 (0:전체, 1:상장폐지종목제외)
            dmst_stex_tp: 국내거래소구분 (KRX, NXT)
        """
        return await self._client.get(
            "/api/dostk/acnt", tr_id="kt00004",
            **self._acct_params(qry_tp=qry_tp, dmst_stex_tp=dmst_stex_tp, **kw),
        )

    async def holdings(self, dmst_stex_tp: str = "KRX", **kw: Any) -> dict[str, Any]:
        """kt00005 — 체결잔고요청 (보유 종목별 잔고)

        Args:
            dmst_stex_tp: 국내거래소구분 (KRX, NXT)
        """
        return await self._client.get(
            "/api/dostk/acnt", tr_id="kt00005",
            **self._acct_params(dmst_stex_tp=dmst_stex_tp, **kw),
        )

    async def order_execution_detail(
        self,
        qry_tp: str = "1", stk_bond_tp: str = "0",
        sell_tp: str = "0", dmst_stex_tp: str = "%",
        **kw: Any,
    ) -> dict[str, Any]:
        """kt00007 — 계좌별주문체결내역상세요청

        Args:
            qry_tp: 조회구분 (1:주문순, 2:역순, 3:미체결, 4:체결내역만)
            stk_bond_tp: 주식채권구분 (0:전체, 1:주식, 2:채권)
            sell_tp: 매도수구분 (0:전체, 1:매도, 2:매수)
            dmst_stex_tp: 국내거래소구분 (%:전체, KRX, NXT, SOR)
        """
        return await self._client.get(
            "/api/dostk/acnt", tr_id="kt00007",
            **self._acct_params(
                qry_tp=qry_tp, stk_bond_tp=stk_bond_tp,
                sell_tp=sell_tp, dmst_stex_tp=dmst_stex_tp, **kw,
            ),
        )

    async def next_day_settlement(self, **kw: Any) -> dict[str, Any]:
        """kt00008 — 계좌별익일결제예정내역요청"""
        return await self._client.get("/api/dostk/acnt", tr_id="kt00008", **self._acct_params(**kw))

    async def order_execution_status(
        self,
        stk_bond_tp: str = "0", mrkt_tp: str = "0",
        sell_tp: str = "0", qry_tp: str = "0", dmst_stex_tp: str = "%",
        **kw: Any,
    ) -> dict[str, Any]:
        """kt00009 — 계좌별주문체결현황요청

        Args:
            stk_bond_tp: 주식채권구분 (0:전체, 1:주식, 2:채권)
            mrkt_tp: 시장구분 (0:전체, 1:코스피, 2:코스닥)
            sell_tp: 매도수구분 (0:전체, 1:매도, 2:매수)
            qry_tp: 조회구분 (0:전체, 1:체결)
            dmst_stex_tp: 국내거래소구분 (%:전체, KRX, NXT, SOR)
        """
        return await self._client.get(
            "/api/dostk/acnt", tr_id="kt00009",
            **self._acct_params(
                stk_bond_tp=stk_bond_tp, mrkt_tp=mrkt_tp,
                sell_tp=sell_tp, qry_tp=qry_tp, dmst_stex_tp=dmst_stex_tp, **kw,
            ),
        )

    async def withdrawable_amount(self, stk_cd: str, trde_tp: str = "1", uv: str = "", **kw: Any) -> dict[str, Any]:
        """kt00010 — 주문인출가능금액요청

        Args:
            stk_cd: 종목번호
            trde_tp: 매매구분 (1:매도, 2:매수)
            uv: 매수가격
        """
        return await self._client.get(
            "/api/dostk/acnt", tr_id="kt00010",
            **self._acct_params(stk_cd=stk_cd, trde_tp=trde_tp, uv=uv, **kw),
        )

    async def orderable_qty_by_margin(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """kt00011 — 증거금율별주문가능수량조회요청

        Args:
            stk_cd: 종목번호
        """
        return await self._client.get(
            "/api/dostk/acnt", tr_id="kt00011",
            **self._acct_params(stk_cd=stk_cd, **kw),
        )

    async def orderable_qty_by_credit(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """kt00012 — 신용보증금율별주문가능수량조회요청

        Args:
            stk_cd: 종목번호
        """
        return await self._client.get(
            "/api/dostk/acnt", tr_id="kt00012",
            **self._acct_params(stk_cd=stk_cd, **kw),
        )

    async def margin_detail(self, **kw: Any) -> dict[str, Any]:
        """kt00013 — 증거금세부내역조회요청"""
        return await self._client.get("/api/dostk/acnt", tr_id="kt00013", **self._acct_params(**kw))

    async def comprehensive_transaction_history(
        self,
        strt_dt: str, end_dt: str, tp: str = "0",
        gds_tp: str = "0", dmst_stex_tp: str = "%",
        **kw: Any,
    ) -> dict[str, Any]:
        """kt00015 — 위탁종합거래내역요청

        Args:
            strt_dt: 시작일자 (YYYYMMDD)
            end_dt: 종료일자 (YYYYMMDD)
            tp: 구분 (0:전체, 1:입출금, 2:입출고, 3:매매, ...)
            gds_tp: 상품구분 (0:전체, 1:국내주식, 2:수익증권, ...)
            dmst_stex_tp: 국내거래소구분 (%:전체, KRX, NXT)
        """
        return await self._client.get(
            "/api/dostk/acnt", tr_id="kt00015",
            **self._acct_params(
                strt_dt=strt_dt, end_dt=end_dt, tp=tp,
                gds_tp=gds_tp, dmst_stex_tp=dmst_stex_tp, **kw,
            ),
        )

    async def daily_return_detail(self, fr_dt: str, to_dt: str, **kw: Any) -> dict[str, Any]:
        """kt00016 — 일별계좌수익률상세현황요청

        Args:
            fr_dt: 평가시작일 (YYYYMMDD)
            to_dt: 평가종료일 (YYYYMMDD)
        """
        return await self._client.get(
            "/api/dostk/acnt", tr_id="kt00016",
            **self._acct_params(fr_dt=fr_dt, to_dt=to_dt, **kw),
        )

    async def today_account_status(self, **kw: Any) -> dict[str, Any]:
        """kt00017 — 계좌별당일현황요청"""
        return await self._client.get("/api/dostk/acnt", tr_id="kt00017", **self._acct_params(**kw))

    async def evaluation_balance_detail(
        self, qry_tp: str = "1", dmst_stex_tp: str = "KRX", **kw: Any,
    ) -> dict[str, Any]:
        """kt00018 — 계좌평가잔고내역요청

        Args:
            qry_tp: 조회구분 (1:합산, 2:개별)
            dmst_stex_tp: 국내거래소구분 (KRX, NXT)
        """
        return await self._client.get(
            "/api/dostk/acnt", tr_id="kt00018",
            **self._acct_params(qry_tp=qry_tp, dmst_stex_tp=dmst_stex_tp, **kw),
        )

    # ── 계좌 조회 (/api/dostk/acnt, ka*) ──────────

    async def account_number_inquiry(self, **kw: Any) -> dict[str, Any]:
        """ka00001 — 계좌번호조회"""
        return await self._client.get("/api/dostk/acnt", tr_id="ka00001", **kw)

    async def daily_balance_return_rate(self, qry_dt: str, **kw: Any) -> dict[str, Any]:
        """ka01690 — 일별잔고수익률

        Args:
            qry_dt: 조회일자 (YYYYMMDD)
        """
        return await self._client.get(
            "/api/dostk/acnt", tr_id="ka01690",
            **self._acct_params(qry_dt=qry_dt, **kw),
        )

    async def realized_profit_by_date(self, strt_dt: str, **kw: Any) -> dict[str, Any]:
        """ka10072 — 일자별종목별실현손익요청_일자

        Args:
            strt_dt: 시작일자 (YYYYMMDD)
        """
        return await self._client.get(
            "/api/dostk/acnt", tr_id="ka10072",
            **self._acct_params(strt_dt=strt_dt, **kw),
        )

    async def realized_profit_by_period(self, strt_dt: str, end_dt: str, **kw: Any) -> dict[str, Any]:
        """ka10073 — 일자별종목별실현손익요청_기간

        Args:
            strt_dt: 시작일자 (YYYYMMDD)
            end_dt: 종료일자 (YYYYMMDD)
        """
        return await self._client.get(
            "/api/dostk/acnt", tr_id="ka10073",
            **self._acct_params(strt_dt=strt_dt, end_dt=end_dt, **kw),
        )

    async def daily_realized_profit(self, strt_dt: str, end_dt: str, **kw: Any) -> dict[str, Any]:
        """ka10074 — 일자별실현손익요청

        Args:
            strt_dt: 시작일자
            end_dt: 종료일자
        """
        return await self._client.get(
            "/api/dostk/acnt", tr_id="ka10074",
            **self._acct_params(strt_dt=strt_dt, end_dt=end_dt, **kw),
        )

    async def unfilled_orders(
        self,
        all_stk_tp: str = "0", trde_tp: str = "0", stex_tp: str = "0",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10075 — 미체결요청

        Args:
            all_stk_tp: 전체종목구분 (0:전체, 1:종목)
            trde_tp: 매매구분 (0:전체, 1:매도, 2:매수)
            stex_tp: 거래소구분 (0:통합, 1:KRX, 2:NXT)
        """
        return await self._client.get(
            "/api/dostk/acnt", tr_id="ka10075",
            **self._acct_params(all_stk_tp=all_stk_tp, trde_tp=trde_tp, stex_tp=stex_tp, **kw),
        )

    async def filled_orders(
        self, qry_tp: str = "0", sell_tp: str = "0", stex_tp: str = "0",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10076 — 체결요청

        Args:
            qry_tp: 조회구분 (0:전체, 1:종목)
            sell_tp: 매도수구분 (0:전체, 1:매도, 2:매수)
            stex_tp: 거래소구분 (0:통합, 1:KRX, 2:NXT)
        """
        return await self._client.get(
            "/api/dostk/acnt", tr_id="ka10076",
            **self._acct_params(qry_tp=qry_tp, sell_tp=sell_tp, stex_tp=stex_tp, **kw),
        )

    async def today_realized_profit_detail(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10077 — 당일실현손익상세요청

        Args:
            stk_cd: 종목코드
        """
        return await self._client.get(
            "/api/dostk/acnt", tr_id="ka10077",
            **self._acct_params(stk_cd=stk_cd, **kw),
        )

    async def account_return_rate(self, stex_tp: str = "0", **kw: Any) -> dict[str, Any]:
        """ka10085 — 계좌수익률요청

        Args:
            stex_tp: 거래소구분 (0:통합, 1:KRX, 2:NXT)
        """
        return await self._client.get(
            "/api/dostk/acnt", tr_id="ka10085",
            **self._acct_params(stex_tp=stex_tp, **kw),
        )

    async def unfilled_split_order_detail(self, ord_no: str, **kw: Any) -> dict[str, Any]:
        """ka10088 — 미체결 분할주문 상세

        Args:
            ord_no: 주문번호
        """
        return await self._client.get(
            "/api/dostk/acnt", tr_id="ka10088",
            **self._acct_params(ord_no=ord_no, **kw),
        )

    async def today_trading_journal(
        self, ottks_tp: str = "1", ch_crd_tp: str = "0", **kw: Any,
    ) -> dict[str, Any]:
        """ka10170 — 당일매매일지요청

        Args:
            ottks_tp: 단주구분 (1:당일매수에 대한 당일매도, 2:당일매도전체)
            ch_crd_tp: 현금신용구분 (0:전체, 1:현금매매만, 2:신용매매만)
        """
        return await self._client.get(
            "/api/dostk/acnt", tr_id="ka10170",
            **self._acct_params(ottks_tp=ottks_tp, ch_crd_tp=ch_crd_tp, **kw),
        )

    # ── 주문 (/api/dostk/ordr) ────────────────────

    async def buy(
        self, stk_cd: str, qty: int, price: int | None = None,
        dmst_stex_tp: str = "KRX", **kw: Any,
    ) -> dict[str, Any]:
        """kt10000 — 매수주문

        Args:
            stk_cd: 종목코드 (6자리)
            qty: 주문수량
            price: 지정가 (None이면 시장가)
            dmst_stex_tp: 거래소구분 (KRX, NXT, SOR)
        """
        trde_tp = "00" if price else "03"  # 00:지정가, 03:시장가
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
        dmst_stex_tp: str = "KRX", **kw: Any,
    ) -> dict[str, Any]:
        """kt10001 — 매도주문

        Args:
            stk_cd: 종목코드 (6자리)
            qty: 주문수량
            price: 지정가 (None이면 시장가)
            dmst_stex_tp: 거래소구분 (KRX, NXT, SOR)
        """
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

    async def modify_order(
        self, org_ord_no: str, stk_cd: str,
        mdfy_qty: str = "", mdfy_uv: str = "",
        dmst_stex_tp: str = "KRX", **kw: Any,
    ) -> dict[str, Any]:
        """kt10002 — 정정주문

        Args:
            org_ord_no: 원주문번호
            stk_cd: 종목코드
            mdfy_qty: 정정수량
            mdfy_uv: 정정단가
            dmst_stex_tp: 거래소구분 (KRX, NXT, SOR)
        """
        data = self._acct_params(
            dmst_stex_tp=dmst_stex_tp, orig_ord_no=org_ord_no,
            stk_cd=stk_cd, mdfy_qty=mdfy_qty, mdfy_uv=mdfy_uv,
            **kw,
        )
        logger.warning("✏️ 정정: 주문번호 %s", org_ord_no)
        return await self._client.post("/api/dostk/ordr", tr_id="kt10002", data=data)

    async def cancel_order(
        self, org_ord_no: str, stk_cd: str,
        cncl_qty: str = "0", dmst_stex_tp: str = "KRX", **kw: Any,
    ) -> dict[str, Any]:
        """kt10003 — 취소주문

        Args:
            org_ord_no: 원주문번호
            stk_cd: 종목코드
            cncl_qty: 취소수량 ('0'이면 잔량 전부 취소)
            dmst_stex_tp: 거래소구분 (KRX, NXT, SOR)
        """
        data = self._acct_params(
            dmst_stex_tp=dmst_stex_tp, orig_ord_no=org_ord_no,
            stk_cd=stk_cd, cncl_qty=cncl_qty,
            **kw,
        )
        logger.warning("❌ 취소: 주문번호 %s", org_ord_no)
        return await self._client.post("/api/dostk/ordr", tr_id="kt10003", data=data)
