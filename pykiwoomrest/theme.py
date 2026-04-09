"""테마 — /api/dostk/stkinfo"""

from __future__ import annotations

from typing import Any

from .client import KiwoomClient


class ThemeAPI:
    """테마 관련 API"""

    def __init__(self, client: KiwoomClient) -> None:
        self._client = client

    async def theme_group_list(
        self,
        qry_tp: str = "0", date_tp: str = "0",
        flu_pl_amt_tp: str = "1", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka90001 — 테마그룹별요청

        Args:
            qry_tp: 조회구분 (0)
            date_tp: 일자구분 (0)
            flu_pl_amt_tp: 등락금액구분 (1)
            stex_tp: 거래소구분 (1:KRX, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka90001",
            qry_tp=qry_tp, date_tp=date_tp,
            flu_pl_amt_tp=flu_pl_amt_tp, stex_tp=stex_tp, **kw,
        )

    async def theme_component_stocks(
        self, thema_grp_cd: str, stex_tp: str = "3", **kw: Any,
    ) -> dict[str, Any]:
        """ka90002 — 테마구성종목요청

        Args:
            thema_grp_cd: 테마그룹코드
            stex_tp: 거래소구분 (1:KRX, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka90002",
            thema_grp_cd=thema_grp_cd, stex_tp=stex_tp, **kw,
        )
