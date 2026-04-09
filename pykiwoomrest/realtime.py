"""실시간 WebSocket — wss://api.kiwoom.com:10000/api/dostk/websocket"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Callable, Coroutine

import websockets

from .config import KiwoomConfig

logger = logging.getLogger("pykiwoomrest.realtime")

# 실시간 데이터 타입
REALTIME_TYPES = {
    "00": "주문체결",
    "04": "잔고",
    "0A": "주식기세",
    "0B": "주식체결",
    "0C": "주식우선호가",
    "0D": "주식호가잔량",
    "0E": "주식시간외호가",
    "0F": "주식당일거래원",
    "0G": "ETF NAV",
    "0H": "주식예상체결",
    "0J": "업종지수",
    "0U": "업종등락",
    "0g": "주식종목정보",
    "1h": "VI발동/해제",
}


class RealtimeClient:
    """키움 실시간 WebSocket 클라이언트

    Usage:
        rt = RealtimeClient(config)
        rt.on("0B", lambda data: print(data))
        await rt.connect()
        await rt.subscribe("0B", "005930")
        await rt.listen()
    """

    def __init__(self, config: KiwoomConfig, token: str | None = None) -> None:
        self._config = config
        self._token = token
        self._ws: websockets.WebSocketClientProtocol | None = None
        self._callbacks: dict[str, list[Callable]] = {}
        self._running = False

    @property
    def ws_url(self) -> str:
        if self._config.mock:
            return "wss://mockapi.kiwoom.com:10000/api/dostk/websocket"
        return "wss://api.kiwoom.com:10000/api/dostk/websocket"

    def on(self, realtime_type: str, callback: Callable) -> None:
        """콜백 등록

        Args:
            realtime_type: "0B" (체결), "0D" (호가), "00" (주문체결) 등
            callback: async def callback(data: dict) -> None
        """
        if realtime_type not in self._callbacks:
            self._callbacks[realtime_type] = []
        self._callbacks[realtime_type].append(callback)

    def off(self, realtime_type: str, callback: Callable | None = None) -> None:
        """콜백 해제"""
        if callback:
            self._callbacks.get(realtime_type, []).remove(callback)
        else:
            self._callbacks.pop(realtime_type, None)

    async def connect(self) -> None:
        """WebSocket 연결"""
        headers = {}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"

        self._ws = await websockets.connect(
            self.ws_url,
            additional_headers=headers,
            ping_interval=60,
            ping_timeout=10,
        )
        self._running = True
        logger.info("WebSocket 연결됨: %s", self.ws_url)

    async def disconnect(self) -> None:
        """WebSocket 연결 해제"""
        self._running = False
        if self._ws:
            await self._ws.close()
            self._ws = None

    async def subscribe(self, realtime_type: str, codes: str | list[str]) -> None:
        """실시간 데이터 구독

        Args:
            realtime_type: "0B", "0D" 등
            codes: 종목코드 또는 종목코드 리스트
        """
        if isinstance(codes, str):
            codes = [codes]

        message = {
            "trnm": "REG",
            "data": [{"item": code, "type": realtime_type} for code in codes],
        }
        await self._send(message)
        logger.info("구독: %s %s", realtime_type, codes)

    async def unsubscribe(self, realtime_type: str, codes: str | list[str]) -> None:
        """실시간 데이터 구독 해제"""
        if isinstance(codes, str):
            codes = [codes]

        message = {
            "trnm": "REMOVE",
            "data": [{"item": code, "type": realtime_type} for code in codes],
        }
        await self._send(message)
        logger.info("구독해제: %s %s", realtime_type, codes)

    async def _send(self, message: dict) -> None:
        if not self._ws:
            raise RuntimeError("WebSocket이 연결되지 않았습니다. connect()를 먼저 호출하세요.")
        await self._ws.send(json.dumps(message))

    async def listen(self) -> None:
        """메시지 수신 대기 (blocking)"""
        if not self._ws:
            raise RuntimeError("WebSocket이 연결되지 않았습니다.")

        async for raw in self._ws:
            try:
                data = json.loads(raw)
                await self._dispatch(data)
            except json.JSONDecodeError:
                logger.warning("JSON 파싱 실패: %s", raw[:100])
            except Exception as e:
                logger.error("메시지 처리 에러: %s", e)

    async def _dispatch(self, data: dict) -> None:
        """수신 데이터를 콜백으로 전달"""
        realtime_type = data.get("type", "")
        if realtime_type in self._callbacks:
            for cb in self._callbacks[realtime_type]:
                result = cb(data)
                if asyncio.iscoroutine(result):
                    await result
