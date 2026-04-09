"""공통 테스트 fixture"""

from __future__ import annotations

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from pykiwoomrest.config import KiwoomConfig
from pykiwoomrest.client import KiwoomClient


@pytest.fixture
def mock_config() -> KiwoomConfig:
    return KiwoomConfig(
        api_key="test_api_key",
        secret_key="test_secret_key",
        account_no="12345678",
        mock=True,
    )


@pytest_asyncio.fixture
async def client(mock_config: KiwoomConfig) -> KiwoomClient:
    """토큰 발급이 mock된 클라이언트"""
    c = KiwoomClient(mock_config)
    c._http = AsyncMock()
    # _issue_token mock
    with patch.object(c, "_issue_token", new_callable=AsyncMock) as mock_token:
        mock_token.return_value = "test_token_abc"
        await c._issue_token()
    c._token = "test_token_abc"
    c._token_expires = 9999999999.0  # far future
    yield c
    c._http = None  # close 안 함 (mock이라)
