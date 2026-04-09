"""순위 조회 — /api/dostk/rkinfo"""

from __future__ import annotations

from typing import Any

from .client import KiwoomClient


class RankAPI:
    """순위 조회 API"""

    def __init__(self, client: KiwoomClient) -> None:
        self._client = client

    async def top_order_book_volume(
        self,
        mrkt_tp: str = "001", sort_tp: str = "1",
        trde_qty_tp: str = "0", stk_cnd: str = "0",
        crd_cnd: str = "0", stex_tp: str = "1",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10020 — 호가잔량상위요청

        Args:
            mrkt_tp: 시장구분 (001:코스피, 101:코스닥)
            sort_tp: 정렬구분 (1~4)
            trde_qty_tp: 거래량구분 (0:전체)
            stk_cnd: 종목조건 (0:전체)
            crd_cnd: 신용조건 (0:전체)
            stex_tp: 거래소구분 (1:KRX, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka10020",
            mrkt_tp=mrkt_tp, sort_tp=sort_tp, trde_qty_tp=trde_qty_tp,
            stk_cnd=stk_cnd, crd_cnd=crd_cnd, stex_tp=stex_tp, **kw,
        )

    async def sudden_order_book_increase(
        self,
        mrkt_tp: str = "001", trde_tp: str = "1",
        sort_tp: str = "1", tm_tp: str = "3",
        trde_qty_tp: str = "0", stk_cnd: str = "0",
        stex_tp: str = "1",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10021 — 호가잔량급증요청

        Args:
            mrkt_tp: 시장구분 (001:코스피, 101:코스닥)
            trde_tp: 매매구분 (1:매수잔량, 2:매도잔량)
            sort_tp: 정렬구분 (1:급증량, 2:급증률)
            tm_tp: 시간 (분 단위)
            trde_qty_tp: 거래량구분 (0:전체)
            stk_cnd: 종목조건 (0:전체)
            stex_tp: 거래소구분 (1:KRX, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka10021",
            mrkt_tp=mrkt_tp, trde_tp=trde_tp, sort_tp=sort_tp,
            tm_tp=tm_tp, trde_qty_tp=trde_qty_tp,
            stk_cnd=stk_cnd, stex_tp=stex_tp, **kw,
        )

    async def sudden_order_ratio_increase(
        self,
        mrkt_tp: str = "001", rt_tp: str = "1",
        tm_tp: str = "3", trde_qty_tp: str = "0",
        stk_cnd: str = "0", stex_tp: str = "1",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10022 — 잔량율급증요청

        Args:
            mrkt_tp: 시장구분 (001:코스피, 101:코스닥)
            rt_tp: 비율구분 (1:매수/매도비율, 2:매도/매수비율)
            tm_tp: 시간 (분 단위)
            trde_qty_tp: 거래량구분 (0:전체)
            stk_cnd: 종목조건 (0:전체)
            stex_tp: 거래소구분 (1:KRX, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka10022",
            mrkt_tp=mrkt_tp, rt_tp=rt_tp, tm_tp=tm_tp,
            trde_qty_tp=trde_qty_tp, stk_cnd=stk_cnd,
            stex_tp=stex_tp, **kw,
        )

    async def sudden_volume_increase(
        self,
        mrkt_tp: str = "000", sort_tp: str = "1",
        tm_tp: str = "1", trde_qty_tp: str = "0",
        stk_cnd: str = "0", pric_tp: str = "0",
        stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10023 — 거래량급증요청

        Args:
            mrkt_tp: 시장구분 (000:전체, 001:코스피, 101:코스닥)
            sort_tp: 정렬구분 (1~4)
            tm_tp: 시간구분 (1:분, 2:전일)
            trde_qty_tp: 거래량구분 (0:전체)
            stk_cnd: 종목조건 (0:전체)
            pric_tp: 가격조건 (0:전체)
            stex_tp: 거래소구분 (1:KRX, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka10023",
            mrkt_tp=mrkt_tp, sort_tp=sort_tp, tm_tp=tm_tp,
            trde_qty_tp=trde_qty_tp, stk_cnd=stk_cnd,
            pric_tp=pric_tp, stex_tp=stex_tp, **kw,
        )

    async def change_rate_rank(
        self,
        mrkt_tp: str = "000", sort_tp: str = "1",
        trde_qty_cnd: str = "0000", stk_cnd: str = "0",
        crd_cnd: str = "0", updown_incls: str = "0",
        pric_cnd: str = "0", trde_prica_cnd: str = "0",
        stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10027 — 전일대비등락률상위요청

        Args:
            mrkt_tp: 시장구분 (000:전체)
            sort_tp: 정렬구분 (1:상승률, 2:하락률)
            trde_qty_cnd: 거래량조건 (0000:전체)
            stk_cnd: 종목조건 (0:전체)
            crd_cnd: 신용조건 (0:전체)
            updown_incls: 상하한포함 (0:미포함, 1:포함)
            pric_cnd: 가격조건 (0:전체)
            trde_prica_cnd: 거래대금조건 (0:전체)
            stex_tp: 거래소구분 (1:KRX, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka10027",
            mrkt_tp=mrkt_tp, sort_tp=sort_tp, trde_qty_cnd=trde_qty_cnd,
            stk_cnd=stk_cnd, crd_cnd=crd_cnd, updown_incls=updown_incls,
            pric_cnd=pric_cnd, trde_prica_cnd=trde_prica_cnd,
            stex_tp=stex_tp, **kw,
        )

    # alias
    async def top_change_rate(
        self,
        mrkt_tp: str = "000", sort_tp: str = "1",
        trde_qty_cnd: str = "0000", stk_cnd: str = "0",
        crd_cnd: str = "0", updown_incls: str = "0",
        pric_cnd: str = "0", trde_prica_cnd: str = "0",
        stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10027 — 전일대비등락률상위요청 (alias)"""
        return await self.change_rate_rank(
            mrkt_tp=mrkt_tp, sort_tp=sort_tp, trde_qty_cnd=trde_qty_cnd,
            stk_cnd=stk_cnd, crd_cnd=crd_cnd, updown_incls=updown_incls,
            pric_cnd=pric_cnd, trde_prica_cnd=trde_prica_cnd,
            stex_tp=stex_tp, **kw,
        )

    async def top_expected_change_rate(
        self,
        mrkt_tp: str = "000", sort_tp: str = "1",
        trde_qty_cnd: str = "0", stk_cnd: str = "0",
        crd_cnd: str = "0", pric_cnd: str = "0",
        stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10029 — 예상체결등락률상위요청

        Args:
            mrkt_tp: 시장구분 (000:전체)
            sort_tp: 정렬구분 (1:상승률, 2:하락률)
            trde_qty_cnd: 거래량조건 (0:전체)
            stk_cnd: 종목조건 (0:전체)
            crd_cnd: 신용조건 (0:전체)
            pric_cnd: 가격조건 (0:전체)
            stex_tp: 거래소구분 (1:KRX, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka10029",
            mrkt_tp=mrkt_tp, sort_tp=sort_tp, trde_qty_cnd=trde_qty_cnd,
            stk_cnd=stk_cnd, crd_cnd=crd_cnd,
            pric_cnd=pric_cnd, stex_tp=stex_tp, **kw,
        )

    async def volume_rank(
        self,
        mrkt_tp: str = "000", sort_tp: str = "1",
        mang_stk_incls: str = "0", crd_tp: str = "0",
        trde_qty_tp: str = "0", pric_tp: str = "0",
        trde_prica_tp: str = "0", mrkt_open_tp: str = "0",
        stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10030 — 당일거래량상위요청

        Args:
            mrkt_tp: 시장구분 (000:전체)
            sort_tp: 정렬구분 (1:거래량순)
            mang_stk_incls: 관리종목포함 (0:포함)
            crd_tp: 신용구분 (0:전체)
            trde_qty_tp: 거래량조건 (0:전체)
            pric_tp: 가격조건 (0:전체)
            trde_prica_tp: 거래대금조건 (0:전체)
            mrkt_open_tp: 시장개시구분 (0:전체)
            stex_tp: 거래소구분 (1:KRX, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka10030",
            mrkt_tp=mrkt_tp, sort_tp=sort_tp, mang_stk_incls=mang_stk_incls,
            crd_tp=crd_tp, trde_qty_tp=trde_qty_tp, pric_tp=pric_tp,
            trde_prica_tp=trde_prica_tp, mrkt_open_tp=mrkt_open_tp,
            stex_tp=stex_tp, **kw,
        )

    # alias
    async def top_volume_today(
        self,
        mrkt_tp: str = "000", sort_tp: str = "1",
        mang_stk_incls: str = "0", crd_tp: str = "0",
        trde_qty_tp: str = "0", pric_tp: str = "0",
        trde_prica_tp: str = "0", mrkt_open_tp: str = "0",
        stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10030 — 당일거래량상위요청 (alias)"""
        return await self.volume_rank(
            mrkt_tp=mrkt_tp, sort_tp=sort_tp, mang_stk_incls=mang_stk_incls,
            crd_tp=crd_tp, trde_qty_tp=trde_qty_tp, pric_tp=pric_tp,
            trde_prica_tp=trde_prica_tp, mrkt_open_tp=mrkt_open_tp,
            stex_tp=stex_tp, **kw,
        )

    async def top_volume_yesterday(
        self,
        mrkt_tp: str = "000", qry_tp: str = "1",
        rank_strt: str = "0", rank_end: str = "100",
        stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10031 — 전일거래량상위요청

        Args:
            mrkt_tp: 시장구분 (000:전체)
            qry_tp: 조회구분 (1)
            rank_strt: 시작순위 (0)
            rank_end: 종료순위 (100)
            stex_tp: 거래소구분 (1:KRX, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka10031",
            mrkt_tp=mrkt_tp, qry_tp=qry_tp,
            rank_strt=rank_strt, rank_end=rank_end,
            stex_tp=stex_tp, **kw,
        )

    async def value_rank(
        self,
        mrkt_tp: str = "000", mang_stk_incls: str = "0",
        stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10032 — 거래대금상위요청

        Args:
            mrkt_tp: 시장구분 (000:전체)
            mang_stk_incls: 관리종목포함 (0:포함)
            stex_tp: 거래소구분 (1:KRX, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka10032",
            mrkt_tp=mrkt_tp, mang_stk_incls=mang_stk_incls,
            stex_tp=stex_tp, **kw,
        )

    async def top_credit_ratio(
        self,
        mrkt_tp: str = "000", trde_qty_tp: str = "0",
        stk_cnd: str = "0", updown_incls: str = "0",
        crd_cnd: str = "0", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10033 — 신용비율상위요청

        Args:
            mrkt_tp: 시장구분 (000:전체)
            trde_qty_tp: 거래량조건 (0:전체)
            stk_cnd: 종목조건 (0:전체)
            updown_incls: 상하한포함 (0:미포함)
            crd_cnd: 신용조건 (0:전체)
            stex_tp: 거래소구분 (1:KRX, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka10033",
            mrkt_tp=mrkt_tp, trde_qty_tp=trde_qty_tp,
            stk_cnd=stk_cnd, updown_incls=updown_incls,
            crd_cnd=crd_cnd, stex_tp=stex_tp, **kw,
        )

    async def top_foreign_trades_by_period(
        self,
        mrkt_tp: str = "000", trde_tp: str = "3",
        dt: str = "0", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10034 — 외인기간별매매상위요청

        Args:
            mrkt_tp: 시장구분 (000:전체)
            trde_tp: 매매구분 (3:순매매)
            dt: 일자구분 (0:당일)
            stex_tp: 거래소구분 (1:KRX, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka10034",
            mrkt_tp=mrkt_tp, trde_tp=trde_tp,
            dt=dt, stex_tp=stex_tp, **kw,
        )

    async def top_foreign_consecutive_buy(
        self,
        mrkt_tp: str = "000", trde_tp: str = "2",
        base_dt_tp: str = "0", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10035 — 외인연속순매매상위요청

        Args:
            mrkt_tp: 시장구분 (000:전체)
            trde_tp: 매매구분 (2:연속순매수)
            base_dt_tp: 기준일구분 (0)
            stex_tp: 거래소구분 (1:KRX, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka10035",
            mrkt_tp=mrkt_tp, trde_tp=trde_tp,
            base_dt_tp=base_dt_tp, stex_tp=stex_tp, **kw,
        )

    async def top_foreign_limit_increase(self, **kw: Any) -> dict[str, Any]:
        """ka10036 — 외인한도소진율증가상위"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10036", **kw)

    async def top_foreign_broker_trading(
        self,
        mrkt_tp: str = "000", dt: str = "0",
        trde_tp: str = "1", sort_tp: str = "1",
        stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10037 — 외국계창구매매상위요청

        Args:
            mrkt_tp: 시장구분 (000:전체)
            dt: 일자구분 (0:당일)
            trde_tp: 매매구분 (1:순매수)
            sort_tp: 정렬구분 (1:금액)
            stex_tp: 거래소구분 (1:KRX, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka10037",
            mrkt_tp=mrkt_tp, dt=dt, trde_tp=trde_tp,
            sort_tp=sort_tp, stex_tp=stex_tp, **kw,
        )

    async def broker_ranking_by_stock(
        self, stk_cd: str, qry_tp: str = "1", **kw: Any,
    ) -> dict[str, Any]:
        """ka10038 — 종목별증권사순위요청

        Args:
            stk_cd: 종목코드
            qry_tp: 조회구분 (1:순매도순위)
        """
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka10038",
            stk_cd=stk_cd, qry_tp=qry_tp, **kw,
        )

    async def top_broker_by_stock(
        self,
        mmcm_cd: str, trde_qty_tp: str = "0",
        trde_tp: str = "1", dt: str = "1",
        stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10039 — 증권사별매매상위요청

        Args:
            mmcm_cd: 회원사코드 (ka10102 조회)
            trde_qty_tp: 거래량구분 (0:전체)
            trde_tp: 매매구분 (1:순매수)
            dt: 일자구분 (1:전일)
            stex_tp: 거래소구분 (1:KRX, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka10039",
            mmcm_cd=mmcm_cd, trde_qty_tp=trde_qty_tp,
            trde_tp=trde_tp, dt=dt, stex_tp=stex_tp, **kw,
        )

    async def main_brokers_today(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10040 — 당일주요거래원요청

        Args:
            stk_cd: 종목코드
        """
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10040", stk_cd=stk_cd, **kw)

    async def top_net_buying_brokers(
        self,
        stk_cd: str, qry_dt_tp: str = "0",
        pot_tp: str = "0", sort_base: str = "1",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10042 — 순매수거래원순위요청

        Args:
            stk_cd: 종목코드
            qry_dt_tp: 조회기간구분 (0)
            pot_tp: 시점구분 (0:당일)
            sort_base: 정렬기준 (1:종가순)
        """
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka10042",
            stk_cd=stk_cd, qry_dt_tp=qry_dt_tp,
            pot_tp=pot_tp, sort_base=sort_base, **kw,
        )

    async def departed_brokers_today(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10053 — 당일상위이탈원요청

        Args:
            stk_cd: 종목코드
        """
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10053", stk_cd=stk_cd, **kw)

    async def same_day_net_buying_rank(
        self,
        strt_dt: str, mrkt_tp: str = "000",
        trde_tp: str = "1", sort_cnd: str = "1",
        unit_tp: str = "1", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10062 — 동일순매매순위요청

        Args:
            strt_dt: 시작일자 (YYYYMMDD)
            mrkt_tp: 시장구분 (000:전체)
            trde_tp: 매매구분 (1:순매수)
            sort_cnd: 정렬조건 (1:수량)
            unit_tp: 단위구분 (1:단주)
            stex_tp: 거래소구분 (1:KRX, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka10062",
            strt_dt=strt_dt, mrkt_tp=mrkt_tp, trde_tp=trde_tp,
            sort_cnd=sort_cnd, unit_tp=unit_tp, stex_tp=stex_tp, **kw,
        )

    async def top_intraday_investor_trading(
        self,
        trde_tp: str = "1", mrkt_tp: str = "000",
        orgn_tp: str = "9000",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10065 — 장중투자자별매매상위요청

        Args:
            trde_tp: 매매구분 (1:순매수)
            mrkt_tp: 시장구분 (000:전체)
            orgn_tp: 기관구분 (9000:외국인)
        """
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka10065",
            trde_tp=trde_tp, mrkt_tp=mrkt_tp, orgn_tp=orgn_tp, **kw,
        )

    async def after_hours_change_rate_rank(
        self,
        mrkt_tp: str = "000", sort_base: str = "1",
        stk_cnd: str = "0", trde_qty_cnd: str = "0",
        crd_cnd: str = "0", trde_prica: str = "0",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10098 — 시간외단일가등락율순위요청

        Args:
            mrkt_tp: 시장구분 (000:전체)
            sort_base: 정렬기준 (1)
            stk_cnd: 종목조건 (0:전체)
            trde_qty_cnd: 거래량조건 (0:전체)
            crd_cnd: 신용조건 (0:전체)
            trde_prica: 거래대금 (0:전체)
        """
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka10098",
            mrkt_tp=mrkt_tp, sort_base=sort_base,
            stk_cnd=stk_cnd, trde_qty_cnd=trde_qty_cnd,
            crd_cnd=crd_cnd, trde_prica=trde_prica, **kw,
        )

    async def top_foreign_institution_trades(
        self,
        mrkt_tp: str = "000", amt_qty_tp: str = "1",
        qry_dt_tp: str = "0", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka90009 — 외국인기관매매상위요청

        Args:
            mrkt_tp: 시장구분 (000:전체)
            amt_qty_tp: 금액수량구분 (1:금액, 2:수량)
            qry_dt_tp: 조회기간구분 (0)
            stex_tp: 거래소구분 (1:KRX, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka90009",
            mrkt_tp=mrkt_tp, amt_qty_tp=amt_qty_tp,
            qry_dt_tp=qry_dt_tp, stex_tp=stex_tp, **kw,
        )

    # aliases for old names
    async def orderbook_rank(self, **kw: Any) -> dict[str, Any]:
        return await self.top_order_book_volume(**kw)
