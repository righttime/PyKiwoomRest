"""업종 정보 — /api/dostk/indtp"""

from __future__ import annotations

from typing import Any

from .client import KiwoomClient


class IndustryAPI:
    """업종 관련 API"""

    def __init__(self, client: KiwoomClient) -> None:
        self._client = client

    async def industry_program_trading(self, **kw: Any) -> dict[str, Any]:
        """ka10010 — 업종프로그램요청"""
        return await self._client.get("/api/dostk/indtp", tr_id="ka10010", **kw)

    async def industry_investor_net_buy(self, **kw: Any) -> dict[str, Any]:
        """ka10051 — 업종별투자자순매수요청"""
        return await self._client.get("/api/dostk/indtp", tr_id="ka10051", **kw)

    async def industry_current_price(self, **kw: Any) -> dict[str, Any]:
        """ka20001 — 업종현재가요청"""
        return await self._client.get("/api/dostk/indtp", tr_id="ka20001", **kw)

    async def industry_stock_price(self, **kw: Any) -> dict[str, Any]:
        """ka20002 — 업종별주가요청"""
        return await self._client.get("/api/dostk/indtp", tr_id="ka20002", **kw)

    async def all_industry_index(self, **kw: Any) -> dict[str, Any]:
        """ka20003 — 전업종지수요청"""
        return await self._client.get("/api/dostk/indtp", tr_id="ka20003", **kw)

    async def industry_daily_price(self, **kw: Any) -> dict[str, Any]:
        """ka20009 — 업종현재가일별요청"""
        return await self._client.get("/api/dostk/indtp", tr_id="ka20009", **kw)
