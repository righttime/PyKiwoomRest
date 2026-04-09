"""대차거래 — /api/dostk/stkinfo"""

from __future__ import annotations

from typing import Any

from .client import KiwoomClient


class LendingAPI:
    """대차거래 API"""

    def __init__(self, client: KiwoomClient) -> None:
        self._client = client

    async def lending_trend(self, all_tp: str = "1", **kw: Any) -> dict[str, Any]:
        """ka10068 — 대차거래추이요청

        Args:
            all_tp: 전체구분 (1)
        """
        return await self._client.get("/api/dostk/slb", tr_id="ka10068", all_tp=all_tp, **kw)

    async def top10_lending(
        self, strt_dt: str, mrkt_tp: str = "001", end_dt: str = "", **kw: Any,
    ) -> dict[str, Any]:
        """ka10069 — 대차거래상위10종목요청

        Args:
            strt_dt: 시작일자 (YYYYMMDD)
            mrkt_tp: 시장구분 (001:코스피)
            end_dt: 종료일자 (YYYYMMDD, optional)
        """
        params: dict[str, Any] = {"strt_dt": strt_dt, "mrkt_tp": mrkt_tp, **kw}
        if end_dt:
            params["end_dt"] = end_dt
        return await self._client.get("/api/dostk/slb", tr_id="ka10069", **params)

    async def lending_trend_by_stock(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka20068 — 대차거래추이요청 (종목별)"""
        return await self._client.get("/api/dostk/slb", tr_id="ka20068", stk_cd=stk_cd, **kw)

    async def lending_details(self, **kw: Any) -> dict[str, Any]:
        """ka90012 — 대차거래내역요청"""
        return await self._client.get("/api/dostk/slb", tr_id="ka90012", **kw)
