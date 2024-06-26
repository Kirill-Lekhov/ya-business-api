from ya_business_api.reviews.constants import Ranking

from pydantic import BaseModel


class AnswerRequest(BaseModel):
	review_id: str
	text: str
	reviews_csrf_token: str
	answer_csrf_token: str


class ReviewsRequest(BaseModel):
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
