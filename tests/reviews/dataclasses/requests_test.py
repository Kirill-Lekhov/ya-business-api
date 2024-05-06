from ya_business_api.reviews.dataclasses.requests import ReviewsRequest
from ya_business_api.reviews.constants import Ranking


class TestReviewsRequest:
	def test___init__(self):
		request = ReviewsRequest()
		assert request.ranking is Ranking.BY_TIME
		assert not request.unread
		assert request.page == 1

		request = ReviewsRequest(ranking=Ranking.BY_RATING_ASC, unread=True, page=10)
		assert request.ranking is Ranking.BY_RATING_ASC
		assert request.unread
		assert request.page == 10

	def test_as_query_params(self):
		request = ReviewsRequest(ranking=Ranking.BY_RATING_DESC, page=10)
		assert request.as_query_params() == {"ranking": Ranking.BY_RATING_DESC.value, "page": 10}

		request = ReviewsRequest(ranking=Ranking.BY_RATING_DESC, unread=True, page=10)
		assert request.as_query_params() == {"ranking": Ranking.BY_RATING_DESC.value, "unread": True, "page": 10}
