from enum import Enum
from typing import Final


SUCCESS_ANSWER_RESPONSE: Final[str] = "OK"


class Ranking(Enum):
	BY_RATING_DESC = "by_rating_desc"
	BY_RATING_ASC = "by_rating_asc"
	BY_TIME = "by_time"
