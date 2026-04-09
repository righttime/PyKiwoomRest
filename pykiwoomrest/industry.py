"""업종 정보 — /api/dostk/sect"""

from __future__ import annotations

from typing import Any

from .client import KiwoomClient


class IndustryAPI:
    """업종 관련 API"""

    def __init__(self, client: KiwoomClient) -> None:
        self._client = client

    async def industry_program_trading(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10010 — 업종프로그램요청

        Args:
            stk_cd: 종목코드
        """
        return await self._client.get("/api/dostk/sect", tr_id="ka10010", stk_cd=stk_cd, **kw)

    async def industry_investor_net_buy(
        self,
        mrkt_tp: str = "0", amt_qty_tp: str = "1",
        stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10051 — 업종별투자자순매수요청

        Args:
            mrkt_tp: 시장구분 (0:코스피)
            amt_qty_tp: 금액수량구분 (1:금액)
            stex_tp: 거래소구분 (1:KRX, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/sect", tr_id="ka10051",
            mrkt_tp=mrkt_tp, amt_qty_tp=amt_qty_tp, stex_tp=stex_tp, **kw,
        )

    async def industry_current_price(
        self, mrkt_tp: str = "0", inds_cd: str = "001", **kw: Any,
    ) -> dict[str, Any]:
        """ka20001 — 업종현재가요청

        Args:
            mrkt_tp: 시장구분 (0:코스피)
            inds_cd: 업종코드 (001:종합KOSPI)
        """
        return await self._client.get(
            "/api/dostk/sect", tr_id="ka20001",
            mrkt_tp=mrkt_tp, inds_cd=inds_cd, **kw,
        )

    async def industry_stock_price(
        self,
        mrkt_tp: str = "0", inds_cd: str = "001",
        stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka20002 — 업종별주가요청

        Args:
            mrkt_tp: 시장구분 (0:코스피)
            inds_cd: 업종코드 (001:종합KOSPI)
            stex_tp: 거래소구분 (1:KRX, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/sect", tr_id="ka20002",
            mrkt_tp=mrkt_tp, inds_cd=inds_cd, stex_tp=stex_tp, **kw,
        )

    async def all_industry_index(self, inds_cd: str = "001", **kw: Any) -> dict[str, Any]:
        """ka20003 — 전업종지수요청

        Args:
            inds_cd: 업종코드 (001:종합KOSPI)
        """
        return await self._client.get("/api/dostk/sect", tr_id="ka20003", inds_cd=inds_cd, **kw)

    async def industry_daily_price(
        self, mrkt_tp: str = "0", inds_cd: str = "001", **kw: Any,
    ) -> dict[str, Any]:
        """ka20009 — 업종현재가일별요청

        Args:
            mrkt_tp: 시장구분 (0:코스피)
            inds_cd: 업종코드 (001:종합KOSPI)
        """
        return await self._client.get(
            "/api/dostk/sect", tr_id="ka20009",
            mrkt_tp=mrkt_tp, inds_cd=inds_cd, **kw,
        )
