"""공매도 — /api/dostk/stkinfo"""

from __future__ import annotations

from typing import Any

from .client import KiwoomClient


class ShortSellingAPI:
    """공매도 API"""

    def __init__(self, client: KiwoomClient) -> None:
        self._client = client

    async def short_selling_trend(
        self, stk_cd: str, strt_dt: str, end_dt: str, **kw: Any,
    ) -> dict[str, Any]:
        """ka10014 — 공매도추이요청

        Args:
            stk_cd: 종목코드
            strt_dt: 시작일자 (YYYYMMDD)
            end_dt: 종료일자 (YYYYMMDD)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10014",
            stk_cd=stk_cd, strt_dt=strt_dt, end_dt=end_dt, **kw,
        )
