from ya_business_api.reviews.dataclasses.requests import ReviewsRequest
from ya_business_api.reviews.constants import Ranking


class TestReviewsRequest:
	def test_as_query_params(self):
		request = ReviewsRequest(permanent_id=1)
		assert request.as_query_params() == {"ranking_by": Ranking.BY_TIME.value}

		request = ReviewsRequest(permanent_id=1, ranking_by=Ranking.BY_RATING_ASC)
		assert request.as_query_params() == {"ranking_by": Ranking.BY_RATING_ASC.value}

		request = ReviewsRequest(permanent_id=1, unread=True)
		assert request.as_query_params() == {"ranking_by": Ranking.BY_TIME.value, "unread": "true"}

		request = ReviewsRequest(
			permanent_id=1,
			unread=True,
			continue_token="CONTINUE_TOKEN",
			ranking_by=Ranking.BY_RATING_ASC,
		)
		assert request.as_query_params() == {
			"ranking_by": Ranking.BY_RATING_ASC.value,
			"unread": "true",
			"continue_token": "CONTINUE_TOKEN",
		}

		request = ReviewsRequest(
			permanent_id=1,
			page=10,
			ranking_by=Ranking.BY_RATING_ASC,
		)
		assert request.as_query_params() == {
			"ranking_by": Ranking.BY_RATING_ASC.value,
			"page": 10,
		}

		request = ReviewsRequest(		# type: ignore - for testing purposes
			permanent_id=1,
			unread=True,
			page=10,
			ranking_by=Ranking.BY_RATING_ASC,
			continue_token="CONTINUE_TOKEN",
		)
		assert request.as_query_params() == {
			"ranking_by": Ranking.BY_RATING_ASC.value,
			"unread": "true",
			"continue_token": "CONTINUE_TOKEN",
		}
