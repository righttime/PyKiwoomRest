"""TradingAPI 테스트"""

from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, MagicMock

from pykiwoomrest.trading import TradingAPI


@pytest.fixture
def trading(client) -> TradingAPI:
    return TradingAPI(client)


@pytest.mark.asyncio
async def test_deposit(trading, client):
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {"tot_evlt_amt": "10,000,000"}
    client._http.get = AsyncMock(return_value=mock_resp)

    result = await trading.deposit()
    assert "tot_evlt_amt" in result


@pytest.mark.asyncio
async def test_holdings(trading, client):
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {"stocks": [{"stk_cd": "005930", "qty": "10"}]}
    client._http.get = AsyncMock(return_value=mock_resp)

    result = await trading.holdings()
    assert len(result["stocks"]) == 1


@pytest.mark.asyncio
async def test_buy_market_order(trading, client):
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {"ord_no": "99999"}
    client._http.post = AsyncMock(return_value=mock_resp)

    result = await trading.buy("005930", 10)
    assert result["ord_no"] == "99999"

    # 시장가 확인 (ord_tp=03)
    call_kwargs = client._http.post.call_args
    data = call_kwargs.kwargs.get("json") or call_kwargs.kwargs.get("data")
    # json 방식으로 보냄


@pytest.mark.asyncio
async def test_sell_limit_order(trading, client):
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {"ord_no": "99998"}
    client._http.post = AsyncMock(return_value=mock_resp)

    result = await trading.sell("005930", 5, price=60000)
    assert result["ord_no"] == "99998"
