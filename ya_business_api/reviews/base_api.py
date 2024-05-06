from ya_business_api.core.base_api import BaseAPI
from ya_business_api.reviews.router import ReviewsRouter


class BaseReviewsAPI(BaseAPI):
	permanent_id: int
	csrf_token: str
	router: ReviewsRouter

	def __init__(self, permanent_id: int, csrf_token: str) -> None:
		self.permanent_id = permanent_id
		self.csrf_token = csrf_token

		super().__init__()

	def make_router(self) -> ReviewsRouter:
		return ReviewsRouter(self.permanent_id)
