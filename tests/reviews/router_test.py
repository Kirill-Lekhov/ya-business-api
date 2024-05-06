from ya_business_api.reviews.router import ReviewsRouter


class TestReviewsRouter:
	def test___init__(self):
		router = ReviewsRouter(1)

		assert router.permanent_id == 1

	def test_reviews(self):
		router = ReviewsRouter(1)

		assert router.reviews() == "https://yandex.ru/sprav/api/1/reviews"

	def test_answer(self):
		router = ReviewsRouter(1)

		assert router.answer() == "https://yandex.ru/sprav/api/ugcpub/business-answer"
