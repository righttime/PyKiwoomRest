"""RankAPI & ForeignAPI 테스트"""

from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, MagicMock

from pykiwoomrest.rank import RankAPI
from pykiwoomrest.foreign import ForeignAPI


@pytest.fixture
def rank(client) -> RankAPI:
    return RankAPI(client)


@pytest.fixture
def foreign(client) -> ForeignAPI:
    return ForeignAPI(client)


@pytest.mark.asyncio
async def test_volume_rank(rank, client):
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {"ranking": [{"stk_cd": "005930", "volume": "5000000"}]}
    client._http.get = AsyncMock(return_value=mock_resp)

    result = await rank.volume_rank()
    assert result["ranking"][0]["stk_cd"] == "005930"


@pytest.mark.asyncio
async def test_change_rate_rank(rank, client):
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {"ranking": []}
    client._http.get = AsyncMock(return_value=mock_resp)

    result = await rank.change_rate_rank()
    assert "ranking" in result


@pytest.mark.asyncio
async def test_foreign_trade_by_stock(foreign, client):
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {"data": [{"dt": "20260409", "buy": "1000"}]}
    client._http.get = AsyncMock(return_value=mock_resp)

    result = await foreign.foreign_trade_by_stock("005930")
    assert len(result["data"]) == 1


@pytest.mark.asyncio
async def test_foreign_institution_rank(foreign, client):
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = {"ranking": []}
    client._http.get = AsyncMock(return_value=mock_resp)

    result = await foreign.foreign_institution_rank()
    assert "ranking" in result
