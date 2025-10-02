from ya_business_api.reviews.constants import Ranking

from typing import Optional, Literal, overload

from pydantic.main import BaseModel


class AnswerRequest(BaseModel):
	review_id: str
	text: str
	reviews_csrf_token: str
	answer_csrf_token: Optional[str] = None


class ReviewsRequest(BaseModel):
	permanent_id: int
	ranking_by: Ranking = Ranking.BY_TIME

	# Pagination type 1
	unread: Optional[Literal[True]] = None
	continue_token: Optional[str] = None

	# Pagination type 2
	page: Optional[int] = None
	# aspectId: ???

	@overload
	def __init__(
		self,
		*,
		permanent_id: int,
		unread: Literal[True],
		continue_token: Optional[str] = None,
		ranking_by: Ranking = Ranking.BY_TIME,
	): ...

	@overload
	def __init__(self, *, permanent_id: int, page: Optional[int] = None, ranking_by: Ranking = Ranking.BY_TIME): ...

	def __init__(
		self,
		*,
		permanent_id: int,
		ranking_by: Ranking = Ranking.BY_TIME,
		continue_token: Optional[str] = None,
		unread: Optional[Literal[True]] = None,
		page: Optional[int] = None,
	):
		super().__init__(
			permanent_id=permanent_id,
			ranking_by=ranking_by,
			continue_token=continue_token,
			unread=unread,
			page=page,
		)

	def as_query_params(self) -> dict:
		params: dict = {"ranking_by": self.ranking_by.value}

		if self.unread is not None:
			params["unread"] = "true"

			if self.continue_token:
				params["continue_token"] = self.continue_token

		elif self.page is not None:
			params["page"] = self.page

		return params
