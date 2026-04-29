"""실시간 데이터 스트리밍 테스트"""

import asyncio
import sys
from pathlib import Path

# 프로젝트 경로 추가
sys.path.insert(0, str(Path(__file__).parent))

from pykiwoomrest import (
    RealtimeAPI,
    RealtimeType,
    OrderExecutionData,
    OrderField,
    QuoteData,
    QuoteField,
    KiwoomConfig
)
from dotenv import load_dotenv
import os

load_dotenv()


async def test_order_execution():
    """주문/체결 실시간 수신 테스트 (0A)"""

    config = KiwoomConfig.from_env()
    token = config.api_key

    realtime = RealtimeAPI(access_token=token, mock=config.mock)
    client = realtime.create_client()

    # 주문/체결 핸들러
    def on_order_execution(message):
        print("\n" + "=" * 60)
        print("📋 주문/체결 수신 (0A)")
        print("=" * 60)

        for data in message.get('data', []):
            # values 리스트를 딕셔너리로 변환
            values = {}
            field_list = list(OrderField)
            values_list = data.get('values', [])

            for i, value in enumerate(values_list):
                if i < len(field_list):
                    values[field_list[i].value] = value

            # 데이터클래스로 변환
            order_data = OrderExecutionData.from_values(values)

            print(f"📦 {order_data.stock_name}({order_data.stock_code})")
            print(f"  주문번호: {order_data.order_no}")
            print(f"  주문상태: {order_data.order_status}")
            print(f"  주문구분: {order_data.order_division}")
            print(f"  매매구분: {order_data.sell_buy_division} (1:매도, 2:매수)")

            if order_data.order_status in ["체결", "확인"]:
                print(f"  체결가: {order_data.execution_price:,.0f}원")
                print(f"  체결량: {order_data.execution_qty:,}주")
                print(f"  체결시간: {order_data.order_time}")
                print(f"  미체결: {order_data.unfilled_qty:,}주")
            elif order_data.order_status == "취소":
                print(f"  취소사유: {order_data.reject_reason or '사용자 취소'}")
            elif order_data.order_status == "거부":
                print(f"  거부사유: {order_data.reject_reason}")

        print("=" * 60)

    client.register_handler("0A", on_order_execution)

    # 백그라운드 실행
    await client.start()

    # 주문/체결 구독 (items는 빈 문자열)
    print("주문/체결 구독 중...")
    await asyncio.sleep(1)
    await client.register(items=[""], types=["0A"], grp_no="0")

    # 60초 동안 수신
    print("60초 동안 주문/체결 수신 대기...")
    print("(매수/매도 주문을 내보면 실시간으로 수신됩니다)")
    await asyncio.sleep(60)

    # 정리
    await client.stop()


async def test_quote():
    """시세 실시간 수신 테스트 (0B)"""

    config = KiwoomConfig.from_env()
    token = config.api_key

    realtime = RealtimeAPI(access_token=token, mock=config.mock)
    client = realtime.create_client()

    # 시세 핸들러
    def on_quote(message):
        print("\n" + "=" * 60)
        print("📊 시세 수신 (0B)")
        print("=" * 60)

        for data in message.get('data', []):
            stock_code = data.get('item', '')

            # values 리스트를 딕셔너리로 변환
            values = {}
            field_list = list(QuoteField)
            values_list = data.get('values', [])

            for i, value in enumerate(values_list):
                if i < len(field_list):
                    values[field_list[i].value] = value

            # 데이터클래스로 변환
            quote = QuoteData.from_values(values)

            # 종목명 (raw 데이터에서 가져오기)
            stock_name = values.get(QuoteField.STOCK_NAME.value, stock_code)

            print(f"📈 {stock_name}({stock_code})")
            print(f"  현재가: {quote.current_price:,.0f}원")

            if quote.change > 0:
                print(f"  전일대비: ▲{quote.change:+,}원 ({quote.change_rate:+.2f}%)")
            elif quote.change < 0:
                print(f"  전일대비: ▼{quote.change:+,}원 ({quote.change_rate:+.2f}%)")
            else:
                print(f"  전일대비: {quote.change:+,}원 ({quote.change_rate:+.2f}%)")

            print(f"  거래량: {quote.cumulative_volume:,}주")
            print(f"  거래대금: {quote.cumulative_amount:,.0f}원")
            print(f"  매수비율: {quote.buy_ratio:.1f}%")

            if quote.session_division == "1":
                print(f"  장구분: 장전 시간외")
            elif quote.session_division == "2":
                print(f"  장구분: 장중")
            elif quote.session_division == "3":
                print(f"  장구분: 장후 시간외")

        print("=" * 60)

    client.register_handler("0B", on_quote)

    # 백그라운드 실행
    await client.start()

    # 시세 구독
    print("시세 구독 중...")
    await asyncio.sleep(1)
    await client.register(
        items=["005930", "000660"],  # 삼성전자, SK하이닉스
        types=["0B"],  # 현재가
        grp_no="1"
    )

    # 30초 동안 수신
    print("30초 동안 시세 수신 대기...")
    await asyncio.sleep(30)

    # 정리
    await client.stop()


async def test_market_status():
    """장상태만 구독하는 테스트 (90)"""

    config = KiwoomConfig.from_env()
    token = config.api_key
    realtime = RealtimeAPI(access_token=token, mock=config.mock)
    client = realtime.create_client()

    # 장상태 핸들러
    def on_market_status(message):
        print("\n" + "=" * 60)
        print("🔔 장상태 수신 (90)")
        print("=" * 60)

        for data in message.get('data', []):
            tr_type = data.get('values', [None])[0] if data.get('values') else None

            if tr_type == "1":
                print("🟢 장 시작 전")
            elif tr_type == "2":
                print("🟡 장 중")
            elif tr_type == "3":
                print("🔴 장 종료")

            print(f"장상태 상세: {data}")

        print("=" * 60)

    client.register_handler("90", on_market_status)

    # 실행
    await client.start()

    # 장상태만 구독
    print("장상태 구독 중...")
    await asyncio.sleep(1)
    await client.register(
        items=[""],  # 장상태는 종목 코드 없음
        types=["90"],  # 장상태 타입
        grp_no="0"
    )

    # 1분 동안 장상태 모니터링
    print("장상태 모니터링 (1분)...")
    await asyncio.sleep(60)

    await client.stop()


async def test_combined():
    """주문/체결 + 시세 + 장상태 통합 테스트"""

    config = KiwoomConfig.from_env()
    token = config.api_key
    realtime = RealtimeAPI(access_token=token, mock=config.mock)
    client = realtime.create_client()

    # 각 핸들러 등록
    def on_order_execution(message):
        print(f"\n📋 주문/체결: {len(message.get('data', []))}개")

    def on_quote(message):
        data = message.get('data', [])
        if data:
            stock_code = data[0].get('item', '')
            print(f"📊 시세 업데이트: {stock_code}")

    def on_market_status(message):
        print(f"\n🔔 장상태 업데이트")

    client.register_handler("0A", on_order_execution)
    client.register_handler("0B", on_quote)
    client.register_handler("90", on_market_status)

    # 백그라운드 실행
    await client.start()

    # 모든 구독 등록
    await asyncio.sleep(1)

    # 장상태
    await client.register(items=[""], types=["90"], grp_no="0")

    # 시세
    await client.register(
        items=["005930", "000660"],
        types=["0B"],
        grp_no="1"
    )

    # 주문/체결
    await client.register(items=[""], types=["0A"], grp_no="2")

    # 2분 동안 수신
    print("통합 실시간 수신 (2분)...")
    await asyncio.sleep(120)

    # 정리
    await client.stop()


async def main():
    """메인 함수"""
    print("=" * 60)
    print("실시간 데이터 스트리밍 테스트")
    print("=" * 60)

    import sys
    if len(sys.argv) > 1:
        test_type = sys.argv[1]

        if test_type == "order":
            await test_order_execution()
        elif test_type == "quote":
            await test_quote()
        elif test_type == "market":
            await test_market_status()
        elif test_type == "combined":
            await test_combined()
        else:
            print(f"알 수 없는 테스트 타입: {test_type}")
            print("사용법: python test_realtime.py [order|quote|market|combined]")
    else:
        # 기본: 시세 테스트
        await test_quote()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n사용자 중단")
    except Exception as e:
        print(f"\n오류: {e}")
        import traceback
        traceback.print_exc()
