from typing import Final
from enum import Enum


BASE_URL: Final[str] = "https://yandex.ru/sprav"


class Cookie(Enum):
	SESSION_ID = "Session_id"
	SESSION_ID2 = "sessionid2"
	I = 'i'		# noqa: E741 - Yandex uses this name of cookie
