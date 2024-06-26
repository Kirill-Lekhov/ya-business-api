from ya_business_api.reviews.sync_api import SyncReviewsAPI
from ya_business_api.reviews.dataclasses.reviews import ReviewsResponse
from ya_business_api.reviews.dataclasses.requests import AnswerRequest, ReviewsRequest
from ya_business_api.reviews.constants import Ranking

from logging import DEBUG
from unittest.mock import patch
from json import dumps

from requests.models import Response
from requests.sessions import Session


class TestReviewsAPI:
	def test___init__(self):
		session = Session()
		api = SyncReviewsAPI("csrftoken", session)

		assert api.csrf_token == "csrftoken"
		assert api.session is session

	def test_get_reviews(self, caplog):
		caplog.set_level(DEBUG)
		api = SyncReviewsAPI("csrftoken", Session())
		response = Response()
		response.status_code = 200
		data = {
			"page": 1,
			"currentState": {
				"filters": {
					"ranking": Ranking.BY_TIME.value,
				},
			},
			"list": {
				"pager": {
					"limit": 20,
					"offset": 0,
					"total": 0,
				},
				"items": [],
				"csrf_token": "CSRF_TOKEN",
			},
		}
		response._content = dumps(data).encode("utf-8")
		response.encoding = "utf-8"

		with patch.object(api.session, "get", return_value=response) as session_get_method:
			response = api.get_reviews(ReviewsRequest(permanent_id=1))
			session_get_method.assert_called_once()
			assert isinstance(response, ReviewsResponse)

			response = api.get_reviews(ReviewsRequest(permanent_id=1), raw=True)
			assert isinstance(response, dict)
			assert response == data

	def test_send_answer(self, caplog):
		caplog.set_level(DEBUG)
		api = SyncReviewsAPI("CSRF_TOKEN", Session())
		request = AnswerRequest(
			review_id="review",
			text="hello",
			reviews_csrf_token="reviews_token",
			answer_csrf_token="answer_token",
		)
		response = Response()
		response.status_code = 200

		with patch.object(api.session, "post", return_value=response) as session_post_method:
			response._content = b"OK"
			assert api.send_answer(request)

			response._content = b"FAILED"
			assert not api.send_answer(request)
			session_post_method.assert_called()

		for record in caplog.records:
			assert record.levelname == "DEBUG"

		assert "ANSWER[200] 0.0s" in caplog.text
