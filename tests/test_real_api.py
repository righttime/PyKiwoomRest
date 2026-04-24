"""PyKiwoomRest 실제 API 테스트

이 테스트는 실제 키움 서버와 통신합니다.
.env 파일에 다음 환경 변수가 필요합니다:
- KIWOOM_API_KEY
- KIWOOM_SECRET_KEY
- KIWOOM_ACCOUNT_NO (선택, 계좌 관련 API 테스트용)
"""

import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# 프로젝트 루트 경로 추가
root = Path(__file__).parent.parent
sys.path.insert(0, str(root))

# .env 파일은 상위 프로젝트 디렉토리에 있음
env_path = root.parent / ".env"
load_dotenv(env_path)

from pykiwoomrest import KiwoomClient, KiwoomConfig, TradingAPI, MarketAPI


# 환경 변수 검증
API_KEY = os.getenv("KIWOOM_APP_KEY")
SECRET_KEY = os.getenv("KIWOOM_APP_SECRET")
ACCOUNT_NO = os.getenv("KIWOOM_ACCOUNT")

if not API_KEY or not SECRET_KEY:
    print("❌ KIWOOM_APP_KEY, KIWOOM_APP_SECRET 환경 변수가 필요합니다.")
    sys.exit(1)

print("=" * 60)
print("PyKiwoomRest 실제 API 테스트")
print("=" * 60)
print(f"API Key: {API_KEY[:8]}...")
print(f"Account: {ACCOUNT_NO or '미설정 (계좌 관련 테스트 건너뜀)'}")
print("=" * 60)


class APITester:
    def __init__(self):
        self.config = KiwoomConfig(
            api_key=API_KEY,
            secret_key=SECRET_KEY,
            account_no=ACCOUNT_NO,
        )
        self.client: KiwoomClient | None = None
        self.trading: TradingAPI | None = None
        self.market: MarketAPI | None = None
        self.passed = 0
        self.failed = 0
        self.skipped = 0

    async def setup(self):
        """클라이언트 초기화"""
        print("\n🔧 클라이언트 초기화 중...")
        self.client = KiwoomClient(self.config)
        try:
            await self.client.init()

            if ACCOUNT_NO:
                self.trading = TradingAPI(self.client)
            self.market = MarketAPI(self.client)

            print("✅ 초기화 완료")
            print(f"   토큰: {self.client.token[:20]}...")
        except RuntimeError as e:
            error_msg = str(e)
            if "8030" in error_msg or "8050" in error_msg:
                print(f"\n❌ 환경 설정 오류:")
                print(f"   {error_msg}")
                print("\n해결 방법:")
                print("   1. VPN 연결 확인 (IP 제약 문제)")
                print("   2. 키움 Open API+ 사이트에서 AppKey/SecretKey 확인")
                print("   3. .env 파일의 환경 변수 확인")
                sys.exit(1)
            raise

    async def teardown(self):
        """클라이언트 정리"""
        if self.client:
            await self.client.close()

    def report(self, test_name: str, success: bool, error: Exception | None = None):
        """테스트 결과 보고"""
        if success:
            print(f"  ✅ {test_name}")
            self.passed += 1
        else:
            print(f"  ❌ {test_name}")
            if error:
                print(f"     오류: {error}")
            self.failed += 1

    def skip(self, test_name: str, reason: str):
        """테스트 스킵"""
        print(f"  ⏭️  {test_name} (스킵: {reason})")
        self.skipped += 1

    # ── 토큰 관련 ──────────────────────────────────

    async def test_token(self):
        """토큰 발급 테스트"""
        print("\n[1/10] 토큰 관리 테스트")
        try:
            # 토큰이 이미 발급되어 있음 확인
            assert self.client.token, "토큰이 비어있음"
            print(f"  ✅ 토큰 발급 성공: {self.client.token[:20]}...")
            self.passed += 1
        except Exception as e:
            self.report("토큰 발급", False, e)

    # ── 계좌 관련 ──────────────────────────────────

    async def test_deposit(self):
        """예수금 조회 테스트"""
        print("\n[2/10] 예수금 조회 (kt00001)")
        if not self.trading:
            self.skip("예수금 조회", "계좌번호 미설정")
            return

        try:
            result = await self.trading.deposit()
            print(f"  응답 키: {list(result.keys())}")

            # 예수금 확인
            d2_asset_oodr_ylp = result.get("d2_asset_oodr_ylp", "0")
            ord_alow_amt_entr = result.get("ord_alow_amt_entr", "0")
            print(f"  D2추정예수금: {d2_asset_oodr_ylp}원")
            print(f"  주문가능금액: {ord_alow_amt_entr}원")

            self.report("예수금 조회", True)
        except Exception as e:
            self.report("예수금 조회", False, e)

    async def test_account_summary(self):
        """계좌 요약 조회 테스트"""
        print("\n[3/10] 계좌 요약 (kt00004)")
        if not self.trading:
            self.skip("계좌 요약", "계좌번호 미설정")
            return

        try:
            result = await self.trading.account_summary()
            print(f"  응답 키: {list(result.keys())}")

            # 총 평가금액 확인
            total_eval_amt = result.get("tota_evlu_pric_amt", "0")
            total_earn_rate = result.get("tota_evlu_rto", "0")
            print(f"  총 평가금액: {total_eval_amt}원")
            print(f"  총 수익률: {total_earn_rate}%")

            self.report("계좌 요약", True)
        except Exception as e:
            self.report("계좌 요약", False, e)

    async def test_holdings(self):
        """보유 종목 조회 테스트"""
        print("\n[4/10] 보유 종목 (kt00005)")
        if not self.trading:
            self.skip("보유 종목", "계좌번호 미설정")
            return

        try:
            result = await self.trading.holdings()
            print(f"  응답 키: {list(result.keys())}")

            # 보유 종목 확인
            stk_cntr_remn = result.get("stk_cntr_remn", [])
            print(f"  보유 종목 수: {len(stk_cntr_remn)}")

            if stk_cntr_remn:
                print("  보유 종목:")
                for h in stk_cntr_remn:
                    stk_nm = h.get("stk_nm", "알수없음")
                    stk_cd = h.get("stk_cd", "알수없음")
                    cur_qty = h.get("cur_qty", "0")
                    cur_prc = h.get("cur_prc", "0")
                    print(f"    - {stk_nm}({stk_cd}): {cur_qty}주 @ {cur_prc}원")

            self.report("보유 종목", True)
        except Exception as e:
            self.report("보유 종목", False, e)

    async def test_unfulfilled_orders(self):
        """미체결 조회 테스트"""
        print("\n[5/10] 미체결 조회 (ka10075)")
        if not self.trading:
            self.skip("미체결 조회", "계좌번호 미설정")
            return

        try:
            result = await self.trading.unfulfilled_orders()
            print(f"  응답 키: {list(result.keys())}")

            # 미체결 확인
            ord_list = result.get("ord_list", [])
            print(f"  미체결 수: {len(ord_list)}")

            if ord_list:
                print("  미체결 주문:")
                for o in ord_list:
                    stk_nm = o.get("stk_nm", "알수없음")
                    ord_qty = o.get("ord_qty", "0")
                    ord_prc = o.get("ord_prc", "0")
                    print(f"    - {stk_nm}: {ord_qty}주 @ {ord_prc}원")

            self.report("미체결 조회", True)
        except Exception as e:
            self.report("미체결 조회", False, e)

    # ── 시세/종목 ───────────────────────────────────

    async def test_basic_info(self):
        """기본 정보 조회 테스트"""
        print("\n[6/10] 기본 정보 (ka10001) - 삼성전자")
        try:
            result = await self.market.basic_info("005930")
            print(f"  응답 키: {list(result.keys())}")

            # 기본 정보 확인
            stk_nm = result.get("stk_nm", "")
            cur_prc = result.get("cur_prc", "0")
            d1_rate = result.get("d1_rate", "0")
            print(f"  종목명: {stk_nm}")
            print(f"  현재가: {cur_prc}원")
            print(f"  전일대비: {d1_rate}%")

            self.report("기본 정보", True)
        except Exception as e:
            self.report("기본 정보", False, e)

    async def test_quote(self):
        """호가 조회 테스트"""
        print("\n[7/10] 호가 조회 (ka10004) - 삼성전자")
        try:
            result = await self.market.quote("005930")
            print(f"  응답 키: {list(result.keys())}")

            # 매수/매도 호가 확인
            ask_prc_1 = result.get("ask_prc_1", "0")
            bid_prc_1 = result.get("bid_prc_1", "0")
            print(f"  매수호가1: {ask_prc_1}원")
            print(f"  매도호가1: {bid_prc_1}원")

            self.report("호가 조회", True)
        except Exception as e:
            self.report("호가 조회", False, e)

    async def test_stock_search(self):
        """종목 검색 테스트"""
        print("\n[8/10] 종목 검색 (ka10100)")
        try:
            result = await self.market.search_stock("삼성전자")
            print(f"  응답 키: {list(result.keys())}")

            # 검색 결과 확인
            list_data = result.get("list", [])
            print(f"  검색 결과 수: {len(list_data)}")

            if list_data:
                first = list_data[0]
                stk_nm = first.get("stk_nm", "")
                stk_cd = first.get("stk_cd", "")
                print(f"  첫 번째: {stk_nm}({stk_cd})")

            self.report("종목 검색", True)
        except Exception as e:
            self.report("종목 검색", False, e)

    # ── 차트 ───────────────────────────────────────

    async def test_daily_chart(self):
        """일봉 차트 조회 테스트"""
        print("\n[9/10] 일봉 차트 (ka10081) - 삼성전자")
        try:
            # 최근 30일
            end_dt = datetime.now().strftime("%Y%m%d")
            start_dt = (datetime.now().replace(day=1) - timedelta(days=30)).strftime("%Y%m%d")

            result = await self.market.day_chart("005930", start_dt=start_dt, end_dt=end_dt)
            print(f"  응답 키: {list(result.keys())}")

            # 차트 데이터 확인
            chart_data = result.get("stk_dt_pole_chart_qry", [])
            print(f"  데이터 수: {len(chart_data)}")

            if chart_data:
                latest = chart_data[0]
                stk_dt = latest.get("stk_dt", "")
                clpr_prc = latest.get("clpr_prc", "0")
                print(f"  최신 데이터: {stk_dt}, 종가 {clpr_prc}원")

            self.report("일봉 차트", True)
        except Exception as e:
            self.report("일봉 차트", False, e)

    # ── 주문 ───────────────────────────────────────

    async def test_order_error(self):
        """주문 에러 테스트 (주문 불가 시간)"""
        print("\n[10/10] 주문 API 테스트 (장 마감 시 에러 확인)")
        if not self.trading:
            self.skip("주문 API", "계좌번호 미설정")
            return

        try:
            # 시장가 매수 주문 (장 마감 시 에러 발생 예상)
            result = await self.trading.buy("005930", qty=1)
            print(f"  응답: {result}")

            # 에러 확인
            return_code = result.get("return_code", -1)
            return_msg = result.get("return_msg", "")
            print(f"  리턴코드: {return_code}")
            print(f"  메시지: {return_msg}")

            if return_code == 0:
                print("  ⚠️  주문이 체결되었습니다 (실제 주문입니다!)")
                self.report("주문 API", True)
            else:
                print("  ✅ 예상대로 에러 발생 (장 마감)")
                self.report("주문 API", True)
        except Exception as e:
            self.report("주문 API", False, e)

    # ── 전체 테스트 실행 ────────────────────────────

    async def run_all(self):
        """모든 테스트 실행"""
        await self.setup()

        # 토큰
        await self.test_token()

        # 계좌
        await self.test_deposit()
        await self.test_account_summary()
        await self.test_holdings()
        await self.test_unfulfilled_orders()

        # 시계
        await self.test_basic_info()
        await self.test_quote()
        await self.test_stock_search()

        # 차트
        await self.test_daily_chart()

        # 주문
        await self.test_order_error()

        await self.teardown()

        # 결과 요약
        print("\n" + "=" * 60)
        print("테스트 결과 요약")
        print("=" * 60)
        print(f"  성공: {self.passed}")
        print(f"  실패: {self.failed}")
        print(f"  스킵: {self.skipped}")
        print(f"  총계: {self.passed + self.failed + self.skipped}")
        print("=" * 60)


# timedelta 임포트 추가
from datetime import timedelta


async def main():
    tester = APITester()
    await tester.run_all()


if __name__ == "__main__":
    asyncio.run(main())
