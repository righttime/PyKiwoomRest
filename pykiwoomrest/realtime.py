"""WebSocket 실시간 데이터 스트리밍"""

import asyncio
import json
import logging
from typing import Optional, Callable, Dict, List, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import websockets

logger = logging.getLogger(__name__)


class RealtimeMessageType(Enum):
    """실시간 메시지 타입"""
    LOGIN = "LOGIN"
    REG = "REG"
    DEREG = "DEREG"
    PING = "PING"
    QUOTE = "QUOTE"
    MARKET_STATUS = "MARKET_STATUS"


class RealtimeType(Enum):
    """실시간 데이터 타입"""
    # 시세 관련 (0x)
    STOCK_0B = "0B"  # 현재가
    STOCK_0C = "0C"  # 호가
    STOCK_0F = "0F"  # 체결
    STOCK_01 = "01"  # 주식체결
    STOCK_02 = "02"  # 주식호가
    STOCK_03 = "03"  # 주식매매

    # 장상태
    MARKET_STATUS = "90"  # 장상태


@dataclass
class Subscription:
    """실시간 구독 정보"""
    grp_no: str  # 그룹 번호
    items: List[str]  # 종목코드 리스트
    types: List[str]  # 실시간 타입 리스트
    refresh: str = "1"  # 기존 등록 유지 여부 (0:새로, 1:유지)


@dataclass
class MessageHandler:
    """메시지 핸들러"""
    message_type: str
    handler: Callable[[Dict[str, Any]], None]


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
            types: 실시간 타입 리스트 (예: ['0B', '0C'])
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
            'trnm': RealtimeMessageType.DEREG.value,
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
