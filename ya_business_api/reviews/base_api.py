from ya_business_api.core.base_api import BaseAPI
from ya_business_api.reviews.router import ReviewsRouter


class BaseReviewsAPI(BaseAPI):
	csrf_token: str
	router: ReviewsRouter

	def __init__(self, csrf_token: str) -> None:
		self.csrf_token = csrf_token

		super().__init__()

	def make_router(self) -> ReviewsRouter:
		return ReviewsRouter()
