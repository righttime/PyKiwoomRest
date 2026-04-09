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
└── foreign.py       # 외국인/기관
```

## 주의사항

- 매수/매도 주문은 항상 로그가 남습니다
- 모의투자에서 충분히 테스트 후 실전 사용하세요
- API 키는 절대 코드에 하드코딩하지 마세요
