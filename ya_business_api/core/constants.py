from typing import Final, Set
from enum import Enum


BASE_URL: Final[str] = "https://yandex.ru/sprav"
PASSPORT_URL: Final[str] = "https://passport.yandex.ru"
INVALID_TOKEN_STATUSES: Final[Set[int]] = {488, 401}


class Cookie(Enum):
	SESSION_ID = "Session_id"
	SESSION_ID2 = "sessionid2"
	I = 'i'		# noqa: E741 - Yandex uses this name of cookie
