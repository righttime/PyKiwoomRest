"""외국인/기관 매매동향 (ka10008, ka10009, ka90009)"""

from __future__ import annotations

from typing import Any

from .client import KiwoomClient


class ForeignAPI:
    """외국인 & 기관 API"""

    def __init__(self, client: KiwoomClient) -> None:
        self._client = client

    async def foreign_trade_by_stock(self, stk_cd: str, **kwargs: Any) -> dict[str, Any]:
        """ka10008 - 외국인종목별매매동향"""
        return await self._client.get(
            "/api/dostk/frgnistt", tr_id="ka10008", stk_cd=stk_cd, **kwargs
        )

    async def institution_trade(self, **kwargs: Any) -> dict[str, Any]:
        """ka10009 - 주식기관요청"""
        return await self._client.get(
            "/api/dostk/frgnistt", tr_id="ka10009", **kwargs
        )

    async def foreign_institution_rank(self, **kwargs: Any) -> dict[str, Any]:
        """ka90009 - 외국인기관매매상위"""
        return await self._client.get(
            "/api/dostk/frgnistt", tr_id="ka90009", **kwargs
        )
