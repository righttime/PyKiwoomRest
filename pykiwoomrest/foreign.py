"""외국인/기관 매매동향 — /api/dostk/frgnistt"""

from __future__ import annotations

from typing import Any

from .client import KiwoomClient


class ForeignAPI:
    """외국인 & 기관 매매 API"""

    def __init__(self, client: KiwoomClient) -> None:
        self._client = client

    async def foreign_trade_by_stock(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10008 — 외국인종목별매매동향"""
        return await self._client.get("/api/dostk/frgnistt", tr_id="ka10008", stk_cd=stk_cd, **kw)

    async def institution_trade(self, **kw: Any) -> dict[str, Any]:
        """ka10009 — 주식기관요청"""
        return await self._client.get("/api/dostk/frgnistt", tr_id="ka10009", **kw)

    async def foreign_institution_rank(self, **kw: Any) -> dict[str, Any]:
        """ka90009 — 외국인기관매매상위요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka90009", **kw)

    async def consecutive_trading_status(self, **kw: Any) -> dict[str, Any]:
        """ka10131 — 기관외국인연속매매현황요청"""
        return await self._client.get("/api/dostk/frgnistt", tr_id="ka10131", **kw)
