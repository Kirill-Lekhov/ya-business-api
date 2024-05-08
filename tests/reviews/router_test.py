from ya_business_api.reviews.router import ReviewsRouter


class TestReviewsRouter:
	def test_reviews(self):
		router = ReviewsRouter()
		assert router.reviews(1) == "https://yandex.ru/sprav/api/1/reviews"

	def test_answer(self):
		router = ReviewsRouter()
		assert router.answer() == "https://yandex.ru/sprav/api/ugcpub/business-answer"
