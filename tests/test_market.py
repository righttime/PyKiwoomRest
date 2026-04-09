"""MarketAPI 테스트"""

from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, MagicMock

from pykiwoomrest.market import MarketAPI


@pytest.fixture
def market(client) -> MarketAPI:
    return MarketAPI(client)


@pytest.mark.asyncio
async def test_basic_info(market, client):
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {"stk_nm": "삼성전자", "cur_prc": "60,000"}
    client._http.get = AsyncMock(return_value=mock_resp)

    result = await market.basic_info("005930")
    assert result["stk_nm"] == "삼성전자"


@pytest.mark.asyncio
async def test_day_chart(market, client):
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {"chart": [{"dt": "20260409", "close": "60000"}]}
    client._http.get = AsyncMock(return_value=mock_resp)

    result = await market.day_chart("005930")
    assert len(result["chart"]) == 1


@pytest.mark.asyncio
async def test_search_stock(market, client):
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {"results": [{"stk_cd": "005930", "stk_nm": "삼성전자"}]}
    client._http.get = AsyncMock(return_value=mock_resp)

    result = await market.search_stock("삼성전자")
    assert result["results"][0]["stk_cd"] == "005930"


@pytest.mark.asyncio
async def test_quote(market, client):
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {"ask1": "60,100", "bid1": "60,000"}
    client._http.get = AsyncMock(return_value=mock_resp)

    result = await market.quote("005930")
    assert "ask1" in result
