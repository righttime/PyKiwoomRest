"""키움 REST API 예외"""

from __future__ import annotations


class KiwoomAPIError(Exception):
    """키움 API 에러"""

    def __init__(self, return_code: str, return_msg: str, response: dict | None = None):
        self.code = return_code
        self.message = return_msg
        self.response = response or {}
        super().__init__(f"[{return_code}] {return_msg}")
