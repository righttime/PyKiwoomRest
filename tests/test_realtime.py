"""실시간 데이터 모듈 테스트"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
import json

from pykiwoomrest.realtime import (
    WebSocketClient,
    RealtimeAPI,
    RealtimeType,
    RealtimeMessageType,
    Subscription
)


@pytest.fixture
def mock_config():
    """모의 설정"""
    class MockConfig:
        mock = True
        api_key = "test_token"
    return MockConfig()


@pytest.fixture
def realtime_api(mock_config):
    """RealtimeAPI fixture"""
    return RealtimeAPI(access_token="test_token", mock=True)


class TestWebSocketClient:
    """WebSocketClient 테스트"""

    @pytest.mark.asyncio
    async def test_initialization(self):
        """초기화 테스트"""
        client = WebSocketClient("ws://test.com", "test_token")

        assert client.uri == "ws://test.com"
        assert client.access_token == "test_token"
        assert not client.connected
        assert client.keep_running
        assert client._next_grp_no == 1
        assert len(client._subscriptions) == 0

    def test_register_handler(self):
        """핸들러 등록 테스트"""
        client = WebSocketClient("ws://test.com", "test_token")

        def handler(msg):
            pass

        client.register_handler("0B", handler)
        assert "0B" in client._message_handlers
        assert handler in client._message_handlers["0B"]

    def test_unregister_handler(self):
        """핸들러 해제 테스트"""
        client = WebSocketClient("ws://test.com", "test_token")

        def handler(msg):
            pass

        client.register_handler("0B", handler)
        client.unregister_handler("0B", handler)
        assert handler not in client._message_handlers["0B"]

    @pytest.mark.asyncio
    async def test_send_message(self):
        """메시지 전송 테스트"""
        client = WebSocketClient("ws://test.com", "test_token")
        client.connected = True

        # WebSocket mock
        mock_ws = AsyncMock()
        client.websocket = mock_ws

        # Dict 메시지 전송
        await client.send_message({"trnm": "LOGIN", "token": "test"})
        mock_ws.send.assert_called_once()

        # 문자열 메시지 전송
        await client.send_message('{"trnm": "PING"}')
        assert mock_ws.send.call_count == 2

    def test_subscription_creation(self):
        """구독 생성 테스트"""
        client = WebSocketClient("ws://test.com", "test_token")

        # 자동 그룹 번호 할당
        grp_no = "1"
        assert client._next_grp_no == 2

    @pytest.mark.asyncio
    async def test_ping_pong_handling(self):
        """PING/PONG 처리 테스트"""
        client = WebSocketClient("ws://test.com", "test_token")
        client.connected = True

        # WebSocket mock
        mock_ws = AsyncMock()
        mock_ws.closed = False
        mock_ws.recv = AsyncMock(return_value='{"trnm": "PING"}')
        client.websocket = mock_ws

        # 메시지 수신 테스트
        pong_called = False

        async def mock_send(msg):
            nonlocal pong_called
            pong_called = True

        client.send_message = mock_send

        # 메시지 수신 실행 (한 번만)
        try:
            await asyncio.wait_for(client.receive_messages(), timeout=1.0)
        except asyncio.TimeoutError:
            pass

        assert pong_called

    @pytest.mark.asyncio
    async def test_message_handler_invocation(self):
        """메시지 핸들러 호출 테스트"""
        client = WebSocketClient("ws://test.com", "test_token")
        client.connected = True

        # 핸들러 등록
        handler_called = False
        received_message = None

        def handler(msg):
            nonlocal handler_called, received_message
            handler_called = True
            received_message = msg

        client.register_handler("0B", handler)

        # WebSocket mock
        test_message = {"trnm": "0B", "price": 50000}
        mock_ws = AsyncMock()
        mock_ws.closed = False
        mock_ws.recv = AsyncMock(return_value=json.dumps(test_message))
        client.websocket = mock_ws

        # 메시지 수신
        try:
            await asyncio.wait_for(client.receive_messages(), timeout=1.0)
        except asyncio.TimeoutError:
            pass

        assert handler_called
        assert received_message == test_message


class TestRealtimeAPI:
    """RealtimeAPI 테스트"""

    def test_initialization(self):
        """초기화 테스트"""
        api = RealtimeAPI(access_token="test_token", mock=True)

        assert api.access_token == "test_token"
        assert "mockapi.kiwoom.com" in api.ws_url

    def test_real_url_for_production(self):
        """실전 URL 테스트"""
        api = RealtimeAPI(access_token="test_token", mock=False)

        assert "api.kiwoom.com" in api.ws_url
        assert "mockapi" not in api.ws_url

    def test_create_client(self):
        """클라이언트 생성 테스트"""
        api = RealtimeAPI(access_token="test_token", mock=True)
        client = api.create_client()

        assert isinstance(client, WebSocketClient)
        assert api._client == client
        assert client.access_token == "test_token"

    def test_client_property(self):
        """client 속성 테스트"""
        api = RealtimeAPI(access_token="test_token", mock=True)
        assert api.client is None

        client = api.create_client()
        assert api.client == client


class TestRealtimeType:
    """RealtimeType 테스트"""

    def test_stock_types(self):
        """주식 타입 테스트"""
        assert RealtimeType.STOCK_0B.value == "0B"
        assert RealtimeType.STOCK_0C.value == "0C"
        assert RealtimeType.STOCK_0F.value == "0F"
        assert RealtimeType.STOCK_01.value == "01"
        assert RealtimeType.STOCK_02.value == "02"
        assert RealtimeType.STOCK_03.value == "03"

    def test_market_status_type(self):
        """장상태 타입 테스트"""
        assert RealtimeType.MARKET_STATUS.value == "90"


class TestSubscription:
    """Subscription 데이터클래스 테스트"""

    def test_creation(self):
        """구독 생성 테스트"""
        sub = Subscription(
            grp_no="1",
            items=["005930"],
            types=["0B"],
            refresh="1"
        )

        assert sub.grp_no == "1"
        assert sub.items == ["005930"]
        assert sub.types == ["0B"]
        assert sub.refresh == "1"

    def test_default_refresh(self):
        """기본 refresh 값 테스트"""
        sub = Subscription(
            grp_no="1",
            items=["005930"],
            types=["0B"]
        )

        assert sub.refresh == "1"


class TestRealtimeMessageType:
    """RealtimeMessageType 테스트"""

    def test_message_types(self):
        """메시지 타입 테스트"""
        assert RealtimeMessageType.LOGIN.value == "LOGIN"
        assert RealtimeMessageType.REG.value == "REG"
        assert RealtimeMessageType.DEREG.value == "DEREG"
        assert RealtimeMessageType.PING.value == "PING"
