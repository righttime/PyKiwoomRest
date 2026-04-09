"""공매도 — /api/dostk/stkinfo"""

from __future__ import annotations

from typing import Any

from .client import KiwoomClient


class ShortSellingAPI:
    """공매도 API"""

    def __init__(self, client: KiwoomClient) -> None:
        self._client = client

    async def short_selling_trend(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10014 — 공매도추이요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka10014", stk_cd=stk_cd, **kw)
