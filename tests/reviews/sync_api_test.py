from ya_business_api.reviews.sync_api import SyncReviewsAPI
from ya_business_api.reviews.dataclasses.reviews import ReviewsResponse
from ya_business_api.reviews.dataclasses.requests import AnswerRequest
from ya_business_api.reviews.constants import Ranking
from ya_business_api.core.constants import Cookie

from logging import DEBUG
from unittest.mock import patch

import pytest
from requests.models import Response
from requests.sessions import Session


class TestReviewsAPI:
	def test___init__(self):
		session = Session()
		api = SyncReviewsAPI(1, "csrftoken", session)

		assert api.permanent_id == 1
		assert api.csrf_token == "csrftoken"
		assert api.session is session

	def test_get_reviews(self, caplog):
		caplog.set_level(DEBUG)
		api = SyncReviewsAPI(1, "csrftoken", Session())
		response = Response()
		response.status_code = 400

		with patch.object(api.session, "get", return_value=response) as session_get_method:
			with pytest.raises(AssertionError):
				api.get_reviews()

			session_get_method.assert_called_once()

			for record in caplog.records:
				assert record.levelname == "DEBUG"

			assert "REVIEWS[400] 0.0s" in caplog.text

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

		with patch.object(response, "json", return_value=data) as response_json_method:
			with patch.object(api.session, "get", return_value=response) as session_get_method:
				response = api.get_reviews()
				session_get_method.assert_called_once()
				response_json_method.assert_called_once()

				assert isinstance(response, ReviewsResponse)

	def test_send_answer(self, caplog):
		caplog.set_level(DEBUG)
		api = SyncReviewsAPI(1, "CSRF_TOKEN", Session())
		request = AnswerRequest("review", "hello", "reviews_token", "answer_token")
		response = Response()

		for i in (488, 401):
			response.status_code = i

			with patch.object(api.session, "post", return_value=response) as session_post_method:
				with patch.object(api.session.cookies, "set") as session_cookies_set_method:
					with pytest.raises(ValueError, match="Invalid token"):
						api.send_answer(request)

					session_cookies_set_method.assert_called_once_with(Cookie.I.value, "")
					session_post_method.assert_called_once()

		response.status_code = 200

		with patch.object(api.session, "post", return_value=response) as session_post_method:
			response._content = b"OK"
			assert api.send_answer(request)

			response._content = b"FAILED"
			assert not api.send_answer(request)

		for record in caplog.records:
			assert record.levelname == "DEBUG"

		assert "ANSWER[200] 0.0s" in caplog.text
