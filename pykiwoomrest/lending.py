"""대차거래 — /api/dostk/stkinfo"""

from __future__ import annotations

from typing import Any

from .client import KiwoomClient


class LendingAPI:
    """대차거래 API"""

    def __init__(self, client: KiwoomClient) -> None:
        self._client = client

    async def lending_trend(self, **kw: Any) -> dict[str, Any]:
        """ka10068 — 대차거래추이요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10068", **kw)

    async def top10_lending(self, **kw: Any) -> dict[str, Any]:
        """ka10069 — 대차거래상위10종목요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10069", **kw)

    async def lending_trend_by_stock(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka20068 — 대차거래추이요청 (종목별)"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka20068", stk_cd=stk_cd, **kw)

    async def lending_details(self, **kw: Any) -> dict[str, Any]:
        """ka90012 — 대차거래내역요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka90012", **kw)
