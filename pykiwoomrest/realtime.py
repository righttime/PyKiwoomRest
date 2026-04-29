"""WebSocket 실시간 데이터 스트리밍"""

import asyncio
import json
import logging
from typing import Optional, Callable, Dict, List, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import websockets

logger = logging.getLogger(__name__)


# ============================================================================
# 필드 정의 (키움 API 실시간 데이터 필드)
# ============================================================================

class OrderField(Enum):
    """주문/체결 관련 필드 (0A)"""
    ACCOUNT_NO = "9201"           # 계좌번호
    ORDER_NO = "9203"              # 주문번호
    MANAGER_NO = "9205"            # 관리자사번
    STOCK_CODE = "9001"            # 종목코드, 업종코드
    ORDER_TYPE = "912"             # 주문업무분류
    ORDER_STATUS = "913"           # 주문상태 (접수, 체결, 확인, 취소, 거부)
    STOCK_NAME = "302"             # 종목명
    ORDER_QTY = "900"              # 주문수량
    ORDER_PRICE = "901"            # 주문가격
    UNFILLED_QTY = "902"           # 미체결수량
    FILLED_AMOUNT = "903"          # 체결누계금액
    ORIGINAL_ORDER_NO = "904"      # 원주문번호
    ORDER_DIVISION = "905"         # 주문구분 (+/-, 매도, 매수, 매도정정, 매수정정, 매수취소, 매도취소)
    TRADE_DIVISION = "906"         # 매매구분 (보통, 시장가, 조건부지정가, 최유리지정가, 최우선지정가, ...)
    SELL_BUY_DIVISION = "907"      # 매도수구분 (1:매도, 2:매수)
    ORDER_TIME = "908"             # 주문/체결시간
    EXECUTION_NO = "909"           # 체결번호
    EXECUTION_PRICE = "910"        # 체결가
    EXECUTION_QTY = "911"          # 체결량
    CURRENT_PRICE = "10"           # 현재가
    ASK_PRICE = "27"               # (최우선)매도호가
    BID_PRICE = "28"               # (최우선)매수호가
    UNIT_EXEC_PRICE = "914"        # 단위체결가
    UNIT_EXEC_QTY = "915"          # 단위체결량
    COMMISSION = "938"             # 당일매매수수료
    TAX = "939"                    # 당일매매세금
    REJECT_REASON = "919"          # 거부사유
    SCREEN_NO = "920"              # 화면번호
    TERMINAL_NO = "921"            # 터미널번호
    CREDIT_DIVISION = "922"        # 신용구분
    LOAN_DATE = "923"              # 대출일
    AFTER_CURRENT_PRICE = "10010"  # 시간외단일가_현재가
    MARKET_DIVISION = "2134"       # 거래소구분 (0:통합, 1:KRX, 2:NXT)
    MARKET_DIVISION_NAME = "2135"  # 거래소구분명
    SOR_YN = "2136"                # SOR여부 (Y,N)


class QuoteField(Enum):
    """시세 관련 필드 (0B)"""
    EXECUTION_TIME = "20"          # 체결시간
    CURRENT_PRICE = "10"           # 현재가
    CHANGE = "11"                  # 전일대비
    CHANGE_RATE = "12"             # 등락률
    ASK_PRICE = "27"               # (최우선)매도호가
    BID_PRICE = "28"               # (최우선)매수호가
    TRADE_VOLUME = "15"            # 거래량 (+:매수체결, -:매도체결)
    CUMULATIVE_VOLUME = "13"       # 누적거래량
    CUMULATIVE_AMOUNT = "14"       # 누적거래대금
    OPEN_PRICE = "16"              # 시가
    HIGH_PRICE = "17"              # 고가
    LOW_PRICE = "18"               # 저가
    CHANGE_SIGN = "25"             # 전일대비기호
    PREVIOUS_VOLUME = "26"         # 전일거래량대비(계약,주)
    AMOUNT_CHANGE = "29"           # 거래대금증감
    PREVIOUS_VOLUME_RATIO = "30"   # 전일거래량대비(비율)
    TURNOVER_RATE = "31"           # 거래회전율
    TRADING_COST = "32"            # 거래비용
    EXECUTION_STRENGTH = "228"     # 체결강도
    MARKET_CAP = "311"             # 시가총액(억)
    SESSION_DIVISION = "290"       # 장구분 (1:장전 시간외, 2:장중, 3:장후 시간외)
    KO_APPROACH = "691"            # K.O 접근도
    HIGH_LIMIT_TIME = "567"        # 상한가발생시간
    LOW_LIMIT_TIME = "568"         # 하한가발생시간
    PREVIOUS_SAME_TIME_VOLUME_RATIO = "851"  # 전일 동시간 거래량 비율
    OPEN_TIME = "1890"             # 시가시간
    HIGH_TIME = "1891"             # 고가시간
    LOW_TIME = "1892"              # 저가시간
    SELL_EXEC_QTY = "1030"         # 매도체결량
    BUY_EXEC_QTY = "1031"          # 매수체결량
    BUY_RATIO = "1032"             # 매수비율
    SELL_EXEC_COUNT = "1071"       # 매도체결건수
    BUY_EXEC_COUNT = "1072"        # 매수체결건수
    INSTANT_AMOUNT = "1313"        # 순간거래대금
    SELL_EXEC_QTY_SINGLE = "1315"  # 매도체결량_단건
    BUY_EXEC_QTY_SINGLE = "1316"   # 매수체결량_단건
    NET_BUY_EXEC_QTY = "1314"      # 순매수체결량
    CFD_MARGIN = "1497"            # CFD증거금
    MAINTENANCE_MARGIN = "1498"    # 유지증거금
    AVERAGE_TRADE_PRICE = "620"    # 당일거래평균가
    CFD_COST = "732"               # CFD거래비용
    DTS_COST = "852"                # 대주거래비용
    MARKET_DIVISION = "9081"       # 거래소구분


# ============================================================================
# 메시지 타입
# ============================================================================

class RealtimeMessageType(Enum):
    """실시간 메시지 타입"""
    LOGIN = "LOGIN"
    REG = "REG"
    DEREG = "DEREG"
    REMOVE = "REMOVE"
    PING = "PING"


class RealtimeType(Enum):
    """실시간 데이터 타입 (TR 명)"""
    # 주문/체결 관련
    ORDER_EXECUTION = "0A"          # 주문/체결

    # 시세 관련
    STOCK_CURRENT = "0B"            # 현재가
    STOCK_QUOTE = "0C"              # 호가
    STOCK_EXECUTION = "0F"          # 체결
    STOCK_01 = "01"                 # 주식체결
    STOCK_02 = "02"                 # 주식호가
    STOCK_03 = "03"                 # 주식매매

    # 장상태
    MARKET_STATUS = "90"            # 장상태


# ============================================================================
# 데이터클래스
# ============================================================================

@dataclass
class OrderExecutionData:
    """주문/체결 데이터 (0A)"""
    account_no: str = ""
    order_no: str = ""
    manager_no: str = ""
    stock_code: str = ""
    order_type: str = ""
    order_status: str = ""
    stock_name: str = ""
    order_qty: int = 0
    order_price: float = 0.0
    unfilled_qty: int = 0
    filled_amount: float = 0.0
    original_order_no: str = ""
    order_division: str = ""
    trade_division: str = ""
    sell_buy_division: str = ""
    order_time: str = ""
    execution_no: str = ""
    execution_price: float = 0.0
    execution_qty: int = 0
    current_price: float = 0.0
    ask_price: float = 0.0
    bid_price: float = 0.0
    unit_exec_price: float = 0.0
    unit_exec_qty: int = 0
    commission: float = 0.0
    tax: float = 0.0
    reject_reason: str = ""
    screen_no: str = ""
    terminal_no: str = ""
    credit_division: str = ""
    loan_date: str = ""
    after_current_price: float = 0.0
    market_division: str = ""
    market_division_name: str = ""
    sor_yn: str = ""
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_values(cls, values: Dict[str, str]) -> "OrderExecutionData":
        """values 딕셔너리에서 OrderExecutionData 생성"""
        def safe_int(val: Optional[str]) -> int:
            try:
                return int(val) if val else 0
            except:
                return 0

        def safe_float(val: Optional[str]) -> float:
            try:
                return float(val) if val else 0.0
            except:
                return 0.0

        return cls(
            account_no=values.get(OrderField.ACCOUNT_NO.value, ""),
            order_no=values.get(OrderField.ORDER_NO.value, ""),
            manager_no=values.get(OrderField.MANAGER_NO.value, ""),
            stock_code=values.get(OrderField.STOCK_CODE.value, ""),
            order_type=values.get(OrderField.ORDER_TYPE.value, ""),
            order_status=values.get(OrderField.ORDER_STATUS.value, ""),
            stock_name=values.get(OrderField.STOCK_NAME.value, ""),
            order_qty=safe_int(values.get(OrderField.ORDER_QTY.value)),
            order_price=safe_float(values.get(OrderField.ORDER_PRICE.value)),
            unfilled_qty=safe_int(values.get(OrderField.UNFILLED_QTY.value)),
            filled_amount=safe_float(values.get(OrderField.FILLED_AMOUNT.value)),
            original_order_no=values.get(OrderField.ORIGINAL_ORDER_NO.value, ""),
            order_division=values.get(OrderField.ORDER_DIVISION.value, ""),
            trade_division=values.get(OrderField.TRADE_DIVISION.value, ""),
            sell_buy_division=values.get(OrderField.SELL_BUY_DIVISION.value, ""),
            order_time=values.get(OrderField.ORDER_TIME.value, ""),
            execution_no=values.get(OrderField.EXECUTION_NO.value, ""),
            execution_price=safe_float(values.get(OrderField.EXECUTION_PRICE.value)),
            execution_qty=safe_int(values.get(OrderField.EXECUTION_QTY.value)),
            current_price=safe_float(values.get(OrderField.CURRENT_PRICE.value)),
            ask_price=safe_float(values.get(OrderField.ASK_PRICE.value)),
            bid_price=safe_float(values.get(OrderField.BID_PRICE.value)),
            unit_exec_price=safe_float(values.get(OrderField.UNIT_EXEC_PRICE.value)),
            unit_exec_qty=safe_int(values.get(OrderField.UNIT_EXEC_QTY.value)),
            commission=safe_float(values.get(OrderField.COMMISSION.value)),
            tax=safe_float(values.get(OrderField.TAX.value)),
            reject_reason=values.get(OrderField.REJECT_REASON.value, ""),
            screen_no=values.get(OrderField.SCREEN_NO.value, ""),
            terminal_no=values.get(OrderField.TERMINAL_NO.value, ""),
            credit_division=values.get(OrderField.CREDIT_DIVISION.value, ""),
            loan_date=values.get(OrderField.LOAN_DATE.value, ""),
            after_current_price=safe_float(values.get(OrderField.AFTER_CURRENT_PRICE.value)),
            market_division=values.get(OrderField.MARKET_DIVISION.value, ""),
            market_division_name=values.get(OrderField.MARKET_DIVISION_NAME.value, ""),
            sor_yn=values.get(OrderField.SOR_YN.value, ""),
            raw=values
        )


@dataclass
class QuoteData:
    """시세 데이터 (0B)"""
    execution_time: str = ""
    current_price: float = 0.0
    change: float = 0.0
    change_rate: float = 0.0
    ask_price: float = 0.0
    bid_price: float = 0.0
    trade_volume: int = 0
    cumulative_volume: int = 0
    cumulative_amount: float = 0.0
    open_price: float = 0.0
    high_price: float = 0.0
    low_price: float = 0.0
    change_sign: str = ""
    previous_volume: int = 0
    amount_change: float = 0.0
    previous_volume_ratio: float = 0.0
    turnover_rate: float = 0.0
    trading_cost: float = 0.0
    execution_strength: float = 0.0
    market_cap: float = 0.0
    session_division: str = ""
    ko_approach: float = 0.0
    high_limit_time: str = ""
    low_limit_time: str = ""
    previous_same_time_volume_ratio: float = 0.0
    open_time: str = ""
    high_time: str = ""
    low_time: str = ""
    sell_exec_qty: int = 0
    buy_exec_qty: int = 0
    buy_ratio: float = 0.0
    sell_exec_count: int = 0
    buy_exec_count: int = 0
    instant_amount: float = 0.0
    sell_exec_qty_single: int = 0
    buy_exec_qty_single: int = 0
    net_buy_exec_qty: int = 0
    cfd_margin: float = 0.0
    maintenance_margin: float = 0.0
    average_trade_price: float = 0.0
    cfd_cost: float = 0.0
    dts_cost: float = 0.0
    market_division: str = ""
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_values(cls, values: Dict[str, str]) -> "QuoteData":
        """values 딕셔너리에서 QuoteData 생성"""
        def safe_int(val: Optional[str]) -> int:
            try:
                return int(val) if val else 0
            except:
                return 0

        def safe_float(val: Optional[str]) -> float:
            try:
                return float(val) if val else 0.0
            except:
                return 0.0

        return cls(
            execution_time=values.get(QuoteField.EXECUTION_TIME.value, ""),
            current_price=safe_float(values.get(QuoteField.CURRENT_PRICE.value)),
            change=safe_float(values.get(QuoteField.CHANGE.value)),
            change_rate=safe_float(values.get(QuoteField.CHANGE_RATE.value)),
            ask_price=safe_float(values.get(QuoteField.ASK_PRICE.value)),
            bid_price=safe_float(values.get(QuoteField.BID_PRICE.value)),
            trade_volume=safe_int(values.get(QuoteField.TRADE_VOLUME.value)),
            cumulative_volume=safe_int(values.get(QuoteField.CUMULATIVE_VOLUME.value)),
            cumulative_amount=safe_float(values.get(QuoteField.CUMULATIVE_AMOUNT.value)),
            open_price=safe_float(values.get(QuoteField.OPEN_PRICE.value)),
            high_price=safe_float(values.get(QuoteField.HIGH_PRICE.value)),
            low_price=safe_float(values.get(QuoteField.LOW_PRICE.value)),
            change_sign=values.get(QuoteField.CHANGE_SIGN.value, ""),
            previous_volume=safe_int(values.get(QuoteField.PREVIOUS_VOLUME.value)),
            amount_change=safe_float(values.get(QuoteField.AMOUNT_CHANGE.value)),
            previous_volume_ratio=safe_float(values.get(QuoteField.PREVIOUS_VOLUME_RATIO.value)),
            turnover_rate=safe_float(values.get(QuoteField.TURNOVER_RATE.value)),
            trading_cost=safe_float(values.get(QuoteField.TRADING_COST.value)),
            execution_strength=safe_float(values.get(QuoteField.EXECUTION_STRENGTH.value)),
            market_cap=safe_float(values.get(QuoteField.MARKET_CAP.value)),
            session_division=values.get(QuoteField.SESSION_DIVISION.value, ""),
            ko_approach=safe_float(values.get(QuoteField.KO_APPROACH.value)),
            high_limit_time=values.get(QuoteField.HIGH_LIMIT_TIME.value, ""),
            low_limit_time=values.get(QuoteField.LOW_LIMIT_TIME.value, ""),
            previous_same_time_volume_ratio=safe_float(values.get(QuoteField.PREVIOUS_SAME_TIME_VOLUME_RATIO.value)),
            open_time=values.get(QuoteField.OPEN_TIME.value, ""),
            high_time=values.get(QuoteField.HIGH_TIME.value, ""),
            low_time=values.get(QuoteField.LOW_TIME.value, ""),
            sell_exec_qty=safe_int(values.get(QuoteField.SELL_EXEC_QTY.value)),
            buy_exec_qty=safe_int(values.get(QuoteField.BUY_EXEC_QTY.value)),
            buy_ratio=safe_float(values.get(QuoteField.BUY_RATIO.value)),
            sell_exec_count=safe_int(values.get(QuoteField.SELL_EXEC_COUNT.value)),
            buy_exec_count=safe_int(values.get(QuoteField.BUY_EXEC_COUNT.value)),
            instant_amount=safe_float(values.get(QuoteField.INSTANT_AMOUNT.value)),
            sell_exec_qty_single=safe_int(values.get(QuoteField.SELL_EXEC_QTY_SINGLE.value)),
            buy_exec_qty_single=safe_int(values.get(QuoteField.BUY_EXEC_QTY_SINGLE.value)),
            net_buy_exec_qty=safe_int(values.get(QuoteField.NET_BUY_EXEC_QTY.value)),
            cfd_margin=safe_float(values.get(QuoteField.CFD_MARGIN.value)),
            maintenance_margin=safe_float(values.get(QuoteField.MAINTENANCE_MARGIN.value)),
            average_trade_price=safe_float(values.get(QuoteField.AVERAGE_TRADE_PRICE.value)),
            cfd_cost=safe_float(values.get(QuoteField.CFD_COST.value)),
            dts_cost=safe_float(values.get(QuoteField.DTS_COST.value)),
            market_division=values.get(QuoteField.MARKET_DIVISION.value, ""),
            raw=values
        )


# ============================================================================
# 구독 관련
# ============================================================================

@dataclass
class Subscription:
    """실시간 구독 정보"""
    grp_no: str  # 그룹 번호
    items: List[str]  # 종목코드 리스트 (주문일 경우 빈 문자열 "")
    types: List[str]  # 실시간 타입 리스트
    refresh: str = "1"  # 기존 등록 유지 여부 (0:새로, 1:유지)


# ============================================================================
# WebSocket 클라이언트
# ============================================================================

class WebSocketClient:
    """WebSocket 클라이언트 - 실시간 데이터 스트리밍"""

    def __init__(self, uri: str, access_token: str):
        self.uri = uri
        self.access_token = access_token
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.connected = False
        self.keep_running = True
        self._receive_task: Optional[asyncio.Task] = None
        self._message_handlers: Dict[str, List[Callable]] = {}
        self._subscriptions: Dict[str, Subscription] = {}  # grp_no -> Subscription
        self._next_grp_no = 1

    async def connect(self) -> bool:
        """WebSocket 서버에 연결"""
        try:
            logger.info(f"Connecting to WebSocket server: {self.uri}")
            self.websocket = await websockets.connect(self.uri)
            self.connected = True
            logger.info("WebSocket 연결 성공")

            # 로그인 패킷 전송
            await self._send_login()
            return True

        except Exception as e:
            logger.error(f"WebSocket 연결 실패: {e}")
            self.connected = False
            return False

    async def _send_login(self) -> bool:
        """로그인 패킷 전송"""
        param = {
            'trnm': RealtimeMessageType.LOGIN.value,
            'token': self.access_token
        }

        logger.info("로그인 패킷 전송 중...")
        await self.send_message(param)

        # 로그인 응답 대기 (최대 5초)
        try:
            response = await asyncio.wait_for(
                self._wait_for_response(RealtimeMessageType.LOGIN.value),
                timeout=5.0
            )

            if response.get('return_code') != 0:
                logger.error(f"로그인 실패: {response.get('return_msg')}")
                await self.disconnect()
                return False

            logger.info("로그인 성공")
            return True

        except asyncio.TimeoutError:
            logger.error("로그인 응답 타임아웃")
            await self.disconnect()
            return False

    async def _wait_for_response(self, expected_type: str, timeout: float = 5.0) -> Dict[str, Any]:
        """특정 타입의 응답 대기"""
        future = asyncio.Future()

        async def wait_handler(message: Dict[str, Any]):
            if not future.done():
                future.set_result(message)

        # 임시 핸들러 등록
        self._register_handler(expected_type, wait_handler)

        try:
            return await asyncio.wait_for(future, timeout=timeout)
        finally:
            self._unregister_handler(expected_type, wait_handler)

    async def send_message(self, message: Any) -> None:
        """서버에 메시지 전송"""
        if not self.connected:
            logger.warning("WebSocket이 연결되지 않음. 연결 시도...")
            if not await self.connect():
                raise ConnectionError("WebSocket 연결 실패")

        # 문자열이 아니면 JSON 직렬화
        if not isinstance(message, str):
            message = json.dumps(message, ensure_ascii=False)

        await self.websocket.send(message)
        logger.debug(f"Message sent: {message[:100]}...")

    async def receive_messages(self) -> None:
        """서버 메시지 수신 루프"""
        logger.info("메시지 수신 루프 시작")
        while self.keep_running:
            try:
                if not self.websocket or self.websocket.closed:
                    logger.warning("WebSocket 연결 끊김. 재연결 시도...")
                    await asyncio.sleep(1)
                    if await self.connect():
                        # 재연결 성공 시 기존 구독 재등록
                        await self._restore_subscriptions()
                    continue

                # 메시지 수신
                raw_message = await self.websocket.recv()
                response = json.loads(raw_message)

                # PING 처리 (PONG 응답)
                if response.get('trnm') == RealtimeMessageType.PING.value:
                    await self.send_message(response)
                    logger.debug("PING 수신, PONG 응답")
                    continue

                # 메시지 핸들러 호출
                message_type = response.get('trnm', '')
                handlers = self._message_handlers.get(message_type, [])

                for handler in handlers:
                    try:
                        if asyncio.iscoroutinefunction(handler):
                            await handler(response)
                        else:
                            handler(response)
                    except Exception as e:
                        logger.error(f"Handler error for {message_type}: {e}", exc_info=True)

                # 기본 로그 (핸들러가 없는 경우)
                if not handlers and message_type != RealtimeMessageType.PING.value:
                    logger.debug(f"실시간 시세 수신 [{message_type}]: {response}")

            except websockets.ConnectionClosed:
                logger.warning("WebSocket 연결이 서버에 의해 종료됨")
                self.connected = False
                await self._handle_disconnect()

            except json.JSONDecodeError as e:
                logger.error(f"JSON 파싱 오류: {e}")

            except Exception as e:
                logger.error(f"메시지 수신 오류: {e}", exc_info=True)
                await asyncio.sleep(1)

    async def _handle_disconnect(self) -> None:
        """연결 끊김 처리"""
        self.connected = False
        if self.websocket:
            try:
                await self.websocket.close()
            except:
                pass

        # 재연결 시도
        if self.keep_running:
            logger.info("5초 후 재연결 시도...")
            await asyncio.sleep(5)

    async def _restore_subscriptions(self) -> None:
        """기존 구독 재등록"""
        if not self._subscriptions:
            return

        logger.info(f"기존 구독 {len(self._subscriptions)}개 재등록...")
        for grp_no, subscription in self._subscriptions.items():
            await self.register(
                grp_no=subscription.grp_no,
                items=subscription.items,
                types=subscription.types,
                refresh="0"  # 재등록은 refresh=0
            )

    def register_handler(self, message_type: str, handler: Callable) -> None:
        """메시지 핸들러 등록"""
        if message_type not in self._message_handlers:
            self._message_handlers[message_type] = []
        self._message_handlers[message_type].append(handler)
        logger.debug(f"Handler registered for {message_type}")

    def unregister_handler(self, message_type: str, handler: Callable) -> None:
        """메시지 핸들러 해제"""
        if message_type in self._message_handlers:
            if handler in self._message_handlers[message_type]:
                self._message_handlers[message_type].remove(handler)
                logger.debug(f"Handler unregistered for {message_type}")

    def _register_handler(self, message_type: str, handler: Callable) -> None:
        """내부 핸들러 등록"""
        if message_type not in self._message_handlers:
            self._message_handlers[message_type] = []
        self._message_handlers[message_type].append(handler)

    def _unregister_handler(self, message_type: str, handler: Callable) -> None:
        """내부 핸들러 해제"""
        if message_type in self._message_handlers:
            if handler in self._message_handlers[message_type]:
                self._message_handlers[message_type].remove(handler)

    async def register(
        self,
        items: List[str],
        types: List[str],
        grp_no: Optional[str] = None,
        refresh: str = "1"
    ) -> str:
        """실시간 항목 등록

        Args:
            items: 종목코드 리스트 (예: ['005930', '000660'])
                   주문 체결(0A)일 경우 빈 리스트 또는 ['']
            types: 실시간 타입 리스트 (예: ['0A', '0B'])
            grp_no: 그룹 번호 (None이면 자동 생성)
            refresh: 기존 등록 유지 여부 (0: 새로, 1: 유지)

        Returns:
            그룹 번호
        """
        if grp_no is None:
            grp_no = str(self._next_grp_no)
            self._next_grp_no += 1

        message = {
            'trnm': RealtimeMessageType.REG.value,
            'grp_no': grp_no,
            'refresh': refresh,
            'data': [{
                'item': items,
                'type': types,
            }]
        }

        logger.info(f"실시간 등록: 그룹 {grp_no}, 종목 {len(items)}개, 타입 {types}")
        await self.send_message(message)

        # 구독 정보 저장
        self._subscriptions[grp_no] = Subscription(
            grp_no=grp_no,
            items=items,
            types=types,
            refresh=refresh
        )

        return grp_no

    async def deregister(self, grp_no: str) -> None:
        """실시간 항목 해지

        Args:
            grp_no: 그룹 번호
        """
        message = {
            'trnm': RealtimeMessageType.REMOVE.value,
            'grp_no': grp_no,
        }

        logger.info(f"실시간 해지: 그룹 {grp_no}")
        await self.send_message(message)

        # 구독 정보 삭제
        if grp_no in self._subscriptions:
            del self._subscriptions[grp_no]

    async def deregister_all(self) -> None:
        """모든 실시간 항목 해지"""
        grp_nos = list(self._subscriptions.keys())
        for grp_no in grp_nos:
            await self.deregister(grp_no)

    async def run(self) -> None:
        """WebSocket 클라이언트 실행"""
        await self.connect()
        await self.receive_messages()

    async def start(self) -> None:
        """백그라운드에서 WebSocket 실행"""
        if self._receive_task and not self._receive_task.done():
            logger.warning("WebSocket 이미 실행 중")
            return

        self._receive_task = asyncio.create_task(self.run())
        logger.info("WebSocket 백그라운드 실행 시작")

    async def stop(self) -> None:
        """WebSocket 클라이언트 중지"""
        logger.info("WebSocket 중지 중...")
        self.keep_running = False

        # 모든 구독 해지
        await self.deregister_all()

        # 수신 태스크 중지
        if self._receive_task and not self._receive_task.done():
            self._receive_task.cancel()
            try:
                await self._receive_task
            except asyncio.CancelledError:
                pass

        await self.disconnect()
        logger.info("WebSocket 중지 완료")

    async def disconnect(self) -> None:
        """WebSocket 연결 종료"""
        self.keep_running = False
        if self.connected and self.websocket:
            try:
                await self.websocket.close()
            except:
                pass
            self.connected = False
            logger.info("WebSocket 연결 종료")

    @property
    def is_connected(self) -> bool:
        """연결 상태"""
        return self.connected and self.websocket and not self.websocket.closed

    @property
    def subscriptions(self) -> Dict[str, Subscription]:
        """현재 구독 목록"""
        return self._subscriptions.copy()

    async def __aenter__(self) -> "WebSocketClient":
        """Async context manager 진입"""
        await self.connect()
        return self

    async def __aexit__(self, *args) -> None:
        """Async context manager 종료"""
        await self.stop()


# ============================================================================
# Realtime API
# ============================================================================

class RealtimeAPI:
    """실시간 데이터 API"""

    def __init__(self, access_token: str, mock: bool = False):
        """초기화

        Args:
            access_token: 액세스 토큰
            mock: 모의투자 여부
        """
        self.access_token = access_token

        # WebSocket URL 설정
        if mock:
            self.ws_url = "wss://mockapi.kiwoom.com:10000/api/dostk/websocket"
        else:
            self.ws_url = "wss://api.kiwoom.com:10000/api/dostk/websocket"

        self._client: Optional[WebSocketClient] = None

    def create_client(self) -> WebSocketClient:
        """WebSocket 클라이언트 생성

        Returns:
            WebSocketClient 인스턴스
        """
        self._client = WebSocketClient(self.ws_url, self.access_token)
        return self._client

    @property
    def client(self) -> Optional[WebSocketClient]:
        """현재 WebSocket 클라이언트"""
        return self._client
