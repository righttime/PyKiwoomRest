"""순위 조회 (ka10020, ka10027, ka10030, ka10032 등)"""

from __future__ import annotations

from typing import Any

from .client import KiwoomClient


class RankAPI:
    """순위 조회 API"""

    def __init__(self, client: KiwoomClient) -> None:
        self._client = client

    async def volume_rank(self, **kwargs: Any) -> dict[str, Any]:
        """ka10030 - 당일거래량상위"""
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka10030", **kwargs
        )

    async def value_rank(self, **kwargs: Any) -> dict[str, Any]:
        """ka10032 - 거래대금상위"""
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka10032", **kwargs
        )

    async def change_rate_rank(self, **kwargs: Any) -> dict[str, Any]:
        """ka10027 - 등락률상위"""
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka10027", **kwargs
        )

    async def orderbook_rank(self, **kwargs: Any) -> dict[str, Any]:
        """ka10020 - 호가잔량상위"""
        return await self._client.get(
            "/api/dostk/rkinfo", tr_id="ka10020", **kwargs
        )
