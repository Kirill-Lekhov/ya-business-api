from ya_business_api.reviews.async_api import AsyncReviewsAPI
from ya_business_api.reviews.constants import Ranking
from ya_business_api.reviews.dataclasses.reviews import ReviewsResponse
from ya_business_api.reviews.dataclasses.requests import AnswerRequest, ReviewsRequest
from tests.aiohttp import Response, RequestContextManager

from json import dumps
from unittest.mock import patch
from logging import DEBUG

import pytest
from aiohttp.client import ClientSession


@pytest.mark.asyncio
class TestAsyncReviewsAPI:
	async def test___init__(self):
		session = ClientSession()
		api = AsyncReviewsAPI("CSRFTOKEN", session)

		assert api.csrf_token == "CSRFTOKEN"
		assert api.session is session

	async def test_get_reviews(self, caplog):
		caplog.set_level(DEBUG)
		session = ClientSession()
		api = AsyncReviewsAPI("CSRFTOKEN", session)
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
		response = Response(200, dumps(data))
		request_context_manager = RequestContextManager(response)

		with patch.object(session, "get", return_value=request_context_manager) as session_get_method:
			with patch("ya_business_api.reviews.async_api.monotonic", return_value=0.0):
				data = await api.get_reviews(ReviewsRequest(permanent_id=1))
				session_get_method.assert_called_once()
				assert isinstance(data, ReviewsResponse)

				data = await api.get_reviews(ReviewsRequest(permanent_id=1), raw=True)
				assert isinstance(data, dict)
				assert data == data

		await api.session.close()

	async def test_send_answer(self, caplog):
		caplog.set_level(DEBUG)
		session = ClientSession()
		api = AsyncReviewsAPI("CSRFTOKEN", session)
		request = AnswerRequest(
			review_id="review",
			text="hello",
			reviews_csrf_token="reviews_token",
			answer_csrf_token="answer_token",
		)
		response = Response(200, "OK")
		request_context_manager = RequestContextManager(response)

		with patch.object(session, "post", return_value=request_context_manager) as session_post_method:
			with patch("ya_business_api.reviews.async_api.monotonic", return_value=0.0):
				session_post_method.reset_mock()
				assert await api.send_answer(request)
				session_post_method.assert_called_once()

				response.content = "FAILED"
				assert not await api.send_answer(request)

				for record in caplog.records:
					assert record.levelname == "DEBUG"

				assert "A:ANSWER[200] 0.0s" in caplog.text

		await session.close()
