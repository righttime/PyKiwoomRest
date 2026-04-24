"""시세/종목/차트 조회 (ka1xxxx TR)"""

from __future__ import annotations

from typing import Any

from .client import KiwoomClient


class MarketAPI:
    """시세 & 차트 API"""

    def __init__(self, client: KiwoomClient) -> None:
        self._client = client

    # ── 시세/종목 (stkinfo) ────────────────────────

    async def basic_info(self, stk_cd: str) -> dict[str, Any]:
        """ka10001 - 주식기본정보 (현재가, 전일대비, 등락률)"""
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10001", stk_cd=stk_cd
        )

    async def trade_volume_by_firm(self, stk_cd: str) -> dict[str, Any]:
        """ka10002 - 주식거래원 (매수/매도 거래원)"""
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10002", stk_cd=stk_cd
        )

    async def execution_info(self, stk_cd: str) -> dict[str, Any]:
        """ka10003 - 체결정보"""
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10003", stk_cd=stk_cd
        )

    async def daily_trade_detail(self, stk_cd: str) -> dict[str, Any]:
        """ka10015 - 일별거래상세"""
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10015", stk_cd=stk_cd
        )

    async def stock_list(self, mrkt_tp: str = "0") -> dict[str, Any]:
        """ka10099 - 종목정보리스트 (POST + special headers)
        mrkt_tp: '0'=KOSPI, '10'=KOSDAQ"""
        return await self._client.post_list(
            "/api/dostk/stkinfo",
            tr_id="ka10099",
            data={"mrkt_tp": mrkt_tp}
        )

    async def search_stock(self, keyword: str) -> dict[str, Any]:
        """ka10100 - 종목정보조회"""
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10100", stk_nm=keyword
        )

    # ── 차트 (chart) ───────────────────────────────

    async def tick_chart(self, stk_cd: str, **kwargs: Any) -> dict[str, Any]:
        """ka10079 - 틱차트"""
        return await self._client.get(
            "/api/dostk/chart", tr_id="ka10079", stk_cd=stk_cd, **kwargs
        )

    async def min_chart(self, stk_cd: str, **kwargs: Any) -> dict[str, Any]:
        """ka10080 - 분봉차트"""
        return await self._client.get(
            "/api/dostk/chart", tr_id="ka10080", stk_cd=stk_cd, **kwargs
        )

    async def day_chart(self, stk_cd: str, start_dt: str, end_dt: str, upd_stkpc_tp: str = "1", base_dt: str = "0") -> dict[str, Any]:
        """ka10081 - 일봉차트 (POST + post_list for pagination)
        Returns raw body dict with 'stk_dt_pole_chart_qry' key."""
        return await self._client.post_list(
            "/api/dostk/chart",
            tr_id="ka10081",
            data={
                "stk_cd": stk_cd,
                "start_dt": start_dt,
                "end_dt": end_dt,
                "upd_stkpc_tp": upd_stkpc_tp,
                "base_dt": base_dt,
            },
            list_key="stk_dt_pole_chart_qry",
        )

    async def week_chart(self, stk_cd: str, **kwargs: Any) -> dict[str, Any]:
        """ka10082 - 주봉차트 (POST required)"""
        return await self._client.post(
            "/api/dostk/chart", tr_id="ka10082",
            data={
                "stk_cd": stk_cd,
                **kwargs,
            }
        )

    async def month_chart(self, stk_cd: str, **kwargs: Any) -> dict[str, Any]:
        """ka10083 - 월봉차트 (POST required)"""
        return await self._client.post(
            "/api/dostk/chart", tr_id="ka10083",
            data={
                "stk_cd": stk_cd,
                **kwargs,
            }
        )

    async def year_chart(self, stk_cd: str, **kwargs: Any) -> dict[str, Any]:
        """ka10094 - 년봉차트 (POST required)"""
        return await self._client.post(
            "/api/dostk/chart", tr_id="ka10094",
            data={
                "stk_cd": stk_cd,
                **kwargs,
            }
        )

    # ── 시세/시장 (mrkcond) ────────────────────────

    async def quote(self, stk_cd: str) -> dict[str, Any]:
        """ka10004 - 주식호가 (매수/매도 호가)"""
        return await self._client.get(
            "/api/dostk/mrkcond", tr_id="ka10004", stk_cd=stk_cd
        )

    async def daily_price(self, stk_cd: str, **kwargs: Any) -> dict[str, Any]:
        """ka10086 - 일별주가 (과거 일별 주가)"""
        return await self._client.get(
            "/api/dostk/mrkcond", tr_id="ka10086", stk_cd=stk_cd, **kwargs
        )
