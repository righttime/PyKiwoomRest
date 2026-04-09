"""차트 조회 — /api/dostk/chart"""

from __future__ import annotations

from typing import Any

from .client import KiwoomClient


class ChartAPI:
    """주식 & 업종 차트 API"""

    def __init__(self, client: KiwoomClient) -> None:
        self._client = client

    # ── 주식 차트 (/api/dostk/chart) ──────────────

    async def tick_chart(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10079 — 주식틱차트조회요청"""
        return await self._client.get("/api/dostk/chart", tr_id="ka10079", stk_cd=stk_cd, **kw)

    async def min_chart(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10080 — 주식분봉차트조회요청"""
        return await self._client.get("/api/dostk/chart", tr_id="ka10080", stk_cd=stk_cd, **kw)

    async def day_chart(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10081 — 주식일봉차트조회요청"""
        return await self._client.get("/api/dostk/chart", tr_id="ka10081", stk_cd=stk_cd, **kw)

    async def week_chart(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10082 — 주식주봉차트조회요청"""
        return await self._client.get("/api/dostk/chart", tr_id="ka10082", stk_cd=stk_cd, **kw)

    async def month_chart(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10083 — 주식월봉차트조회요청"""
        return await self._client.get("/api/dostk/chart", tr_id="ka10083", stk_cd=stk_cd, **kw)

    async def year_chart(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10094 — 주식년봉차트조회요청"""
        return await self._client.get("/api/dostk/chart", tr_id="ka10094", stk_cd=stk_cd, **kw)

    # aliases
    async def daily_chart(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        return await self.day_chart(stk_cd, **kw)

    async def weekly_chart(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        return await self.week_chart(stk_cd, **kw)

    async def monthly_chart(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        return await self.month_chart(stk_cd, **kw)

    async def yearly_chart(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        return await self.year_chart(stk_cd, **kw)

    # ── 투자자/기관 차트 (/api/dostk/chart) ───────

    async def investor_institution_chart(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10060 — 종목별투자자기관별차트요청"""
        return await self._client.get("/api/dostk/chart", tr_id="ka10060", stk_cd=stk_cd, **kw)

    async def intraday_investor_chart(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10064 — 장중투자자별매매차트요청"""
        return await self._client.get("/api/dostk/chart", tr_id="ka10064", stk_cd=stk_cd, **kw)

    # ── 업종 차트 (/api/dostk/chart) ──────────────

    async def industry_tick_chart(self, industry_cd: str, **kw: Any) -> dict[str, Any]:
        """ka20004 — 업종틱차트조회요청"""
        return await self._client.get("/api/dostk/chart", tr_id="ka20004", indu_cd=industry_cd, **kw)

    async def industry_minute_chart(self, industry_cd: str, **kw: Any) -> dict[str, Any]:
        """ka20005 — 업종분봉조회요청"""
        return await self._client.get("/api/dostk/chart", tr_id="ka20005", indu_cd=industry_cd, **kw)

    async def industry_daily_chart(self, industry_cd: str, **kw: Any) -> dict[str, Any]:
        """ka20006 — 업종일봉조회요청"""
        return await self._client.get("/api/dostk/chart", tr_id="ka20006", indu_cd=industry_cd, **kw)

    async def industry_weekly_chart(self, industry_cd: str, **kw: Any) -> dict[str, Any]:
        """ka20007 — 업종주봉조회요청"""
        return await self._client.get("/api/dostk/chart", tr_id="ka20007", indu_cd=industry_cd, **kw)

    async def industry_monthly_chart(self, industry_cd: str, **kw: Any) -> dict[str, Any]:
        """ka20008 — 업종월봉조회요청"""
        return await self._client.get("/api/dostk/chart", tr_id="ka20008", indu_cd=industry_cd, **kw)

    async def industry_yearly_chart(self, industry_cd: str, **kw: Any) -> dict[str, Any]:
        """ka20019 — 업종년봉조회요청"""
        return await self._client.get("/api/dostk/chart", tr_id="ka20019", indu_cd=industry_cd, **kw)
