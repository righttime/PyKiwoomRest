"""ETF — /api/dostk/stkinfo"""

from __future__ import annotations

from typing import Any

from .client import KiwoomClient


class EtfAPI:
    """ETF 관련 API"""

    def __init__(self, client: KiwoomClient) -> None:
        self._client = client

    async def return_rate(
        self, stk_cd: str, etfobjt_idex_cd: str = "", dt: str = "0", **kw: Any,
    ) -> dict[str, Any]:
        """ka40001 — ETF수익율요청

        Args:
            stk_cd: 종목코드
            etfobjt_idex_cd: ETF지수코드
            dt: 일자구분 (0)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka40001",
            stk_cd=stk_cd, etfobjt_idex_cd=etfobjt_idex_cd, dt=dt, **kw,
        )

    async def stock_info(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka40002 — ETF종목정보요청

        Args:
            stk_cd: 종목코드
        """
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka40002", stk_cd=stk_cd, **kw)

    async def daily_trend(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka40003 — ETF일별추이요청

        Args:
            stk_cd: 종목코드
        """
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka40003", stk_cd=stk_cd, **kw)

    async def overall_market_price(
        self,
        txon_type: str = "0", navpre: str = "0",
        mngmcomp: str = "0000", txon_yn: str = "0",
        trace_idex: str = "0", stex_tp: str = "3",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka40004 — ETF전체시세요청

        Args:
            txon_type: 상장유형 (0)
            navpre: NAV구분 (0)
            mngmcomp: 운용사 (0000:전체)
            txon_yn: 상장여부 (0)
            trace_idex: 추종지수 (0)
            stex_tp: 거래소구분 (1:KRX, 3:통합)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka40004",
            txon_type=txon_type, navpre=navpre, mngmcomp=mngmcomp,
            txon_yn=txon_yn, trace_idex=trace_idex,
            stex_tp=stex_tp, **kw,
        )

    async def time_segment_trend(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka40006 — ETF시간대별추이요청

        Args:
            stk_cd: 종목코드
        """
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka40006", stk_cd=stk_cd, **kw)

    async def time_segment_execution(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka40007 — ETF시간대별체결요청

        Args:
            stk_cd: 종목코드
        """
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka40007", stk_cd=stk_cd, **kw)

    async def daily_execution(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka40008 — ETF일자별체결요청

        Args:
            stk_cd: 종목코드
        """
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka40008", stk_cd=stk_cd, **kw)

    async def time_nav(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka40009 — ETF시간대별NAV요청

        Args:
            stk_cd: 종목코드
        """
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka40009", stk_cd=stk_cd, **kw)

    async def time_trend(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka40010 — ETF시간대별추이요청

        Args:
            stk_cd: 종목코드
        """
        return await self._client.get("/api/dostk/stkinfo", tr_id="ka40010", stk_cd=stk_cd, **kw)
