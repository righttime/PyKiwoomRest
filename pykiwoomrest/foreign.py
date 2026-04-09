"""외국인/기관 매매동향 — /api/dostk/frgnistt"""

from __future__ import annotations

from typing import Any

from .client import KiwoomClient


class ForeignAPI:
    """외국인 & 기관 매매 API"""

    def __init__(self, client: KiwoomClient) -> None:
        self._client = client

    async def foreign_trade_by_stock(
        self,
        stk_cd: str, strt_dt: str, end_dt: str,
        orgn_prsm_unp_tp: str = "1", for_prsm_unp_tp: str = "1",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10008 — 외국인종목별매매동향

        Args:
            stk_cd: 종목코드
            strt_dt: 시작일자 (YYYYMMDD)
            end_dt: 종료일자 (YYYYMMDD)
            orgn_prsm_unp_tp: 기관추정단가구분 (1:매수단가)
            for_prsm_unp_tp: 외인추정단가구분 (1:매수단가)
        """
        return await self._client.get(
            "/api/dostk/frgnistt", tr_id="ka10008",
            stk_cd=stk_cd, strt_dt=strt_dt, end_dt=end_dt,
            orgn_prsm_unp_tp=orgn_prsm_unp_tp, for_prsm_unp_tp=for_prsm_unp_tp, **kw,
        )

    async def institution_trade(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10009 — 주식기관요청

        Args:
            stk_cd: 종목코드
        """
        return await self._client.get("/api/dostk/frgnistt", tr_id="ka10009", stk_cd=stk_cd, **kw)

    async def foreign_institution_rank(self, **kw: Any) -> dict[str, Any]:
        """ka90009 — 외국인기관매매상위요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka90009", **kw)

    async def consecutive_trading_status(
        self,
        dt: str = "1", mrkt_tp: str = "001",
        netslmt_tp: str = "2", stk_inds_tp: str = "0",
        amt_qty_tp: str = "0", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10131 — 기관외국인연속매매현황요청

        Args:
            dt: 일자구분 (1)
            mrkt_tp: 시장구분 (001:코스피)
            netslmt_tp: 순매매한도구분 (2)
            stk_inds_tp: 종목업종구분 (0)
            amt_qty_tp: 금액수량구분 (0)
            stex_tp: 거래소구분 (1:KRX, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/frgnistt", tr_id="ka10131",
            dt=dt, mrkt_tp=mrkt_tp, netslmt_tp=netslmt_tp,
            stk_inds_tp=stk_inds_tp, amt_qty_tp=amt_qty_tp,
            stex_tp=stex_tp, **kw,
        )
