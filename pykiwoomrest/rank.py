"""순위 조회 — /api/dostk/rkinfo"""

from __future__ import annotations

from typing import Any

from .client import KiwoomClient


class RankAPI:
    """순위 조회 API"""

    def __init__(self, client: KiwoomClient) -> None:
        self._client = client

    async def top_order_book_volume(self, **kw: Any) -> dict[str, Any]:
        """ka10020 — 호가잔량상위요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10020", **kw)

    async def sudden_order_book_increase(self, **kw: Any) -> dict[str, Any]:
        """ka10021 — 호가잔량급증요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10021", **kw)

    async def sudden_order_ratio_increase(self, **kw: Any) -> dict[str, Any]:
        """ka10022 — 잔량율급증요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10022", **kw)

    async def sudden_volume_increase(self, **kw: Any) -> dict[str, Any]:
        """ka10023 — 거래량급증요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10023", **kw)

    async def change_rate_rank(self, **kw: Any) -> dict[str, Any]:
        """ka10027 — 전일대비등락률상위요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10027", **kw)

    # alias
    async def top_change_rate(self, **kw: Any) -> dict[str, Any]:
        return await self.change_rate_rank(**kw)

    async def top_expected_change_rate(self, **kw: Any) -> dict[str, Any]:
        """ka10029 — 예상체결등락률상위요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10029", **kw)

    async def volume_rank(self, **kw: Any) -> dict[str, Any]:
        """ka10030 — 당일거래량상위요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10030", **kw)

    # alias
    async def top_volume_today(self, **kw: Any) -> dict[str, Any]:
        return await self.volume_rank(**kw)

    async def top_volume_yesterday(self, **kw: Any) -> dict[str, Any]:
        """ka10031 — 전일거래량상위요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10031", **kw)

    async def value_rank(self, **kw: Any) -> dict[str, Any]:
        """ka10032 — 거래대금상위요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10032", **kw)

    async def top_credit_ratio(self, **kw: Any) -> dict[str, Any]:
        """ka10033 — 신용비율상위요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10033", **kw)

    async def top_foreign_trades_by_period(self, **kw: Any) -> dict[str, Any]:
        """ka10034 — 외인기간별매매상위요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10034", **kw)

    async def top_foreign_consecutive_buy(self, **kw: Any) -> dict[str, Any]:
        """ka10035 — 외인연속순매매상위요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10035", **kw)

    async def top_foreign_limit_increase(self, **kw: Any) -> dict[str, Any]:
        """ka10036 — 외인한도소진율증가상위"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10036", **kw)

    async def top_foreign_broker_trading(self, **kw: Any) -> dict[str, Any]:
        """ka10037 — 외국계창구매매상위요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10037", **kw)

    async def broker_ranking_by_stock(self, stk_cd: str, **kw: Any) -> dict[str, Any]:
        """ka10038 — 종목별증권사순위요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10038", stk_cd=stk_cd, **kw)

    async def top_broker_by_stock(self, **kw: Any) -> dict[str, Any]:
        """ka10039 — 증권사별매매상위요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10039", **kw)

    async def main_brokers_today(self, **kw: Any) -> dict[str, Any]:
        """ka10040 — 당일주요거래원요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10040", **kw)

    async def top_net_buying_brokers(self, **kw: Any) -> dict[str, Any]:
        """ka10042 — 순매수거래원순위요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10042", **kw)

    async def departed_brokers_today(self, **kw: Any) -> dict[str, Any]:
        """ka10053 — 당일상위이탈원요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10053", **kw)

    async def same_day_net_buying_rank(self, **kw: Any) -> dict[str, Any]:
        """ka10062 — 동일순매매순위요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10062", **kw)

    async def top_intraday_investor_trading(self, **kw: Any) -> dict[str, Any]:
        """ka10065 — 장중투자자별매매상위요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10065", **kw)

    async def after_hours_change_rate_rank(self, **kw: Any) -> dict[str, Any]:
        """ka10098 — 시간외단일가등락율순위요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka10098", **kw)

    async def top_foreign_institution_trades(self, **kw: Any) -> dict[str, Any]:
        """ka90009 — 외국인기관매매상위요청"""
        return await self._client.get("/api/dostk/rkinfo", tr_id="ka90009", **kw)

    # aliases for old names
    async def orderbook_rank(self, **kw: Any) -> dict[str, Any]:
        return await self.top_order_book_volume(**kw)
