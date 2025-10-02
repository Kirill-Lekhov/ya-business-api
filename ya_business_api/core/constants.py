from typing import Final, Set, Dict
from enum import Enum


BASE_URL: Final[str] = "https://yandex.ru/sprav"
PASSPORT_URL: Final[str] = "https://passport.yandex.ru"
INVALID_TOKEN_STATUSES: Final[Set[int]] = {488, 401}
CSRF_TOKEN_HEADER: Final[str] = "X-CSRF-Token"
DEFAULT_HEADERS: Final[Dict[str, str]] = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
}


class Cookie(Enum):
	SESSION_ID = "Session_id"
	SESSION_ID2 = "sessionid2"
	I = 'i'		# noqa: E741 - Yandex uses this name of cookie
