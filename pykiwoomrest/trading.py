"""매수/매도 주문, 계좌 조회 (kt0xxxx, kt1xxxx TR)"""

from __future__ import annotations

import logging
from typing import Any

from .client import KiwoomClient

logger = logging.getLogger("pykiwoomrest.trading")


class TradingAPI:
    """매매 & 계좌 API"""

    def __init__(self, client: KiwoomClient, account_no: str | None = None) -> None:
        self._client = client
        self._account_no = account_no or client.config.account_no

    # ── 계좌 조회 ──────────────────────────────────

    async def deposit(self) -> dict[str, Any]:
        """kt00001 - 예수금상세현황 (POST 요청)"""
        data = {
            "qry_tp": "3",  # 3:추정조회, 2:일반조회
        }
        return await self._client.post(
            "/api/dostk/acnt", tr_id="kt00001", data=data
        )

    async def account_summary(self) -> dict[str, Any]:
        """kt00004 - 계좌평가현황 (총 평가금액, 수익률)"""
        data = {
            "qry_tp": "1",  # 1:일반조회, 2:주문가능조회
            "dmst_stex_tp": "KRX",  # 국내거래소구분 (필수)
        }
        return await self._client.post(
            "/api/dostk/acnt", tr_id="kt00004", data=data
        )

    async def holdings(self) -> dict[str, Any]:
        """kt00005 - 체결잔고 (보유 종목별 잔고)"""
        data = {
            "dmst_stex_tp": "KRX",  # 국내거소구분 (필수)
        }
        return await self._client.post(
            "/api/dostk/acnt", tr_id="kt00005", data=data
        )

    async def daily_profit_rate(self, qry_dt: str) -> dict[str, Any]:
        """ka01690 - 일별잔고수익률

        Args:
            qry_dt: 조회일자 (YYYYMMDD)
        """
        data = {
            "qry_dt": qry_dt,
        }
        logger.debug("📊 일별잔고수익률 조회: qry_dt=%s", qry_dt)
        return await self._client.post(
            "/api/dostk/acnt", tr_id="ka01690", data=data
        )

    # ── 주문 ───────────────────────────────────────

    async def buy(
        self,
        stk_cd: str,
        qty: int,
        price: int | None = None,
        dmst_stex_tp: str = "KRX",
    ) -> dict[str, Any]:
        """kt10000 - 매수주문

        Args:
            stk_cd: 종목코드
            qty: 수량
            price: 가격 (None이면 시장가)
            dmst_stex_tp: 국내거래소구분 (KRX, SOR, NXT 등)
        """
        # trde_tp: 0=보통, 3=시장가
        trde_tp = "3" if not price else "0"
        data = {
            "dmst_stex_tp": dmst_stex_tp,  # 국내거래소구분 (필수)
            "stk_cd": stk_cd,
            "ord_qty": str(qty),
            "trde_tp": trde_tp,
        }
        if price:
            data["ord_uv"] = str(price)  # 주문단가
        logger.warning("📈 매수주문: %s %d주 %s", stk_cd, qty, f"{price}원" if price else "시장가")
        logger.info(f"TradingAPI.buy 호출: endpoint=/api/dostk/ordr, tr_id=kt10000, data={data}")
        result = await self._client.post(
            "/api/dostk/ordr", tr_id="kt10000", data=data
        )
        logger.info(f"TradingAPI.buy 응답: {result}")
        return result

    async def sell(
        self,
        stk_cd: str,
        qty: int,
        price: int | None = None,
        dmst_stex_tp: str = "KRX",
    ) -> dict[str, Any]:
        """kt10001 - 매도주문

        Args:
            stk_cd: 종목코드
            qty: 수량
            price: 가격
            dmst_stex_tp: 국내거래소구분 (KRX, SOR, NXT 등)
        """
        # trde_tp: 0=보통, 3=시장가
        trde_tp = "3" if not price else "0"
        data = {
            "dmst_stex_tp": dmst_stex_tp,  # 국내거래소구분 (필수)
            "stk_cd": stk_cd,
            "ord_qty": str(qty),
            "trde_tp": trde_tp,
        }
        if price:
            data["ord_uv"] = str(price)  # 주문단가
        logger.warning("📉 매도주문: %s %d주 %s", stk_cd, qty, f"{price}원" if price else "시장가")
        return await self._client.post(
            "/api/dostk/ordr", tr_id="kt10001", data=data
        )

    async def cancel_order(
        self,
        orig_ord_no: str,
        stk_cd: str,
        qty: int | None = None,
        dmst_stex_tp: str = "KRX",
    ) -> dict[str, Any]:
        """kt10003 - 주문취소

        Args:
            orig_ord_no: 원주문번호
            stk_cd: 종목코드
            qty: 수량
            dmst_stex_tp: 국내거래소구분 (KRX, SOR, NXT 등)
        """
        data = {
            "dmst_stex_tp": dmst_stex_tp,  # 국내거래소구분 (필수)
            "orig_ord_no": orig_ord_no,
            "stk_cd": stk_cd,
        }
        if qty is not None:
            data["cncl_qty"] = str(qty)
        else:
            data["cncl_qty"] = "0"  # 전량 취소
        logger.warning("❌ 주문취소: %s %s", orig_ord_no, stk_cd)
        return await self._client.post(
            "/api/dostk/ordr", tr_id="kt10003", data=data
        )

    async def modify_order(
        self,
        orig_ord_no: str,
        stk_cd: str,
        mdfy_qty: int,
        mdfy_price: int,
    ) -> dict[str, Any]:
        """kt10002 - 주문정정"""
        data = {
            "dmst_stex_tp": "KRX",  # 국내거래소구분 (필수)
            "orig_ord_no": orig_ord_no,
            "stk_cd": stk_cd,
            "mdfy_qty": str(mdfy_qty),
            "mdfy_uv": str(mdfy_price),  # 수정단가
        }
        logger.warning("🔁 주문정정: %s %s %d주 → %d원", orig_ord_no, stk_cd, mdfy_qty, mdfy_price)
        return await self._client.post(
            "/api/dostk/ordr", tr_id="kt10002", data=data
        )

    async def unfulfilled_orders(
        self,
        all_stk_tp: str = "0",
        trde_tp: str = "0",
        stk_cd: str = "",
    ) -> dict[str, Any]:
        """ka10075 - 미체결조회

        Args:
            all_stk_tp: 전체종목구분 0:전체, 1:종목
            trde_tp:    매매구분    0:전체, 1:매도, 2:매수
            stk_cd:     종목코드 (all_stk_tp=1일 때 필수)
        """
        data = {
            "all_stk_tp": all_stk_tp,
            "trde_tp": trde_tp,
            "stk_cd": stk_cd,
            "stex_tp": "0",
        }
        logger.debug("🔍 미체결조회: all_stk_tp=%s trde_tp=%s stk_cd=%s", all_stk_tp, trde_tp, stk_cd)
        return await self._client.post(
            "/api/dostk/acnt", tr_id="ka10075", data=data
        )

    async def order_contracts(
        self,
        ord_dt: str = "",
        qry_tp: str = "3",  # 3:미체결, 4:체결내역만
        stk_bond_tp: str = "0",  # 0:전체, 1:주식, 2:채권
        sell_tp: str = "0",  # 0:전체, 1:매도, 2:매수
        stk_cd: str = "",  # 공백일때 전체종목
        fr_ord_no: str = "",  # 시작주문번호, 공백일때 전체
        dmst_stex_tp: str = "%",  # %:전체, KRX, NXT, SOR
    ) -> dict[str, Any]:
        """kt00007 - 계좌별주문체결내역상세

        Args:
            ord_dt: 주문일자 (YYYYMMDD), 공백 가능
            qry_tp: 조회구분 (필수)
                1: 주문순
                2: 역순
                3: 미체결
                4: 체결내역만
            stk_bond_tp: 주식채권구분 (필수)
                0: 전체
                1: 주식
                2: 채권
            sell_tp: 매도수구분 (필수)
                0: 전체
                1: 매도
                2: 매수
            stk_cd: 종목코드, 공백허용 (공백일때 전체종목)
            fr_ord_no: 시작주문번호, 공백허용 (공백일때 전체주문)
            dmst_stex_tp: 국내거래소구분 (필수)
                %: 전체
                KRX: 한국거래소
                NXT: 넥스트트레이드
                SOR: 최선주문집행

        Returns:
            응답 데이터 (acnt_ord_cntr_prps_dtl 배열 포함)
        """
        data = {
            "ord_dt": ord_dt,
            "qry_tp": qry_tp,
            "stk_bond_tp": stk_bond_tp,
            "sell_tp": sell_tp,
            "stk_cd": stk_cd,
            "fr_ord_no": fr_ord_no,
            "dmst_stex_tp": dmst_stex_tp,
        }

        logger.debug(
            "📋 계좌별주문체결내역상세: qry_tp=%s stk_cd=%s sell_tp=%s",
            qry_tp, stk_cd, sell_tp
        )
        return await self._client.post(
            "/api/dostk/acnt", tr_id="kt00007", data=data
        )
