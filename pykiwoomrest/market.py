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
        """ka10001 — 주식기본정보요청 (현재가, 전일대비, 등락률)"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10001", stk_cd=stk_cd)

    async def trading_agent(self, stk_cd: str) -> dict[str, Any]:
        """ka10002 — 주식거래원요청 (매수/매도 거래원)"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10002", stk_cd=stk_cd)

    # alias
    async def trade_volume_by_firm(self, stk_cd: str) -> dict[str, Any]:
        return await self.trading_agent(stk_cd)

    async def execution_info(self, stk_cd: str) -> dict[str, Any]:
        """ka10003 — 체결정보요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10003", stk_cd=stk_cd)

    async def credit_trading_trend(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10013 — 신용매매동향요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10013", stk_cd=stk_cd, **kw)

    async def daily_transaction_detail(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10015 — 일별거래상세요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10015", stk_cd=stk_cd, **kw)

    async def new_high_low(self, **kw: Any) -> dict[str, Any]:
        """ka10016 — 신고저가요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10016", **kw)

    async def upper_lower_limit(self, **kw: Any) -> dict[str, Any]:
        """ka10017 — 상하한가요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10017", **kw)

    async def near_high_low(self, **kw: Any) -> dict[str, Any]:
        """ka10018 — 고저가근접요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10018", **kw)

    async def rapid_price_change(self, **kw: Any) -> dict[str, Any]:
        """ka10019 — 가격급등락요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10019", **kw)

    async def trading_volume_update(self, **kw: Any) -> dict[str, Any]:
        """ka10024 — 거래량갱신요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10024", **kw)

    async def volume_concentration(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10025 — 매물대집중요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10025", stk_cd=stk_cd, **kw)

    async def high_low_per(self, **kw: Any) -> dict[str, Any]:
        """ka10026 — 고저PER요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10026", **kw)

    async def change_rate_vs_opening(self, **kw: Any) -> dict[str, Any]:
        """ka10028 — 시가대비등락률요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10028", **kw)

    async def trading_agent_supply_demand(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10043 — 거래원매물대분석요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10043", stk_cd=stk_cd, **kw)

    async def trading_agent_instant_volume(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10052 — 거래원순간거래량요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10052", stk_cd=stk_cd, **kw)

    async def vi_triggered_stocks(self, **kw: Any) -> dict[str, Any]:
        """ka10054 — 변동성완화장치(VI) 발동종목요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10054", **kw)

    async def today_vs_yesterday_volume(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10055 — 당일전일체결량요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10055", stk_cd=stk_cd, **kw)

    async def daily_trading_by_investor(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10058 — 투자자별일별매매종목요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10058", stk_cd=stk_cd, **kw)

    async def investor_institution_by_stock(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10059 — 종목별투자자기관별요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10059", stk_cd=stk_cd, **kw)

    async def investor_institution_aggregate(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10061 — 종목별투자자기관별합계요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10061", stk_cd=stk_cd, **kw)

    async def today_vs_yesterday_execution(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10084 — 당일전일체결요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10084", stk_cd=stk_cd, **kw)

    async def watchlist_stock_info(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10095 — 관심종목정보요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10095", stk_cd=stk_cd, **kw)

    async def stock_list(self, **kw: Any) -> dict[str, Any]:
        """ka10099 — 종목정보리스트"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10099", **kw)

    async def search_stock(self, keyword: str, **kw: Any) -> dict[str, Any]:
        """ka10100 — 종목정보조회"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10100", stk_nm=keyword, **kw)

    async def industry_code_list(self, **kw: Any) -> dict[str, Any]:
        """ka10101 — 업종코드리스트"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10101", **kw)

    async def member_company_list(self, **kw: Any) -> dict[str, Any]:
        """ka10102 — 회원사리스트"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10102", **kw)

    async def realtime_stock_inquiry_rank(self, **kw: Any) -> dict[str, Any]:
        """ka00198 — 실시간종목조회순위"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka00198", **kw)

    # ── 시세/호가 (/api/dostk/mrkcond) ────────────

    async def quote(self, stk_cd: str) -> dict[str, Any]:
        """ka10004 — 주식호가요청 (매수/매도 10호가)"""
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka10004", stk_cd=stk_cd)

    async def stock_daily_weekly_monthly(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10005 — 주식일주월시분요청"""
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka10005", stk_cd=stk_cd, **kw)

    async def stock_minute_price(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10006 — 주식시분요청"""
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka10006", stk_cd=stk_cd, **kw)

    async def order_book_info(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10007 — 시세표성정보요청"""
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka10007", stk_cd=stk_cd, **kw)

    async def rights_issue_price(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10011 — 신주인수권전체시세요청"""
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka10011", stk_cd=stk_cd, **kw)

    async def daily_institutional_trading(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10044 — 일별기관매매종목요청"""
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka10044", stk_cd=stk_cd, **kw)

    async def institutional_trading_trend(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10045 — 종목별기관매매추이요청"""
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka10045", stk_cd=stk_cd, **kw)

    async def hourly_execution_strength(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10046 — 체결강도추이시간별요청"""
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka10046", stk_cd=stk_cd, **kw)

    async def daily_execution_strength(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10047 — 체결강도추이일별요청"""
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka10047", stk_cd=stk_cd, **kw)

    async def intraday_investor_trading(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10063 — 장중투자자별매매요청"""
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka10063", stk_cd=stk_cd, **kw)

    async def after_hours_investor_trading(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10066 — 장마감후투자자별매매요청"""
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka10066", stk_cd=stk_cd, **kw)

    async def broker_stock_trading_trend(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10078 — 증권사별종목매매동향요청"""
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka10078", stk_cd=stk_cd, **kw)

    async def daily_price(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10086 — 일별주가요청"""
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka10086", stk_cd=stk_cd, **kw)

    async def after_hours_single_price(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10087 — 시간외단일가요청"""
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka10087", stk_cd=stk_cd, **kw)

    async def program_trading_by_time(self, **kw: Any) -> dict[str, Any]:
        """ka90005 — 프로그램매매추이요청 (시간대별)"""
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka90005", **kw)

    async def program_arbitrage_balance(self, **kw: Any) -> dict[str, Any]:
        """ka90006 — 프로그램매매차익잔고추이요청"""
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka90006", **kw)

    async def cumulative_program_trading(self, **kw: Any) -> dict[str, Any]:
        """ka90007 — 프로그램매매누적추이요청"""
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka90007", **kw)

    async def program_trading_by_stock_time(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka90008 — 종목시간별프로그램매매추이요청"""
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka90008", stk_cd=stk_cd, **kw)

    async def program_trading_by_date(self, **kw: Any) -> dict[str, Any]:
        """ka90010 — 프로그램매매추이요청 (일자별)"""
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka90010", **kw)

    async def program_trading_by_stock_day(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka90013 — 종목일별프로그램매매추이요청"""
        return await self._client.get("/api/dostk/mrkcond", tr_id="ka90013", stk_cd=stk_cd, **kw)

    async def program_buy_top50(self, **kw: Any) -> dict[str, Any]:
        """ka90003 — 프로그램순매수상위50요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka90003", **kw)

    async def program_trading_by_stock(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka90004 — 종목별프로그램매매현황요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka90004", stk_cd=stk_cd, **kw)
