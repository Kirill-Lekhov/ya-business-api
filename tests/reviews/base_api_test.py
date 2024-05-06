from ya_business_api.reviews.base_api import BaseReviewsAPI
from ya_business_api.reviews.router import ReviewsRouter


class TestBaseReviewsAPI:
	def test___init__(self):
		api = BaseReviewsAPI(1212, "CSRFTOKEN")
		assert api.permanent_id == 1212
		assert api.csrf_token == "CSRFTOKEN"

	def test_make_router(self):
		api = BaseReviewsAPI(1212, "CSRFTOKEN")
		router = api.make_router()
		assert isinstance(router, ReviewsRouter)
