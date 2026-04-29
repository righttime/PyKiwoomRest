"""실시간 데이터 스트리밍 테스트"""

import asyncio
import sys
from pathlib import Path

# 프로젝트 경로 추가
sys.path.insert(0, str(Path(__file__).parent))

from pykiwoomrest import RealtimeAPI, KiwoomConfig
from dotenv import load_dotenv
import os

load_dotenv()


async def test_realtime_basic():
    """기본 실시간 데이터 테스트"""

    # 토큰 가져오기
    config = KiwoomConfig.from_env()
    token = config.api_key  # 실제로는 access_token 필요

    # RealtimeAPI 생성
    realtime = RealtimeAPI(access_token=token, mock=config.mock)

    # WebSocket 클라이언트 생성
    client = realtime.create_client()

    # 핸들러 등록
    def on_quote(message):
        """시세 핸들러"""
        print(f"📊 시세 수신: {message}")

    def on_market_status(message):
        """장상태 핸들러"""
        print(f"🔔 장상태 수신: {message}")

    def on_reg_response(message):
        """등록 응답 핸들러"""
        if message.get('return_code') == 0:
            print(f"✅ 등록 성공: {message.get('return_msg')}")
        else:
            print(f"❌ 등록 실패: {message.get('return_msg')}")

    client.register_handler("0B", on_quote)
    client.register_handler("90", on_market_status)
    client.register_handler("REG", on_reg_response)

    # 백그라운드 실행
    await client.start()

    # 장상태 구독 (90: 장상태)
    await asyncio.sleep(1)
    await client.register(
        items=[""],  # 장상태는 종목 코드 없음
        types=["90"],  # 장상태 타입
        grp_no="0"
    )

    # 삼성전자 시세 구독
    await asyncio.sleep(1)
    await client.register(
        items=["005930"],
        types=["0B"],  # 현재가
        grp_no="1"
    )

    # 30초 동안 수신
    print("30초 동안 실시간 데이터 수신...")
    await asyncio.sleep(30)

    # 정리
    await client.stop()
    print("테스트 완료")


async def test_realtime_with_context():
    """Context manager 사용 테스트"""

    config = KiwoomConfig.from_env()
    realtime = RealtimeAPI(access_token=config.api_key, mock=config.mock)

    async with realtime.create_client() as client:
        # 핸들러 등록
        def handler(message):
            print(f"수신: {message}")

        client.register_handler("0B", handler)

        # 구독
        await client.register(
            items=["005930", "000660"],
            types=["0B", "0C"],
            grp_no="1"
        )

        # 10초 동안 수신
        await asyncio.sleep(10)


async def test_realtime_market_status():
    """장상태만 구독하는 테스트"""

    config = KiwoomConfig.from_env()
    realtime = RealtimeAPI(access_token=config.api_key, mock=config.mock)
    client = realtime.create_client()

    # 장상태 핸들러
    def on_market_status(message):
        tr_type = message.get('tr_type')  # 1:장시작전, 2:장중, 3:장종료
        if tr_type == "1":
            print("🟢 장 시작 전")
        elif tr_type == "2":
            print("🟡 장 중")
        elif tr_type == "3":
            print("🔴 장 종료")

        print(f"장상태 상세: {message}")

    client.register_handler("90", on_market_status)

    # 실행
    await client.start()

    # 장상태만 구독
    await asyncio.sleep(1)
    await client.register(
        items=[""],
        types=["90"],
        grp_no="0"
    )

    # 1분 동안 장상태 모니터링
    print("장상태 모니터링 (1분)...")
    await asyncio.sleep(60)

    await client.stop()


async def main():
    """메인 함수"""
    print("=" * 60)
    print("실시간 데이터 스트리밍 테스트")
    print("=" * 60)

    try:
        # 기본 테스트
        await test_realtime_basic()
    except KeyboardInterrupt:
        print("\n사용자 중단")
    except Exception as e:
        print(f"\n오류: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
