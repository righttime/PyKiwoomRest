"""차트 조회 — /api/dostk/chart"""

from __future__ import annotations

from typing import Any

from .client import KiwoomClient


class ChartAPI:
    """주식 & 업종 차트 API"""

    def __init__(self, client: KiwoomClient) -> None:
        self._client = client

    # ── 주식 차트 (/api/dostk/chart) ──────────────

    async def tick_chart(
        self, stk_cd: str, tic_scope: str = "1", upd_stkpc_tp: str = "0", **kw: Any,
    ) -> dict[str, Any]:
        """ka10079 — 주식틱차트조회요청

        Args:
            stk_cd: 종목코드
            tic_scope: 틱범위 (1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱)
            upd_stkpc_tp: 수정주가구분 (0 or 1)
        """
        return await self._client.get(
            "/api/dostk/chart", tr_id="ka10079",
            stk_cd=stk_cd, tic_scope=tic_scope, upd_stkpc_tp=upd_stkpc_tp, **kw,
        )

    async def min_chart(
        self, stk_cd: str, tic_scope: str = "1", upd_stkpc_tp: str = "0", **kw: Any,
    ) -> dict[str, Any]:
        """ka10080 — 주식분봉차트조회요청

        Args:
            stk_cd: 종목코드
            tic_scope: 틱범위 (1:1분, 3:3분, 5:5분, 10:10분, 15:15분, 30:30분, 45:45분, 60:60분)
            upd_stkpc_tp: 수정주가구분 (0 or 1)
        """
        return await self._client.get(
            "/api/dostk/chart", tr_id="ka10080",
            stk_cd=stk_cd, tic_scope=tic_scope, upd_stkpc_tp=upd_stkpc_tp, **kw,
        )

    async def day_chart(
        self, stk_cd: str, base_dt: str, upd_stkpc_tp: str = "0", **kw: Any,
    ) -> dict[str, Any]:
        """ka10081 — 주식일봉차트조회요청

        Args:
            stk_cd: 종목코드
            base_dt: 기준일자 (YYYYMMDD)
            upd_stkpc_tp: 수정주가구분 (0 or 1)
        """
        return await self._client.get(
            "/api/dostk/chart", tr_id="ka10081",
            stk_cd=stk_cd, base_dt=base_dt, upd_stkpc_tp=upd_stkpc_tp, **kw,
        )

    async def week_chart(
        self, stk_cd: str, base_dt: str, upd_stkpc_tp: str = "0", **kw: Any,
    ) -> dict[str, Any]:
        """ka10082 — 주식주봉차트조회요청

        Args:
            stk_cd: 종목코드
            base_dt: 기준일자 (YYYYMMDD)
            upd_stkpc_tp: 수정주가구분 (0 or 1)
        """
        return await self._client.get(
            "/api/dostk/chart", tr_id="ka10082",
            stk_cd=stk_cd, base_dt=base_dt, upd_stkpc_tp=upd_stkpc_tp, **kw,
        )

    async def month_chart(
        self, stk_cd: str, base_dt: str, upd_stkpc_tp: str = "0", **kw: Any,
    ) -> dict[str, Any]:
        """ka10083 — 주식월봉차트조회요청

        Args:
            stk_cd: 종목코드
            base_dt: 기준일자 (YYYYMMDD)
            upd_stkpc_tp: 수정주가구분 (0 or 1)
        """
        return await self._client.get(
            "/api/dostk/chart", tr_id="ka10083",
            stk_cd=stk_cd, base_dt=base_dt, upd_stkpc_tp=upd_stkpc_tp, **kw,
        )

    async def year_chart(
        self, stk_cd: str, base_dt: str, upd_stkpc_tp: str = "0", **kw: Any,
    ) -> dict[str, Any]:
        """ka10094 — 주식년봉차트조회요청

        Args:
            stk_cd: 종목코드
            base_dt: 기준일자 (YYYYMMDD)
            upd_stkpc_tp: 수정주가구분 (0 or 1)
        """
        return await self._client.get(
            "/api/dostk/chart", tr_id="ka10094",
            stk_cd=stk_cd, base_dt=base_dt, upd_stkpc_tp=upd_stkpc_tp, **kw,
        )

    # aliases
    async def daily_chart(
        self, stk_cd: str, base_dt: str, upd_stkpc_tp: str = "0", **kw: Any,
    ) -> dict[str, Any]:
        return await self.day_chart(stk_cd, base_dt=base_dt, upd_stkpc_tp=upd_stkpc_tp, **kw)

    async def weekly_chart(
        self, stk_cd: str, base_dt: str, upd_stkpc_tp: str = "0", **kw: Any,
    ) -> dict[str, Any]:
        return await self.week_chart(stk_cd, base_dt=base_dt, upd_stkpc_tp=upd_stkpc_tp, **kw)

    async def monthly_chart(
        self, stk_cd: str, base_dt: str, upd_stkpc_tp: str = "0", **kw: Any,
    ) -> dict[str, Any]:
        return await self.month_chart(stk_cd, base_dt=base_dt, upd_stkpc_tp=upd_stkpc_tp, **kw)

    async def yearly_chart(
        self, stk_cd: str, base_dt: str, upd_stkpc_tp: str = "0", **kw: Any,
    ) -> dict[str, Any]:
        return await self.year_chart(stk_cd, base_dt=base_dt, upd_stkpc_tp=upd_stkpc_tp, **kw)

    # ── 투자자/기관 차트 (/api/dostk/chart) ───────

    async def investor_institution_chart(
        self,
        dt: str, stk_cd: str, amt_qty_tp: str = "1",
        trde_tp: str = "0", unit_tp: str = "1000",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10060 — 종목별투자자기관별차트요청

        Args:
            dt: 일자 (YYYYMMDD)
            stk_cd: 종목코드
            amt_qty_tp: 금액수량구분 (1:금액, 2:수량)
            trde_tp: 매매구분 (0:순매수, 1:매수, 2:매도)
            unit_tp: 단위구분 (1000:천주, 1:단주)
        """
        return await self._client.get(
            "/api/dostk/chart", tr_id="ka10060",
            dt=dt, stk_cd=stk_cd, amt_qty_tp=amt_qty_tp,
            trde_tp=trde_tp, unit_tp=unit_tp, **kw,
        )

    async def intraday_investor_chart(
        self,
        mrkt_tp: str = "000", amt_qty_tp: str = "1",
        trde_tp: str = "0", stk_cd: str = "",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10064 — 장중투자자별매매차트요청

        Args:
            mrkt_tp: 시장구분 (000:전체, 001:코스피, 101:코스닥)
            amt_qty_tp: 금액수량구분 (1:금액, 2:수량)
            trde_tp: 매매구분 (0:순매수, 1:매수, 2:매도)
            stk_cd: 종목코드
        """
        return await self._client.get(
            "/api/dostk/chart", tr_id="ka10064",
            mrkt_tp=mrkt_tp, amt_qty_tp=amt_qty_tp,
            trde_tp=trde_tp, stk_cd=stk_cd, **kw,
        )

    # ── 업종 차트 (/api/dostk/chart) ──────────────

    async def industry_tick_chart(
        self, industry_cd: str, tic_scope: str = "1", **kw: Any,
    ) -> dict[str, Any]:
        """ka20004 — 업종틱차트조회요청

        Args:
            industry_cd: 업종코드
            tic_scope: 틱범위 (1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱)
        """
        return await self._client.get(
            "/api/dostk/chart", tr_id="ka20004",
            indu_cd=industry_cd, tic_scope=tic_scope, **kw,
        )

    async def industry_minute_chart(
        self, industry_cd: str, tic_scope: str = "1", **kw: Any,
    ) -> dict[str, Any]:
        """ka20005 — 업종분봉조회요청

        Args:
            industry_cd: 업종코드
            tic_scope: 틱범위 (1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱)
        """
        return await self._client.get(
            "/api/dostk/chart", tr_id="ka20005",
            indu_cd=industry_cd, tic_scope=tic_scope, **kw,
        )

    async def industry_daily_chart(
        self, industry_cd: str, base_dt: str, **kw: Any,
    ) -> dict[str, Any]:
        """ka20006 — 업종일봉조회요청

        Args:
            industry_cd: 업종코드
            base_dt: 기준일자 (YYYYMMDD)
        """
        return await self._client.get(
            "/api/dostk/chart", tr_id="ka20006",
            indu_cd=industry_cd, base_dt=base_dt, **kw,
        )

    async def industry_weekly_chart(
        self, industry_cd: str, base_dt: str, **kw: Any,
    ) -> dict[str, Any]:
        """ka20007 — 업종주봉조회요청

        Args:
            industry_cd: 업종코드
            base_dt: 기준일자 (YYYYMMDD)
        """
        return await self._client.get(
            "/api/dostk/chart", tr_id="ka20007",
            indu_cd=industry_cd, base_dt=base_dt, **kw,
        )

    async def industry_monthly_chart(
        self, industry_cd: str, base_dt: str, **kw: Any,
    ) -> dict[str, Any]:
        """ka20008 — 업종월봉조회요청

        Args:
            industry_cd: 업종코드
            base_dt: 기준일자 (YYYYMMDD)
        """
        return await self._client.get(
            "/api/dostk/chart", tr_id="ka20008",
            indu_cd=industry_cd, base_dt=base_dt, **kw,
        )

    async def industry_yearly_chart(
        self, industry_cd: str, base_dt: str, **kw: Any,
    ) -> dict[str, Any]:
        """ka20019 — 업종년봉조회요청

        Args:
            industry_cd: 업종코드
            base_dt: 기준일자 (YYYYMMDD)
        """
        return await self._client.get(
            "/api/dostk/chart", tr_id="ka20019",
            indu_cd=industry_cd, base_dt=base_dt, **kw,
        )
