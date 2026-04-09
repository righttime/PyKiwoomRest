"""시세/종목/호가 조회 — /api/dostk/stkinfo, /api/dostk/mrkcond"""

from __future__ import annotations

from typing import Any

from .client import KiwoomClient


class MarketAPI:
    """시세 & 종목 정보 API"""

    def __init__(self, client: KiwoomClient) -> None:
        self._client = client

    # ── 종목정보 (/api/dostk/stkinfo) ─────────────

    async def basic_info(self, stk_cd: str) -> dict[str, Any]:
        """ka10001 — 주식기본정보요청 (현재가, 전일대비, 등락률)

        Args:
            stk_cd: 종목코드 (6자리)
        """
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10001", stk_cd=stk_cd)

    async def trading_agent(self, stk_cd: str) -> dict[str, Any]:
        """ka10002 — 주식거래원요청 (매수/매도 거래원)

        Args:
            stk_cd: 종목코드
        """
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10002", stk_cd=stk_cd)

    # alias
    async def trade_volume_by_firm(self, stk_cd: str) -> dict[str, Any]:
        return await self.trading_agent(stk_cd)

    async def execution_info(self, stk_cd: str) -> dict[str, Any]:
        """ka10003 — 체결정보요청

        Args:
            stk_cd: 종목코드
        """
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10003", stk_cd=stk_cd)

    async def credit_trading_trend(
        self, stk_cd: str, dt: str, qry_tp: str = "1", **kw: Any,
    ) -> dict[str, Any]:
        """ka10013 — 신용매매동향요청

        Args:
            stk_cd: 종목코드
            dt: 일자 (YYYYMMDD)
            qry_tp: 조회구분 (1:융자, 2:대주)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10013",
            stk_cd=stk_cd, dt=dt, qry_tp=qry_tp, **kw,
        )

    async def daily_transaction_detail(self, stk_cd: str, strt_dt: str, **kw: Any) -> dict[str, Any]:
        """ka10015 — 일별거래상세요청

        Args:
            stk_cd: 종목코드
            strt_dt: 시작일자 (YYYYMMDD)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10015",
            stk_cd=stk_cd, strt_dt=strt_dt, **kw,
        )

    async def new_high_low(
        self,
        mrkt_tp: str = "000", ntl_tp: str = "1", high_low_close_tp: str = "1",
        stk_cnd: str = "0", trde_qty_tp: str = "00000", crd_cnd: str = "0",
        updown_incls: str = "0", dt: str = "20", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10016 — 신고저가요청

        Args:
            mrkt_tp: 시장구분 (000:전체, 001:코스피, 101:코스닥)
            ntl_tp: 신고저구분 (1:신고가, 2:신저가)
            high_low_close_tp: 고저종구분 (1:고저기준, 2:종가기준)
            stk_cnd: 종목조건 (0:전체, 1:관리종목제외, 3:우선주제외, ...)
            trde_qty_tp: 거래량구분 (00000:전체, 00010:만주이상, ...)
            crd_cnd: 신용조건 (0:전체, 1:신용융자A군, ...)
            updown_incls: 상하한포함 (0:미포함, 1:포함)
            dt: 기간 (5, 10, 20, 60, 250)
            stex_tp: 거래소구분 (1:KRX, 2:NXT, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10016",
            mrkt_tp=mrkt_tp, ntl_tp=ntl_tp, high_low_close_tp=high_low_close_tp,
            stk_cnd=stk_cnd, trde_qty_tp=trde_qty_tp, crd_cnd=crd_cnd,
            updown_incls=updown_incls, dt=dt, stex_tp=stex_tp, **kw,
        )

    async def upper_lower_limit(
        self,
        mrkt_tp: str = "000", updown_tp: str = "1", sort_tp: str = "1",
        stk_cnd: str = "0", trde_qty_tp: str = "00000", crd_cnd: str = "0",
        trde_gold_tp: str = "0", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10017 — 상하한가요청

        Args:
            mrkt_tp: 시장구분 (000:전체, 001:코스피, 101:코스닥)
            updown_tp: 상하한구분 (1:상한, 2:상승, 3:보합, 4:하한, 5:하락, 6:전일상한, 7:전일하한)
            sort_tp: 정렬구분 (1:종목코드순, 2:연속횟수순, 3:등락률순)
            stk_cnd: 종목조건 (0:전체, 1:관리종목제외, ...)
            trde_qty_tp: 거래량구분 (00000:전체, ...)
            crd_cnd: 신용조건 (0:전체, ...)
            trde_gold_tp: 매매금구분 (0:전체, ...)
            stex_tp: 거래소구분 (1:KRX, 2:NXT, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10017",
            mrkt_tp=mrkt_tp, updown_tp=updown_tp, sort_tp=sort_tp,
            stk_cnd=stk_cnd, trde_qty_tp=trde_qty_tp, crd_cnd=crd_cnd,
            trde_gold_tp=trde_gold_tp, stex_tp=stex_tp, **kw,
        )

    async def near_high_low(
        self,
        high_low_tp: str = "1", alacc_rt: str = "10",
        mrkt_tp: str = "000", trde_qty_tp: str = "00000",
        stk_cnd: str = "0", crd_cnd: str = "0", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10018 — 고저가근접요청

        Args:
            high_low_tp: 고저구분 (1:고가, 2:저가)
            alacc_rt: 근접율 (05, 10, 15, 20, 25, 30)
            mrkt_tp: 시장구분 (000:전체, 001:코스피, 101:코스닥)
            trde_qty_tp: 거래량구분 (00000:전체, ...)
            stk_cnd: 종목조건 (0:전체, ...)
            crd_cnd: 신용조건 (0:전체, ...)
            stex_tp: 거래소구분 (1:KRX, 2:NXT, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10018",
            high_low_tp=high_low_tp, alacc_rt=alacc_rt,
            mrkt_tp=mrkt_tp, trde_qty_tp=trde_qty_tp,
            stk_cnd=stk_cnd, crd_cnd=crd_cnd, stex_tp=stex_tp, **kw,
        )

    async def rapid_price_change(
        self,
        mrkt_tp: str = "000", flu_tp: str = "1", tm_tp: str = "1", tm: str = "10",
        trde_qty_tp: str = "00000", stk_cnd: str = "0", crd_cnd: str = "0",
        pric_cnd: str = "0", updown_incls: str = "0", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10019 — 가격급등락요청

        Args:
            mrkt_tp: 시장구분 (000:전체, 001:코스피, 101:코스닥)
            flu_tp: 등락구분 (1:급등, 2:급락)
            tm_tp: 시간구분 (1:분전, 2:일전)
            tm: 시간 (분 또는 일 입력)
            trde_qty_tp: 거래량구분 (00000:전체, ...)
            stk_cnd: 종목조건 (0:전체, ...)
            crd_cnd: 신용조건 (0:전체, ...)
            pric_cnd: 가격조건 (0:전체, ...)
            updown_incls: 상하한포함 (0:미포함, 1:포함)
            stex_tp: 거래소구분 (1:KRX, 2:NXT, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10019",
            mrkt_tp=mrkt_tp, flu_tp=flu_tp, tm_tp=tm_tp, tm=tm,
            trde_qty_tp=trde_qty_tp, stk_cnd=stk_cnd, crd_cnd=crd_cnd,
            pric_cnd=pric_cnd, updown_incls=updown_incls, stex_tp=stex_tp, **kw,
        )

    async def trading_volume_update(
        self,
        mrkt_tp: str = "000", cycle_tp: str = "20",
        trde_qty_tp: str = "10", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10024 — 거래량갱신요청

        Args:
            mrkt_tp: 시장구분 (000:전체, 001:코스피, 101:코스닥)
            cycle_tp: 주기구분 (5:5일, 10:10일, 20:20일, 60:60일, 250:250일)
            trde_qty_tp: 거래량구분 (5:5천주이상, 10:만주이상, ...)
            stex_tp: 거래소구분 (1:KRX, 2:NXT, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10024",
            mrkt_tp=mrkt_tp, cycle_tp=cycle_tp,
            trde_qty_tp=trde_qty_tp, stex_tp=stex_tp, **kw,
        )

    async def volume_concentration(
        self, stk_cd: str,
        mrkt_tp: str = "000", prps_cnctr_rt: str = "80",
        cur_prc_entry: str = "0", prpscnt: str = "5",
        cycle_tp: str = "250", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10025 — 매물대집중요청

        Args:
            stk_cd: 종목코드
            mrkt_tp: 시장구분 (000:전체, 001:코스피, 101:코스닥)
            prps_cnctr_rt: 매물집중비율 (0~100)
            cur_prc_entry: 현재가진입 (0:미포함, 1:포함)
            prpscnt: 매물대수
            cycle_tp: 주기구분 (50:50일, 100:100일, 150:150일, 200:200일, 250:250일, 300:300일)
            stex_tp: 거래소구분 (1:KRX, 2:NXT, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10025",
            stk_cd=stk_cd, mrkt_tp=mrkt_tp, prps_cnctr_rt=prps_cnctr_rt,
            cur_prc_entry=cur_prc_entry, prpscnt=prpscnt,
            cycle_tp=cycle_tp, stex_tp=stex_tp, **kw,
        )

    async def high_low_per(self, pertp: str = "3", stex_tp: str = "3", **kw: Any) -> dict[str, Any]:
        """ka10026 — 고저PER요청

        Args:
            pertp: PER구분 (1:저PBR, 2:고PBR, 3:저PER, 4:고PER, 5:저ROE, 6:高ROE)
            stex_tp: 거래소구분 (1:KRX, 2:NXT, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10026",
            pertp=pertp, stex_tp=stex_tp, **kw,
        )

    async def change_rate_vs_opening(
        self,
        sort_tp: str = "1", trde_qty_cnd: str = "0000", mrkt_tp: str = "000",
        updown_incls: str = "0", stk_cnd: str = "0", crd_cnd: str = "0",
        trde_prica_cnd: str = "0", flu_cnd: str = "1", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10028 — 시가대비등락률요청

        Args:
            sort_tp: 정렬구분 (1:시가, 2:고가, 3:저가, 4:기준가)
            trde_qty_cnd: 거래량조건 (0000:전체, ...)
            mrkt_tp: 시장구분 (000:전체, 001:코스피, 101:코스닥)
            updown_incls: 상하한포함 (0:불포함, 1:포함)
            stk_cnd: 종목조건 (0:전체, ...)
            crd_cnd: 신용조건 (0:전체, ...)
            trde_prica_cnd: 거래대금조건 (0:전체, ...)
            flu_cnd: 등락조건 (1:상위, 2:하위)
            stex_tp: 거래소구분 (1:KRX, 2:NXT, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10028",
            sort_tp=sort_tp, trde_qty_cnd=trde_qty_cnd, mrkt_tp=mrkt_tp,
            updown_incls=updown_incls, stk_cnd=stk_cnd, crd_cnd=crd_cnd,
            trde_prica_cnd=trde_prica_cnd, flu_cnd=flu_cnd, stex_tp=stex_tp, **kw,
        )

    async def trading_agent_supply_demand(
        self,
        stk_cd: str, strt_dt: str, end_dt: str,
        qry_dt_tp: str = "0", pot_tp: str = "0", dt: str = "20",
        sort_base: str = "1", mmcm_cd: str = "", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10043 — 거래원매물대분석요청

        Args:
            stk_cd: 종목코드
            strt_dt: 시작일자 (YYYYMMDD)
            end_dt: 종료일자 (YYYYMMDD)
            qry_dt_tp: 조회기간구분 (0:기간으로, 1:시작일자/종료일자로)
            pot_tp: 시점구분 (0:당일, 1:전일)
            dt: 기간 (5:5일, 10:10일, 20:20일, 40:40일, 60:60일, 120:120일)
            sort_base: 정렬기준 (1:종가순, 2:날짜순)
            mmcm_cd: 회원사코드 (ka10102 조회)
            stex_tp: 거래소구분 (1:KRX, 2:NXT, 3:통합)
        """
        params: dict[str, Any] = dict(
            stk_cd=stk_cd, strt_dt=strt_dt, end_dt=end_dt,
            qry_dt_tp=qry_dt_tp, pot_tp=pot_tp, dt=dt,
            sort_base=sort_base, stex_tp=stex_tp, **kw,
        )
        if mmcm_cd:
            params["mmcm_cd"] = mmcm_cd
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10043", **params)

    async def trading_agent_instant_volume(
        self,
        mmcm_cd: str, mrkt_tp: str = "0",
        qty_tp: str = "0", pric_tp: str = "0", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10052 — 거래원순간거래량요청

        Args:
            mmcm_cd: 회원사코드 (ka10102 조회)
            mrkt_tp: 시장구분 (0:전체, 1:코스피, 2:코스닥, 3:종목)
            qty_tp: 수량구분 (0:전체, 1:1000주, ...)
            pric_tp: 가격구분 (0:전체, ...)
            stex_tp: 거래소구분 (1:KRX, 2:NXT, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10052",
            mmcm_cd=mmcm_cd, mrkt_tp=mrkt_tp,
            qty_tp=qty_tp, pric_tp=pric_tp, stex_tp=stex_tp, **kw,
        )

    async def vi_triggered_stocks(
        self,
        mrkt_tp: str = "000", bf_mkrt_tp: str = "0", motn_tp: str = "0",
        skip_stk: str = "000000000", trde_qty_tp: str = "0",
        min_trde_qty: str = "", max_trde_qty: str = "",
        trde_prica_tp: str = "0", min_trde_prica: str = "",
        max_trde_prica: str = "", motn_drc: str = "0", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10054 — 변동성완화장치(VI) 발동종목요청

        Args:
            mrkt_tp: 시장구분 (000:전체, 001:코스피, 101:코스닥)
            bf_mkrt_tp: 장전구분 (0:전체, 1:정규시장, 2:시간외단일가)
            motn_tp: 발동구분 (0:전체, 1:정적VI, 2:동적VI, 3:동적VI+정적VI)
            skip_stk: 제외종목 (9자리, 0=포함, 1=제외)
            trde_qty_tp: 거래량구분 (0:사용안함, 1:사용)
            min_trde_qty: 최소거래량
            max_trde_qty: 최대거래량
            trde_prica_tp: 거래대금구분 (0:사용안함, 1:사용)
            min_trde_prica: 최소거래대금
            max_trde_prica: 최대거래대금
            motn_drc: 발동방향 (0:전체, 1:상승, 2:하락)
            stex_tp: 거래소구분 (1:KRX, 2:NXT, 3:통합)
        """
        params: dict[str, Any] = dict(
            mrkt_tp=mrkt_tp, bf_mkrt_tp=bf_mkrt_tp, motn_tp=motn_tp,
            skip_stk=skip_stk, trde_qty_tp=trde_qty_tp,
            trde_prica_tp=trde_prica_tp, motn_drc=motn_drc,
            stex_tp=stex_tp, **kw,
        )
        if min_trde_qty:
            params["min_trde_qty"] = min_trde_qty
        if max_trde_qty:
            params["max_trde_qty"] = max_trde_qty
        if min_trde_prica:
            params["min_trde_prica"] = min_trde_prica
        if max_trde_prica:
            params["max_trde_prica"] = max_trde_prica
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10054", **params)

    async def today_vs_yesterday_volume(
        self, stk_cd: str, tdy_pred: str = "1", **kw: Any,
    ) -> dict[str, Any]:
        """ka10055 — 당일전일체결량요청

        Args:
            stk_cd: 종목코드
            tdy_pred: 당일전일 (1:당일, 2:전일)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10055",
            stk_cd=stk_cd, tdy_pred=tdy_pred, **kw,
        )

    async def daily_trading_by_investor(
        self,
        strt_dt: str, end_dt: str, trde_tp: str = "1",
        mrkt_tp: str = "001", invsr_tp: str = "8000", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10058 — 투자자별일별매매종목요청

        Args:
            strt_dt: 시작일자 (YYYYMMDD)
            end_dt: 종료일자 (YYYYMMDD)
            trde_tp: 매매구분 (1:순매도, 2:순매수)
            mrkt_tp: 시장구분 (001:코스피, 101:코스닥)
            invsr_tp: 투자자구분 (8000:개인, 9000:외국인, 1000:금융투자, ...)
            stex_tp: 거래소구분 (1:KRX, 2:NXT, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10058",
            strt_dt=strt_dt, end_dt=end_dt, trde_tp=trde_tp,
            mrkt_tp=mrkt_tp, invsr_tp=invsr_tp, stex_tp=stex_tp, **kw,
        )

    async def investor_institution_by_stock(
        self,
        dt: str, stk_cd: str, amt_qty_tp: str = "1",
        trde_tp: str = "0", unit_tp: str = "1000",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10059 — 종목별투자자기관별요청

        Args:
            dt: 일자 (YYYYMMDD)
            stk_cd: 종목코드
            amt_qty_tp: 금액수량구분 (1:금액, 2:수량)
            trde_tp: 매매구분 (0:순매수, 1:매수, 2:매도)
            unit_tp: 단위구분 (1000:천주, 1:단주)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10059",
            dt=dt, stk_cd=stk_cd, amt_qty_tp=amt_qty_tp,
            trde_tp=trde_tp, unit_tp=unit_tp, **kw,
        )

    async def investor_institution_aggregate(
        self,
        stk_cd: str, strt_dt: str, end_dt: str,
        amt_qty_tp: str = "1", trde_tp: str = "0", unit_tp: str = "1000",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10061 — 종목별투자자기관별합계요청

        Args:
            stk_cd: 종목코드
            strt_dt: 시작일자 (YYYYMMDD)
            end_dt: 종료일자 (YYYYMMDD)
            amt_qty_tp: 금액수량구분 (1:금액, 2:수량)
            trde_tp: 매매구분 (0:순매수)
            unit_tp: 단위구분 (1000:천주, 1:단주)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10061",
            stk_cd=stk_cd, strt_dt=strt_dt, end_dt=end_dt,
            amt_qty_tp=amt_qty_tp, trde_tp=trde_tp, unit_tp=unit_tp, **kw,
        )

    async def today_vs_yesterday_execution(
        self, stk_cd: str, tdy_pred: str = "1", tic_min: str = "0", **kw: Any,
    ) -> dict[str, Any]:
        """ka10084 — 당일전일체결요청

        Args:
            stk_cd: 종목코드
            tdy_pred: 당일전일 (1:당일, 2:전일)
            tic_min: 틱분 (0:틱, 1:분)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10084",
            stk_cd=stk_cd, tdy_pred=tdy_pred, tic_min=tic_min, **kw,
        )

    async def watchlist_stock_info(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10095 — 관심종목정보요청

        Args:
            stk_cd: 종목코드 (여러개시 | 로 구분)
        """
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10095", stk_cd=stk_cd, **kw)

    async def stock_list(self, mrkt_tp: str = "0", **kw: Any) -> dict[str, Any]:
        """ka10099 — 종목정보리스트

        Args:
            mrkt_tp: 시장구분 (0:코스피, 10:코스닥, 30:K-OTC, 50:코넥스, 60:ETN)
        """
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10099", mrkt_tp=mrkt_tp, **kw)

    async def search_stock(self, keyword: str, **kw: Any) -> dict[str, Any]:
        """ka10100 — 종목정보조회

        Args:
            keyword: 종목코드 또는 종목명
        """
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10100", stk_cd=keyword, **kw)

    async def industry_code_list(self, mrkt_tp: str = "0", **kw: Any) -> dict[str, Any]:
        """ka10101 — 업종코드리스트

        Args:
            mrkt_tp: 시장구분 (0:코스피, 1:코스닥, 2:KOSPI200, 4:KOSPI100, 7:KRX100)
        """
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10101", mrkt_tp=mrkt_tp, **kw)

    async def member_company_list(self, **kw: Any) -> dict[str, Any]:
        """ka10102 — 회원사리스트"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10102", **kw)

    async def realtime_stock_inquiry_rank(self, qry_tp: str = "1", **kw: Any) -> dict[str, Any]:
        """ka00198 — 실시간종목조회순위

        Args:
            qry_tp: 구분 (1:1분, 2:10분, 3:1시간, 4:당일누적, 5:30초)
        """
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka00198", qry_tp=qry_tp, **kw)

    # ── 시세/호가 (/api/dostk/mrkcond) ────────────

    async def quote(self, stk_cd: str) -> dict[str, Any]:
        """ka10004 — 주식호가요청 (매수/매도 10호가)

        Args:
            stk_cd: 종목코드
        """
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka10004", stk_cd=stk_cd)

    async def stock_daily_weekly_monthly(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10005 — 주식일주월시분요청

        Args:
            stk_cd: 종목코드
        """
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka10005", stk_cd=stk_cd, **kw)

    async def stock_minute_price(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10006 — 주식시분요청

        Args:
            stk_cd: 종목코드
        """
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka10006", stk_cd=stk_cd, **kw)

    async def order_book_info(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10007 — 시세표성정보요청

        Args:
            stk_cd: 종목코드
        """
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka10007", stk_cd=stk_cd, **kw)

    async def rights_issue_price(self, stk_cd: str, newstk_recvrht_tp: str = "00", **kw: Any) -> dict[str, Any]:
        """ka10011 — 신주인수권전체시세요청

        Args:
            stk_cd: 종목코드
            newstk_recvrht_tp: 신주인수권구분 (00:전체, 05:신주인수권증권, 07:신주인수권증서)
        """
        return await self._client.get(
            "/api/dostk/mrkcond", tr_id="ka10011",
            stk_cd=stk_cd, newstk_recvrht_tp=newstk_recvrht_tp, **kw,
        )

    async def daily_institutional_trading(
        self,
        strt_dt: str, end_dt: str, trde_tp: str = "1",
        mrkt_tp: str = "001", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10044 — 일별기관매매종목요청

        Args:
            strt_dt: 시작일자 (YYYYMMDD)
            end_dt: 종료일자 (YYYYMMDD)
            trde_tp: 매매구분 (1:순매도, 2:순매수)
            mrkt_tp: 시장구분 (001:코스피, 101:코스닥)
            stex_tp: 거래소구분 (1:KRX, 2:NXT, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/mrkcond", tr_id="ka10044",
            strt_dt=strt_dt, end_dt=end_dt, trde_tp=trde_tp,
            mrkt_tp=mrkt_tp, stex_tp=stex_tp, **kw,
        )

    async def institutional_trading_trend(
        self,
        stk_cd: str, strt_dt: str, end_dt: str,
        orgn_prsm_unp_tp: str = "1", for_prsm_unp_tp: str = "1",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10045 — 종목별기관매매추이요청

        Args:
            stk_cd: 종목코드
            strt_dt: 시작일자 (YYYYMMDD)
            end_dt: 종료일자 (YYYYMMDD)
            orgn_prsm_unp_tp: 기관추정단가구분 (1:매수단가, 2:매도단가)
            for_prsm_unp_tp: 외인추정단가구분 (1:매수단가, 2:매도단가)
        """
        return await self._client.get(
            "/api/dostk/mrkcond", tr_id="ka10045",
            stk_cd=stk_cd, strt_dt=strt_dt, end_dt=end_dt,
            orgn_prsm_unp_tp=orgn_prsm_unp_tp, for_prsm_unp_tp=for_prsm_unp_tp, **kw,
        )

    async def hourly_execution_strength(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10046 — 체결강도추이시간별요청

        Args:
            stk_cd: 종목코드
        """
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka10046", stk_cd=stk_cd, **kw)

    async def daily_execution_strength(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10047 — 체결강도추이일별요청

        Args:
            stk_cd: 종목코드
        """
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka10047", stk_cd=stk_cd, **kw)

    async def intraday_investor_trading(
        self,
        mrkt_tp: str = "000", amt_qty_tp: str = "1",
        invsr: str = "7", frgn_all: str = "0", smtm_netprps_tp: str = "0",
        stex_tp: str = "3", **kw: Any,
    ) -> dict[str, Any]:
        """ka10063 — 장중투자자별매매요청

        Args:
            mrkt_tp: 시장구분 (000:전체, 001:코스피, 101:코스닥)
            amt_qty_tp: 금액수량구분 (1:금액&수량)
            invsr: 투자자별 (6:외국인, 7:기관계, 1:투신, ...)
            frgn_all: 외국계전체 (1:체크, 0:미체크)
            smtm_netprps_tp: 동시순매수구분 (1:체크, 0:미체크)
            stex_tp: 거래소구분 (1:KRX, 2:NXT, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/mrkcond", tr_id="ka10063",
            mrkt_tp=mrkt_tp, amt_qty_tp=amt_qty_tp,
            invsr=invsr, frgn_all=frgn_all, smtm_netprps_tp=smtm_netprps_tp,
            stex_tp=stex_tp, **kw,
        )

    async def after_hours_investor_trading(
        self,
        mrkt_tp: str = "000", amt_qty_tp: str = "1",
        trde_tp: str = "0", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10066 — 장마감후투자자별매매요청

        Args:
            mrkt_tp: 시장구분 (000:전체, 001:코스피, 101:코스닥)
            amt_qty_tp: 금액수량구분 (1:금액, 2:수량)
            trde_tp: 매매구분 (0:순매수, 1:매수, 2:매도)
            stex_tp: 거래소구분 (1:KRX, 2:NXT, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/mrkcond", tr_id="ka10066",
            mrkt_tp=mrkt_tp, amt_qty_tp=amt_qty_tp,
            trde_tp=trde_tp, stex_tp=stex_tp, **kw,
        )

    async def broker_stock_trading_trend(
        self,
        mmcm_cd: str, stk_cd: str, strt_dt: str, end_dt: str,
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10078 — 증권사별종목매매동향요청

        Args:
            mmcm_cd: 회원사코드 (ka10102 조회)
            stk_cd: 종목코드
            strt_dt: 시작일자 (YYYYMMDD)
            end_dt: 종료일자 (YYYYMMDD)
        """
        return await self._client.get(
            "/api/dostk/mrkcond", tr_id="ka10078",
            mmcm_cd=mmcm_cd, stk_cd=stk_cd,
            strt_dt=strt_dt, end_dt=end_dt, **kw,
        )

    async def daily_price(
        self, stk_cd: str, qry_dt: str, indc_tp: str = "0", **kw: Any,
    ) -> dict[str, Any]:
        """ka10086 — 일별주가요청

        Args:
            stk_cd: 종목코드
            qry_dt: 조회일자 (YYYYMMDD)
            indc_tp: 표시구분 (0:수량, 1:금액(백만원))
        """
        return await self._client.get(
            "/api/dostk/mrkcond", tr_id="ka10086",
            stk_cd=stk_cd, qry_dt=qry_dt, indc_tp=indc_tp, **kw,
        )

    async def after_hours_single_price(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10087 — 시간외단일가요청

        Args:
            stk_cd: 종목코드
        """
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka10087", stk_cd=stk_cd, **kw)

    async def program_trading_by_time(
        self,
        date: str, amt_qty_tp: str = "1",
        mrkt_tp: str = "P00101", min_tic_tp: str = "0", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka90005 — 프로그램매매추이요청 (시간대별)

        Args:
            date: 날짜 (YYYYMMDD)
            amt_qty_tp: 금액수량구분 (1:금액(백만원), 2:수량(천주))
            mrkt_tp: 시장구분 (P00101:코스피, P10102:코스닥)
            min_tic_tp: 분틱구분 (0:틱, 1:분)
            stex_tp: 거래소구분 (1:KRX, 2:NXT, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/mrkcond", tr_id="ka90005",
            date=date, amt_qty_tp=amt_qty_tp,
            mrkt_tp=mrkt_tp, min_tic_tp=min_tic_tp, stex_tp=stex_tp, **kw,
        )

    async def program_arbitrage_balance(self, date: str, stex_tp: str = "3", **kw: Any) -> dict[str, Any]:
        """ka90006 — 프로그램매매차익잔고추이요청

        Args:
            date: 날짜 (YYYYMMDD)
            stex_tp: 거래소구분 (1:KRX, 2:NXT, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/mrkcond", tr_id="ka90006",
            date=date, stex_tp=stex_tp, **kw,
        )

    async def cumulative_program_trading(
        self,
        date: str, amt_qty_tp: str = "1",
        mrkt_tp: str = "0", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka90007 — 프로그램매매누적추이요청

        Args:
            date: 날짜 (YYYYMMDD, 종료일기준 1년간)
            amt_qty_tp: 금액수량구분 (1:금액, 2:수량)
            mrkt_tp: 시장구분 (0:코스피, 1:코스닥)
            stex_tp: 거래소구분 (1:KRX, 2:NXT, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/mrkcond", tr_id="ka90007",
            date=date, amt_qty_tp=amt_qty_tp,
            mrkt_tp=mrkt_tp, stex_tp=stex_tp, **kw,
        )

    async def program_trading_by_stock_time(
        self,
        amt_qty_tp: str = "1", stk_cd: str = "", date: str = "",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka90008 — 종목시간별프로그램매매추이요청

        Args:
            amt_qty_tp: 금액수량구분 (1:금액, 2:수량)
            stk_cd: 종목코드
            date: 날짜 (YYYYMMDD)
        """
        return await self._client.get(
            "/api/dostk/mrkcond", tr_id="ka90008",
            amt_qty_tp=amt_qty_tp, stk_cd=stk_cd, date=date, **kw,
        )

    async def program_trading_by_date(
        self,
        date: str, amt_qty_tp: str = "1",
        mrkt_tp: str = "P00101", min_tic_tp: str = "0", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka90010 — 프로그램매매추이요청 (일자별)

        Args:
            date: 날짜 (YYYYMMDD)
            amt_qty_tp: 금액수량구분 (1:금액(백만원), 2:수량(천주))
            mrkt_tp: 시장구분 (P00101:코스피, P10102:코스닥)
            min_tic_tp: 분틱구분 (0:틱, 1:분)
            stex_tp: 거래소구분 (1:KRX, 2:NXT, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/mrkcond", tr_id="ka90010",
            date=date, amt_qty_tp=amt_qty_tp,
            mrkt_tp=mrkt_tp, min_tic_tp=min_tic_tp, stex_tp=stex_tp, **kw,
        )

    async def program_trading_by_stock(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka90004 — 종목별프로그램매매현황요청

        Args:
            stk_cd: 종목코드
        """
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka90004", stk_cd=stk_cd, **kw)

    async def program_buy_top50(
        self,
        trde_upper_tp: str = "1", amt_qty_tp: str = "1",
        mrkt_tp: str = "P00101", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka90003 — 프로그램순매수상위50요청

        Args:
            trde_upper_tp: 매매상위구분 (1:순매도상위, 2:순매수상위)
            amt_qty_tp: 금액수량구분 (1:금액, 2:수량)
            mrkt_tp: 시장구분 (P00101:코스피, P10102:코스닥)
            stex_tp: 거래소구분 (1:KRX, 2:NXT, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka90003",
            trde_upper_tp=trde_upper_tp, amt_qty_tp=amt_qty_tp,
            mrkt_tp=mrkt_tp, stex_tp=stex_tp, **kw,
        )

    async def program_trading_by_stock_day(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka90013 — 종목일별프로그램매매추이요청

        Args:
            stk_cd: 종목코드
        """
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka90013", stk_cd=stk_cd, **kw)
