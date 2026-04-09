"""KiwoomClient 테스트"""

from __future__ import annotations

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from pykiwoomrest.client import KiwoomClient
from pykiwoomrest.config import KiwoomConfig


@pytest.fixture
def config() -> KiwoomConfig:
    return KiwoomConfig(api_key="k", secret_key="s", account_no="1234", mock=True)


class TestKiwoomConfig:
    def test_mock_base_url(self):
        cfg = KiwoomConfig(mock=True)
        assert cfg.base_url == "https://mockapi.kiwoom.com"

    def test_real_base_url(self):
        cfg = KiwoomConfig(mock=False)
        assert cfg.base_url == "https://api.kiwoom.com"

    def test_from_env(self, tmp_path):
        env_file = tmp_path / ".env"
        env_file.write_text("KIWOOM_API_KEY=ak\nKIWOOM_SECRET_KEY=sk\nKIWOOM_ACCOUNT_NO=1111\nKIWOOM_MOCK=false\n")
        cfg = KiwoomConfig.from_env(str(env_file))
        assert cfg.api_key == "ak"
        assert cfg.mock is False
        assert cfg.base_url == "https://api.kiwoom.com"


class TestKiwoomClient:
    @pytest.mark.asyncio
    async def test_issue_token(self, config: KiwoomConfig):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {"token": "abc123"}
        mock_http = AsyncMock()
        mock_http.post.return_value = mock_resp
        mock_http.aclose = AsyncMock()

        with patch("pykiwoomrest.client.httpx.AsyncClient", return_value=mock_http):
            client = KiwoomClient(config)
            client._http = mock_http
            token = await client._issue_token()
            assert token == "abc123"
            assert client._token == "abc123"

    @pytest.mark.asyncio
    async def test_get_request(self, client: KiwoomClient):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {"stk_nm": "삼성전자", "cur_prc": "60,000"}
        client._http.get = AsyncMock(return_value=mock_resp)

        result = await client.get("/api/dostk/stkinfo", tr_id="ka10001", stk_cd="005930")
        assert result["stk_nm"] == "삼성전자"

        # 헤더 확인
        call_kwargs = client._http.get.call_args
        headers = call_kwargs.kwargs["headers"]
        assert headers["api_id"] == "ka10001"
        assert "Bearer test_token_abc" in headers["Authorization"]

    @pytest.mark.asyncio
    async def test_post_request(self, client: KiwoomClient):
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {"ord_no": "12345"}
        client._http.post = AsyncMock(return_value=mock_resp)

        result = await client.post("/api/dostk/acnt", tr_id="kt10000", data={"stk_cd": "005930"})
        assert result["ord_no"] == "12345"

    @pytest.mark.asyncio
    async def test_context_manager(self, config: KiwoomConfig):
        with patch("pykiwoomrest.client.httpx.AsyncClient") as MockHttp:
            mock_http = AsyncMock()
            mock_resp = MagicMock()
            mock_resp.raise_for_status = MagicMock()
            mock_resp.json.return_value = {"token": "ctx_token"}
            mock_http.post.return_value = mock_resp
            MockHttp.return_value = mock_http

            async with KiwoomClient(config) as c:
                assert c._token == "ctx_token"
            mock_http.aclose.assert_called_once()
