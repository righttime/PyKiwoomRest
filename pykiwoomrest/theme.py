"""테마 — /api/dostk/stkinfo"""

from __future__ import annotations

from typing import Any

from .client import KiwoomClient


class ThemeAPI:
    """테마 관련 API"""

    def __init__(self, client: KiwoomClient) -> None:
        self._client = client

    async def theme_group_list(self, **kw: Any) -> dict[str, Any]:
        """ka90001 — 테마그룹별요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka90001", **kw)

    async def theme_component_stocks(self, **kw: Any) -> dict[str, Any]:
        """ka90002 — 테마구성종목요청"""
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka90002", **kw)
