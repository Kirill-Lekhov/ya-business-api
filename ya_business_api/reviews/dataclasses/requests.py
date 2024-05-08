from ya_business_api.core.dataclasses import ValidatedMixin
from ya_business_api.reviews.constants import Ranking

from dataclasses import dataclass


@dataclass
class AnswerRequest(ValidatedMixin):
	review_id: str
	text: str
	reviews_csrf_token: str
	answer_csrf_token: str


@dataclass
class ReviewsRequest(ValidatedMixin):
	permanent_id: int
	ranking: Ranking = Ranking.BY_TIME
	unread: bool = False
	page: int = 1
	# aspectId: ???

	def as_query_params(self) -> dict:
		params = {"ranking": self.ranking.value, "page": self.page}

		if self.unread:
			params["unread"] = self.unread

		return params
