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
    Subscription,
    OrderField,
    QuoteField,
    OrderExecutionData,
    QuoteData
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


class TestOrderExecutionData:
    """OrderExecutionData 테스트"""

    def test_from_values_basic(self):
        """기본 values 변환 테스트"""
        values = {
            OrderField.ORDER_NO.value: "12345",
            OrderField.STOCK_CODE.value: "005930",
            OrderField.ORDER_STATUS.value: "체결",
            OrderField.ORDER_QTY.value: "100",
            OrderField.ORDER_PRICE.value: "50000",
            OrderField.EXECUTION_PRICE.value: "50000",
            OrderField.EXECUTION_QTY.value: "50",
        }

        data = OrderExecutionData.from_values(values)

        assert data.order_no == "12345"
        assert data.stock_code == "005930"
        assert data.order_status == "체결"
        assert data.order_qty == 100
        assert data.order_price == 50000.0
        assert data.execution_price == 50000.0
        assert data.execution_qty == 50

    def test_from_values_with_nulls(self):
        """null 값 처리 테스트"""
        values = {
            OrderField.ORDER_NO.value: None,
            OrderField.ORDER_QTY.value: "",
            OrderField.ORDER_PRICE.value: "invalid",
        }

        data = OrderExecutionData.from_values(values)

        assert data.order_no == ""
        assert data.order_qty == 0
        assert data.order_price == 0.0

    def test_all_fields(self):
        """모든 필드 변환 테스트"""
        values = {
            OrderField.ACCOUNT_NO.value: "12345678",
            OrderField.ORDER_NO.value: "ORD001",
            OrderField.STOCK_CODE.value: "005930",
            OrderField.ORDER_STATUS.value: "체결",
            OrderField.STOCK_NAME.value: "삼성전자",
            OrderField.ORDER_QTY.value: "100",
            OrderField.ORDER_PRICE.value: "50000",
            OrderField.UNFILLED_QTY.value: "50",
            OrderField.EXECUTION_PRICE.value: "50000",
            OrderField.EXECUTION_QTY.value: "50",
            OrderField.SELL_BUY_DIVISION.value: "2",
        }

        data = OrderExecutionData.from_values(values)

        assert data.account_no == "12345678"
        assert data.order_no == "ORD001"
        assert data.stock_code == "005930"
        assert data.order_status == "체결"
        assert data.stock_name == "삼성전자"
        assert data.order_qty == 100
        assert data.order_price == 50000.0
        assert data.unfilled_qty == 50
        assert data.execution_price == 50000.0
        assert data.execution_qty == 50
        assert data.sell_buy_division == "2"


class TestQuoteData:
    """QuoteData 테스트"""

    def test_from_values_basic(self):
        """기본 values 변환 테스트"""
        values = {
            QuoteField.CURRENT_PRICE.value: "50000",
            QuoteField.CHANGE.value: "1000",
            QuoteField.CHANGE_RATE.value: "2.0",
            QuoteField.CUMULATIVE_VOLUME.value: "1000000",
            QuoteField.TRADE_VOLUME.value: "5000",
        }

        data = QuoteData.from_values(values)

        assert data.current_price == 50000.0
        assert data.change == 1000.0
        assert data.change_rate == 2.0
        assert data.cumulative_volume == 1000000
        assert data.trade_volume == 5000

    def test_from_values_with_nulls(self):
        """null 값 처리 테스트"""
        values = {
            QuoteField.CURRENT_PRICE.value: None,
            QuoteField.CHANGE.value: "",
            QuoteField.CUMULATIVE_VOLUME.value: "invalid",
        }

        data = QuoteData.from_values(values)

        assert data.current_price == 0.0
        assert data.change == 0.0
        assert data.cumulative_volume == 0

    def test_all_fields(self):
        """모든 필드 변환 테스트"""
        values = {
            QuoteField.EXECUTION_TIME.value: "153000",
            QuoteField.CURRENT_PRICE.value: "50000",
            QuoteField.CHANGE.value: "1000",
            QuoteField.CHANGE_RATE.value: "2.0",
            QuoteField.OPEN_PRICE.value: "49000",
            QuoteField.HIGH_PRICE.value: "51000",
            QuoteField.LOW_PRICE.value: "48500",
            QuoteField.CUMULATIVE_VOLUME.value: "1000000",
            QuoteField.CUMULATIVE_AMOUNT.value: "50000000000",
            QuoteField.BUY_EXEC_QTY.value: "600000",
            QuoteField.SELL_EXEC_QTY.value: "400000",
        }

        data = QuoteData.from_values(values)

        assert data.execution_time == "153000"
        assert data.current_price == 50000.0
        assert data.change == 1000.0
        assert data.change_rate == 2.0
        assert data.open_price == 49000.0
        assert data.high_price == 51000.0
        assert data.low_price == 48500.0
        assert data.cumulative_volume == 1000000
        assert data.cumulative_amount == 50000000000.0
        assert data.buy_exec_qty == 600000
        assert data.sell_exec_qty == 400000


class TestOrderField:
    """OrderField Enum 테스트"""

    def test_order_fields(self):
        """주문 필드 상수 테스트"""
        assert OrderField.ACCOUNT_NO.value == "9201"
        assert OrderField.ORDER_NO.value == "9203"
        assert OrderField.STOCK_CODE.value == "9001"
        assert OrderField.ORDER_STATUS.value == "913"
        assert OrderField.ORDER_QTY.value == "900"
        assert OrderField.ORDER_PRICE.value == "901"
        assert OrderField.EXECUTION_PRICE.value == "910"
        assert OrderField.EXECUTION_QTY.value == "911"
        assert OrderField.SELL_BUY_DIVISION.value == "907"


class TestQuoteField:
    """QuoteField Enum 테스트"""

    def test_quote_fields(self):
        """시세 필드 상수 테스트"""
        assert QuoteField.CURRENT_PRICE.value == "10"
        assert QuoteField.CHANGE.value == "11"
        assert QuoteField.CHANGE_RATE.value == "12"
        assert QuoteField.OPEN_PRICE.value == "16"
        assert QuoteField.HIGH_PRICE.value == "17"
        assert QuoteField.LOW_PRICE.value == "18"
        assert QuoteField.CUMULATIVE_VOLUME.value == "13"
        assert QuoteField.CUMULATIVE_AMOUNT.value == "14"
        assert QuoteField.TRADE_VOLUME.value == "15"
        assert QuoteField.BUY_EXEC_QTY.value == "1031"


class TestRealtimeType:
    """RealtimeType 테스트"""

    def test_order_types(self):
        """주문 타입 테스트"""
        assert RealtimeType.ORDER_EXECUTION.value == "0A"

    def test_stock_types(self):
        """주식 타입 테스트"""
        assert RealtimeType.STOCK_CURRENT.value == "0B"
        assert RealtimeType.STOCK_QUOTE.value == "0C"
        assert RealtimeType.STOCK_EXECUTION.value == "0F"

    def test_market_status_type(self):
        """장상태 타입 테스트"""
        assert RealtimeType.MARKET_STATUS.value == "90"


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

        client.register_handler("0A", handler)
        assert "0A" in client._message_handlers
        assert handler in client._message_handlers["0A"]

    def test_unregister_handler(self):
        """핸들러 해제 테스트"""
        client = WebSocketClient("ws://test.com", "test_token")

        def handler(msg):
            pass

        client.register_handler("0A", handler)
        client.unregister_handler("0A", handler)
        assert handler not in client._message_handlers["0A"]

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

    @pytest.mark.asyncio
    async def test_register_subscription(self):
        """구독 등록 테스트"""
        client = WebSocketClient("ws://test.com", "test_token")
        client.connected = True

        # WebSocket mock
        mock_ws = AsyncMock()
        client.websocket = mock_ws

        # 주문 체결 구독
        grp_no = await client.register(
            items=[""],  # 주문은 빈 문자열
            types=["0A"],
            grp_no="0"
        )

        assert grp_no == "0"
        assert "0" in client._subscriptions
        assert client._subscriptions["0"].items == [""]
        assert client._subscriptions["0"].types == ["0A"]

    @pytest.mark.asyncio
    async def test_register_quote_subscription(self):
        """시세 구독 테스트"""
        client = WebSocketClient("ws://test.com", "test_token")
        client.connected = True

        # WebSocket mock
        mock_ws = AsyncMock()
        client.websocket = mock_ws

        # 시세 구독
        grp_no = await client.register(
            items=["005930", "000660"],
            types=["0B"],
            grp_no="1"
        )

        assert grp_no == "1"
        assert "1" in client._subscriptions
        assert client._subscriptions["1"].items == ["005930", "000660"]
        assert client._subscriptions["1"].types == ["0B"]

    @pytest.mark.asyncio
    async def test_deregister(self):
        """구독 해지 테스트"""
        client = WebSocketClient("ws://test.com", "test_token")
        client.connected = True

        # WebSocket mock
        mock_ws = AsyncMock()
        client.websocket = mock_ws

        # 구독 후 해지
        await client.register(items=["005930"], types=["0B"], grp_no="1")
        assert "1" in client._subscriptions

        await client.deregister("1")
        assert "1" not in client._subscriptions

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
    async def test_order_execution_message_handling(self):
        """주문 체결 메시지 핸들링 테스트"""
        client = WebSocketClient("ws://test.com", "test_token")
        client.connected = True

        # 핸들러 등록
        handler_called = False
        received_data = None

        def handler(msg):
            nonlocal handler_called, received_data
            handler_called = True
            received_data = msg

        client.register_handler("0A", handler)

        # WebSocket mock
        test_message = {
            "trnm": "0A",
            "data": [{
                "item": "005930",
                "type": "0A",
                "values": [
                    "", "", "",  # 9201-9205
                    "005930", "1", "체결", "삼성전자",  # 9001, 912, 913, 302
                    "100", "50000", "50",  # 900, 901, 902
                    "", "", "", "",  # 903-906
                    "2", "153000", "",  # 907, 908, 909
                    "50000", "100",  # 910, 911
                ]
            }]
        }

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
        assert received_data == test_message


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

    def test_order_subscription(self):
        """주문 구독 테스트"""
        sub = Subscription(
            grp_no="0",
            items=[""],  # 주문은 빈 문자열
            types=["0A"]
        )

        assert sub.grp_no == "0"
        assert sub.items == [""]
        assert sub.types == ["0A"]
