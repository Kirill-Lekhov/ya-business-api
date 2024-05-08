from ya_business_api.reviews.base_api import BaseReviewsAPI
from ya_business_api.reviews.router import ReviewsRouter


class TestBaseReviewsAPI:
	def test___init__(self):
		api = BaseReviewsAPI("CSRFTOKEN")
		assert api.csrf_token == "CSRFTOKEN"

	def test_make_router(self):
		api = BaseReviewsAPI("CSRFTOKEN")
		router = api.make_router()
		assert isinstance(router, ReviewsRouter)
