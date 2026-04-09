"""조건검색 — /api/dostk/stkinfo"""

from __future__ import annotations

from typing import Any

from .client import KiwoomClient


class ConditionAPI:
    """조건검색 API (영웅문4 조건 활용)"""

    def __init__(self, client: KiwoomClient) -> None:
        self._client = client

    async def condition_list(self, trnm: str = "CNSRLST", **kw: Any) -> dict[str, Any]:
        """ka10171 — 조건검색 목록조회

        Args:
            trnm: TR명 (고정값: CNSRLST)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10171", trnm=trnm, **kw,
        )

    async def condition_search(
        self,
        trnm: str = "CNSRREQ", seq: str = "",
        search_type: str = "", stex_tp: str = "K",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10172 — 조건검색 요청 (일반)

        Args:
            trnm: 서비스명 (고정값: CNSRREQ)
            seq: 조건검색식 일련번호
            search_type: 조회타입
            stex_tp: 거래소구분 (K:KRX)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10172",
            trnm=trnm, seq=seq, search_type=search_type,
            stex_tp=stex_tp, **kw,
        )

    async def condition_search_realtime(
        self,
        trnm: str = "CNSRREQ", seq: str = "",
        search_type: str = "1", stex_tp: str = "K",
        **kw: Any,
    ) -> dict[str, Any]:
        """ka10173 — 조건검색 요청 (실시간)

        Args:
            trnm: 서비스명 (고정값: CNSRREQ)
            seq: 조건검색식 일련번호
            search_type: 조회타입 (1:조건검색+실시간조건검색)
            stex_tp: 거래소구분 (K:KRX)
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10173",
            trnm=trnm, seq=seq, search_type=search_type,
            stex_tp=stex_tp, **kw,
        )

    async def condition_search_cancel(
        self, trnm: str = "CNSRCLR", seq: str = "", **kw: Any,
    ) -> dict[str, Any]:
        """ka10174 — 조건검색 실시간 해제

        Args:
            trnm: 서비스명 (CNSRCLR)
            seq: 조건검색식 일련번호
        """
        return await self._client.get(
            "/api/dostk/stkinfo", tr_id="ka10174",
            trnm=trnm, seq=seq, **kw,
        )
