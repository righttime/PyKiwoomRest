"""설정 관리"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv


@dataclass
class KiwoomConfig:
    """키움 API 설정"""

    api_key: str = ""
    secret_key: str = ""
    account_no: str = ""
    mock: bool = True

    # Base URL (자동 설정)
    base_url: str = field(init=False, default="")

    def __post_init__(self) -> None:
        if self.mock:
            self.base_url = "https://mockapi.kiwoom.com"
        else:
            self.base_url = "https://api.kiwoom.com"

    @classmethod
    def from_env(cls, env_path: str | None = None) -> KiwoomConfig:
        """ .env 파일에서 설정 로드"""
        if env_path:
            load_dotenv(env_path)
        else:
            load_dotenv()

        mock = os.getenv("KIWOOM_MOCK", "true").lower() == "true"

        if mock:
            api_key = os.getenv("KIWOOM_MOCK_API_KEY") or os.getenv("KIWOOM_API_KEY", "")
            secret_key = os.getenv("KIWOOM_MOCK_SECRET_KEY") or os.getenv("KIWOOM_SECRET_KEY", "")
        else:
            api_key = os.getenv("KIWOOM_REAL_API_KEY") or os.getenv("KIWOOM_API_KEY", "")
            secret_key = os.getenv("KIWOOM_REAL_SECRET_KEY") or os.getenv("KIWOOM_SECRET_KEY", "")

        return cls(
            api_key=api_key,
            secret_key=secret_key,
            account_no=os.getenv("KIWOOM_ACCOUNT_NO", ""),
            mock=mock,
        )
