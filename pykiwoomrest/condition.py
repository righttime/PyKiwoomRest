"""조건검색 — /api/dostk/stkinfo"""

from __future__ import annotations

from typing import Any

from .client import KiwoomClient


class ConditionAPI:
    """조건검색 API (영웅문4 조건 활용)"""

    def __init__(self, client: KiwoomClient) -> None:
        self._client = client

    async def condition_list(self, **kw: Any) -> dict[str, Any]:
        """ka10171 — 조건검색 목록조회"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10171", **kw)

    async def condition_search(self, **kw: Any) -> dict[str, Any]:
        """ka10172 — 조건검색 요청 (일반)"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10172", **kw)

    async def condition_search_realtime(self, **kw: Any) -> dict[str, Any]:
        """ka10173 — 조건검색 요청 (실시간)"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10173", **kw)

    async def condition_search_cancel(self, **kw: Any) -> dict[str, Any]:
        """ka10174 — 조건검색 실시간 해제"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10174", **kw)
