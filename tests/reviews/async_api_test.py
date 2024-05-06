from ya_business_api.reviews.async_api import AsyncReviewsAPI
from ya_business_api.reviews.constants import Ranking
from ya_business_api.reviews.dataclasses.reviews import ReviewsResponse
from ya_business_api.reviews.dataclasses.requests import AnswerRequest

from json import loads, dumps
from unittest.mock import patch
from typing import Any
from logging import DEBUG

import pytest
from aiohttp.client import ClientSession


class Response:
	status: int

	def __init__(self, status: int, content: str) -> None:
		self.status = status
		self.content = content

	async def json(self) -> Any:
		return loads(self.content)

	async def text(self) -> str:
		return self.content


class RequestContextManager:
	def __init__(self, response: Response) -> None:
		self.response = response

	async def __aenter__(self, *args, **kwargs):
		return self.response

	async def __aexit__(self, *args, **kwargs):
		pass


@pytest.mark.asyncio
class TestAsyncReviewsAPI:
	async def test___init__(self):
		session = ClientSession()
		api = AsyncReviewsAPI(1212, "CSRFTOKEN", session)

		assert api.permanent_id == 1212
		assert api.csrf_token == "CSRFTOKEN"
		assert api.session is session

	async def test_get_reviews(self, caplog):
		caplog.set_level(DEBUG)
		session = ClientSession()
		api = AsyncReviewsAPI(1212, "CSRFTOKEN", session)
		response = Response(400, "")
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
		request_context_manager = RequestContextManager(response)

		with patch.object(session, "get", return_value=request_context_manager) as session_get_method:
			with patch("ya_business_api.reviews.async_api.monotonic", return_value=0.0):
				with pytest.raises(AssertionError):
					await api.get_reviews()

				for record in caplog.records:
					assert record.levelname == "DEBUG"

				assert "REVIEWS[400] 0.0s\n" in caplog.text
				session_get_method.assert_called_once()

				session_get_method.reset_mock()
				response.status = 200
				response.content = dumps(data)

				data = await api.get_reviews()
				session_get_method.assert_called_once()
				assert isinstance(data, ReviewsResponse)

		await api.session.close()

	async def test_send_answer(self, caplog):
		caplog.set_level(DEBUG)
		session = ClientSession()
		api = AsyncReviewsAPI(1, "CSRFTOKEN", session)
		request = AnswerRequest("review", "hello", "reviews_token", "answer_token")
		response = Response(200, "")
		request_context_manager = RequestContextManager(response)

		with patch.object(session, "post", return_value=request_context_manager) as session_post_method:
			with patch("ya_business_api.reviews.async_api.monotonic", return_value=0.0):
				for i in (488, 401):
					response.status = i

					with patch.object(session.cookie_jar, "update_cookies") as update_cookies_method:
						with pytest.raises(ValueError, match="Invalid token"):
							await api.send_answer(request)

						update_cookies_method.assert_called()

				response.status = 200
				response.content = "OK"
				session_post_method.reset_mock()
				assert await api.send_answer(request)
				session_post_method.assert_called_once()

				response.content = "FAILED"
				assert not await api.send_answer(request)

				for record in caplog.records:
					assert record.levelname == "DEBUG"

				assert "A:ANSWER[200] 0.0s" in caplog.text

		await session.close()
