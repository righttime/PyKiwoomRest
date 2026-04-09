"""ETF — /api/dostk/stkinfo"""

from __future__ import annotations

from typing import Any

from .client import KiwoomClient


class EtfAPI:
    """ETF 관련 API"""

    def __init__(self, client: KiwoomClient) -> None:
        self._client = client

    async def return_rate(self, **kw: Any) -> dict[str, Any]:
        """ka40001 — ETF수익율요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka40001", **kw)

    async def stock_info(self, **kw: Any) -> dict[str, Any]:
        """ka40002 — ETF종목정보요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka40002", **kw)

    async def daily_trend(self, **kw: Any) -> dict[str, Any]:
        """ka40003 — ETF일별추이요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka40003", **kw)

    async def overall_market_price(self, **kw: Any) -> dict[str, Any]:
        """ka40004 — ETF전체시세요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka40004", **kw)

    async def time_segment_trend(self, **kw: Any) -> dict[str, Any]:
        """ka40006 — ETF시간대별추이요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka40006", **kw)

    async def time_segment_execution(self, **kw: Any) -> dict[str, Any]:
        """ka40007 — ETF시간대별체결요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka40007", **kw)

    async def daily_execution(self, **kw: Any) -> dict[str, Any]:
        """ka40008 — ETF일자별체결요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka40008", **kw)

    async def time_nav(self, **kw: Any) -> dict[str, Any]:
        """ka40009 — ETF시간대별NAV요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka40009", **kw)

    async def time_trend(self, **kw: Any) -> dict[str, Any]:
        """ka40010 — ETF시간대별추이요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka40010", **kw)
