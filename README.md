# PyKiwoomRest - 키움증권 REST API Python 래퍼

키움증권 REST API를 Python에서 쉽게 사용할 수 있는 비동기 래퍼 라이브러리입니다.

## 설치

```bash
cd PyKiwoomRest
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 설정

`.env.example`을 복사해서 `.env`를 만들고 API 키를 입력:

```bash
cp .env.example .env
# .env 편집
```

## 사용법

### 기본

```python
import asyncio
from pykiwoomrest import KiwoomClient, KiwoomConfig

async def main():
    config = KiwoomConfig.from_env()
    async with KiwoomClient(config) as client:
        # MarketAPI 사용 (시세, 차트)
        from pykiwoomrest.market import MarketAPI
        market = MarketAPI(client)

        # 삼성전자 기본 정보
        info = await market.basic_info("005930")
        print(info)

asyncio.run(main())
```

### 시세 조회

```python
from pykiwoomrest.market import MarketAPI

market = MarketAPI(client)

# 주식기본정보
info = await market.basic_info("005930")

# 일봉차트
chart = await market.day_chart("005930")

# 종목 검색
result = await market.search_stock("삼성전자")

# 호가
quote = await market.quote("005930")
```

### 순위 조회

```python
from pykiwoomrest.rank import RankAPI

rank = RankAPI(client)

# 거래량 상위
top_volume = await rank.volume_rank()

# 등락률 상위
top_change = await rank.change_rate_rank()
```

### 외국인/기관

```python
from pykiwoomrest.foreign import ForeignAPI

foreign = ForeignAPI(client)

# 종목별 외국인 매매동향
data = await foreign.foreign_trade_by_stock("005930")
```

### 계좌 & 매매 (⚠️ 주의)

```python
from pykiwoomrest.trading import TradingAPI

trading = TradingAPI(client)

# 예수금 조회
deposit = await trading.deposit()

# 계좌 평가
summary = await trading.account_summary()

# 보유 종목
holdings = await trading.holdings()

# 매수 (시장가)
result = await trading.buy("005930", 10)

# 매수 (지정가)
result = await trading.buy("005930", 10, price=60000)

# 매도
result = await trading.sell("005930", 5, price=61000)
```

## 테스트

```bash
pytest -v
```

## 모의투자

`.env`에서 `KIWOOM_MOCK=true`로 설정하면 자동으로 모의투자 서버(`mockapi.kiwoom.com`)에 연결됩니다.

## 구조

```
pykiwoomrest/
├── __init__.py      # 패키지 진입점
├── config.py        # 설정 관리 (API 키, 모의/실전)
├── client.py        # KiwoomClient (토큰, HTTP 공통)
├── market.py        # 시세/차트 (ka1xxxx)
├── trading.py       # 매매/계좌 (kt0xxxx, kt1xxxx)
├── rank.py          # 순위 조회
├── foreign.py       # 외국인/기관
└── realtime.py      # 실시간 데이터 (WebSocket)
```

## 지원하는 키움 API 목록

### MarketAPI - 시세/종목/차트 조회

#### basic_info(stk_cd)
- **TR ID**: ka10001
- **설명**: 주식기본정보 (현재가, 전일대비, 등락률)
- **매개변수**: stk_cd (종목코드, 6자리)

#### trade_volume_by_firm(stk_cd)
- **TR ID**: ka10002
- **설명**: 주식거래원 (매수/매도 거래원)
- **매개변수**: stk_cd (종목코드)

#### execution_info(stk_cd)
- **TR ID**: ka10003
- **설명**: 체결정보
- **매개변수**: stk_cd (종목코드)

#### daily_trade_detail(stk_cd)
- **TR ID**: ka10015
- **설명**: 일별거래상세
- **매개변수**: stk_cd (종목코드)

#### stock_list(mrkt_tp="0")
- **TR ID**: ka10099
- **설명**: 종목정보리스트 (KOSPI/KOSDAQ 전체 종목)
- **매개변수**: mrkt_tp ("0"=KOSPI, "10"=KOSDAQ)

#### search_stock(keyword)
- **TR ID**: ka10100
- **설명**: 종목정보조회 (이름으로 종목 검색)
- **매개변수**: keyword (종목명)

#### tick_chart(stk_cd, **kwargs)
- **TR ID**: ka10079
- **설명**: 틱차트
- **매개변수**: stk_cd (종목코드), 추가 옵션 **kwargs

#### min_chart(stk_cd, **kwargs)
- **TR ID**: ka10080
- **설명**: 분봉차트
- **매개변수**: stk_cd (종목코드), 추가 옵션 **kwargs

#### day_chart(stk_cd, start_dt, end_dt, upd_stkpc_tp="1", base_dt="0")
- **TR ID**: ka10081
- **설명**: 일봉차트 (페이지네이션 자동 지원)
- **매개변수**: stk_cd (종목코드), start_dt (시작일), end_dt (종료일), upd_stkpc_tp (수정주가여부), base_dt (기준일)

#### week_chart(stk_cd, **kwargs)
- **TR ID**: ka10082
- **설명**: 주봉차트
- **매개변수**: stk_cd (종목코드), 추가 옵션 **kwargs

#### month_chart(stk_cd, **kwargs)
- **TR ID**: ka10083
- **설명**: 월봉차트
- **매개변수**: stk_cd (종목코드), 추가 옵션 **kwargs

#### year_chart(stk_cd, **kwargs)
- **TR ID**: ka10094
- **설명**: 년봉차트
- **매개변수**: stk_cd (종목코드), 추가 옵션 **kwargs

#### quote(stk_cd)
- **TR ID**: ka10004
- **설명**: 주식호가 (매수/매도 호가창)
- **매개변수**: stk_cd (종목코드)

#### daily_price(stk_cd, **kwargs)
- **TR ID**: ka10086
- **설명**: 일별주가 (과거 일별 주가)
- **매개변수**: stk_cd (종목코드), 추가 옵션 **kwargs

### TradingAPI - 매매/계좌 주문 및 조회

#### deposit()
- **TR ID**: kt00001
- **설명**: 예수금상세현황
- **매개변수**: 없음 (계좌번호는 config에서 자동 사용)

#### account_summary()
- **TR ID**: kt00004
- **설명**: 계좌평가현황 (총 평가금액, 수익률)
- **매개변수**: 없음

#### holdings()
- **TR ID**: kt00005
- **설명**: 체결잔고 (보유 종목별 잔고)
- **매개변수**: 없음

#### daily_profit_rate(qry_dt)
- **TR ID**: ka01690
- **설명**: 일별잔고수익률 (전체 계좌 현황 + 종목별 수익률)
- **매개변수**: qry_dt (조회일자, YYYYMMDD)

#### buy(stk_cd, qty, price=None)
- **TR ID**: kt10000
- **설명**: 매수주문 (지정가/시장가)
- **매개변수**: stk_cd (종목코드), qty (수량), price (가격, None=시장가)

#### sell(stk_cd, qty, price=None)
- **TR ID**: kt10001
- **설명**: 매도주문 (지정가/시장가)
- **매개변수**: stk_cd (종목코드), qty (수량), price (가격, None=시장가)

#### cancel_order(orig_ord_no, stk_cd, qty=None)
- **TR ID**: kt10003
- **설명**: 주문취소 (전량취소 또는 일부취소)
- **매개변수**: orig_ord_no (원주문번호), stk_cd (종목코드), qty (취소수량, None=전량)

#### modify_order(orig_ord_no, stk_cd, mdfy_qty, mdfy_price)
- **TR ID**: kt10002
- **설명**: 주문정정
- **매개변수**: orig_ord_no (원주문번호), stk_cd (종목코드), mdfy_qty (정정수량), mdfy_price (정정가격)

#### unfulfilled_orders(all_stk_tp="0", trde_tp="0", stk_cd="")
- **TR ID**: ka10075
- **설명**: 미체결조회
- **매개변수**: all_stk_tp ("0"=전체, "1"=특정종목), trde_tp ("0"=전체, "1"=매도, "2"=매수), stk_cd (종목코드, all_stk_tp="1"일 때 필수)

### RankAPI - 순위 조회

#### volume_rank(**kwargs)
- **TR ID**: ka10030
- **설명**: 당일거래량상위
- **매개변수**: 추가 옵션 **kwargs

#### value_rank(**kwargs)
- **TR ID**: ka10032
- **설명**: 거래대금상위
- **매개변수**: 추가 옵션 **kwargs

#### change_rate_rank(**kwargs)
- **TR ID**: ka10027
- **설명**: 등락률상위
- **매개변수**: 추가 옵션 **kwargs

#### orderbook_rank(**kwargs)
- **TR ID**: ka10020
- **설명**: 호가잔량상위
- **매개변수**: 추가 옵션 **kwargs

### ForeignAPI - 외국인/기관 매매동향

#### foreign_trade_by_stock(stk_cd)
- **TR ID**: ka10008
- **설명**: 외국인종목별매매동향
- **매개변수**: stk_cd (종목코드)

#### institution_trade(**kwargs)
- **TR ID**: ka10009
- **설명**: 주식기관요청
- **매개변수**: 추가 옵션 **kwargs

#### foreign_institution_rank(**kwargs)
- **TR ID**: ka90009
- **설명**: 외국인기관매매상위
- **매개변수**: 추가 옵션 **kwargs

### RealtimeAPI - 실시간 데이터 스트리밍

실시간 시세, 장상태, 주문 체결 등을 WebSocket을 통해 수신합니다.

#### 기본 사용법

```python
from pykiwoomrest import RealtimeAPI, RealtimeType

# RealtimeAPI 생성
realtime = RealtimeAPI(access_token=token, mock=False)
client = realtime.create_client()

# 핸들러 등록
def on_quote(message):
    print(f"시세 수신: {message}")

def on_market_status(message):
    print(f"장상태 수신: {message}")

client.register_handler("0B", on_quote)  # 현재가
client.register_handler("90", on_market_status)  # 장상태

# 백그라운드 실행
await client.start()

# 실시간 항목 등록
# 장상태 (90)
await client.register(items=[""], types=["90"], grp_no="0")

# 종목 시세 (0B: 현재가, 0C: 호가, 0F: 체결)
await client.register(
    items=["005930", "000660"],
    types=["0B", "0C"],
    grp_no="1"
)

# 수신 대기
await asyncio.sleep(30)

# 정리
await client.stop()
```

#### 주문/체결 실시간 수신 (0A)

```python
from pykiwoomrest import RealtimeAPI, OrderExecutionData, OrderField

realtime = RealtimeAPI(access_token=token, mock=False)
client = realtime.create_client()

# 주문/체결 핸들러
def on_order_execution(message):
    """주문 체결 핸들러"""
    for data in message.get('data', []):
        # values 리스트를 딕셔너리로 변환
        values = {OrderField(field).value: value 
                 for field, value in zip(OrderField, data.get('values', []))}
        
        # 데이터클래스로 변환
        order_data = OrderExecutionData.from_values(values)
        
        print(f"주문 체결: {order_data.stock_name}({order_data.stock_code})")
        print(f"  상태: {order_data.order_status}")
        print(f"  주문번호: {order_data.order_no}")
        print(f"  체결가: {order_data.execution_price:,}")
        print(f"  체결량: {order_data.execution_qty:,}")
        
        if order_data.order_status == "체결":
            print(f"  체결완료: {order_data.execution_qty}/{order_data.order_qty}")
        elif order_data.order_status == "취소":
            print(f"  주문취소됨")

client.register_handler("0A", on_order_execution)

# 주문 체결 구독 (items는 빈 문자열)
await client.start()
await client.register(items=[""], types=["0A"], grp_no="0")

await asyncio.sleep(60)  # 1분 동안 수신
await client.stop()
```

#### 시세 실시간 수신 (0B)

```python
from pykiwoomrest import RealtimeAPI, QuoteData, QuoteField

realtime = RealtimeAPI(access_token=token, mock=False)
client = realtime.create_client()

# 시세 핸들러
def on_quote(message):
    """시세 핸들러"""
    for data in message.get('data', []):
        # values 리스트를 딕셔너리로 변환
        values = {QuoteField(field).value: value 
                 for field, value in zip(QuoteField, data.get('values', []))}
        
        # 데이터클래스로 변환
        quote = QuoteData.from_values(values)
        
        print(f"시세: {quote.raw.get(QuoteField.STOCK_NAME.value, '')}({data.get('item')})")
        print(f"  현재가: {quote.current_price:,}")
        print(f"  전일대비: {quote.change:+,} ({quote.change_rate:+.2f}%)")
        print(f"  거래량: {quote.cumulative_volume:,}")
        print(f"  거래대금: {quote.cumulative_amount:,.0f}")
        print(f"  매수비율: {quote.buy_ratio:.1f}%")

client.register_handler("0B", on_quote)

# 시세 구독
await client.start()
await client.register(items=["005930"], types=["0B"], grp_no="1")

await asyncio.sleep(30)
await client.stop()
```

#### 실시간 데이터 타입

| 타입 코드 | 설명 | 데이터클래스 |
|-----------|------|-------------|
| `0A` | 주문/체결 | OrderExecutionData |
| `0B` | 현재가 | QuoteData |
| `0C` | 호가 | - |
| `0F` | 체결 | - |
| `01` | 주식체결 | - |
| `02` | 주식호가 | - |
| `03` | 주식매매 | - |
| `90` | 장상태 | - |

#### 주문/체결 필드 (OrderField)

| 필드 코드 | 한글명 | 설명 |
|-----------|--------|------|
| `9201` | 계좌번호 | - |
| `9203` | 주문번호 | 주문 번호 |
| `9001` | 종목코드, 업종코드 | - |
| `913` | 주문상태 | 접수, 체결, 확인, 취소, 거부 |
| `302` | 종목명 | - |
| `900` | 주문수량 | - |
| `901` | 주문가격 | - |
| `902` | 미체결수량 | - |
| `910` | 체결가 | - |
| `911` | 체결량 | - |
| `907` | 매도수구분 | 1:매도, 2:매수 |

#### 시세 필드 (QuoteField)

| 필드 코드 | 한글명 | 설명 |
|-----------|--------|------|
| `10` | 현재가 | - |
| `11` | 전일대비 | - |
| `12` | 등락륨 | - |
| `13` | 누적거래량 | - |
| `14` | 누적거래대금 | - |
| `16` | 시가 | - |
| `17` | 고가 | - |
| `18` | 저가 | - |
| `1030` | 매도체결량 | - |
| `1031` | 매수체결량 | - |
| `1032` | 매수비율 | - |

#### WebSocketClient 메서드

| 메서드 | 설명 |
|--------|------|
| `connect()` | WebSocket 서버 연결 |
| `disconnect()` | 연결 종료 |
| `start()` | 백그라운드에서 실행 |
| `stop()` | 실행 중지 |
| `register(items, types, grp_no, refresh)` | 실시간 항목 등록 |
| `deregister(grp_no)` | 실시간 항목 해지 |
| `register_handler(message_type, handler)` | 메시지 핸들러 등록 |
| `unregister_handler(message_type, handler)` | 핸들러 해제 |

## 주의사항

- 매수/매도 주문은 항상 로그가 남습니다
- 모의투자에서 충분히 테스트 후 실전 사용하세요
- API 키는 절대 코드에 하드코딩하지 마세요
