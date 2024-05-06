from ya_business_api.core.mixins.asynchronous import AsyncAPIMixin
from ya_business_api.core.constants import Cookie
from ya_business_api.reviews.base_api import BaseReviewsAPI
from ya_business_api.reviews.constants import INVALID_TOKEN_STATUSES, SUCCESS_ANSWER_RESPONSE
from ya_business_api.reviews.dataclasses.reviews import ReviewsResponse
from ya_business_api.reviews.dataclasses.requests import AnswerRequest, ReviewsRequest

from time import monotonic
from logging import getLogger; log = getLogger(__name__)
from typing import Optional

from aiohttp.client import ClientSession


class AsyncReviewsAPI(AsyncAPIMixin, BaseReviewsAPI):
	def __init__(self, permanent_id: int, csrf_token: str, session: ClientSession) -> None:
		super().__init__(session, permanent_id, csrf_token)

	async def get_reviews(self, request: Optional[ReviewsRequest] = None) -> ReviewsResponse:
		url = self.router.reviews()
		request = request or ReviewsRequest()
		time_start = monotonic()

		async with self.session.get(url, params=request.as_query_params(), allow_redirects=False) as response:
			log.debug(f"A:REVIEWS[{response.status}] {monotonic() - time_start:.1f}s")
			assert response.status == 200
			response = ReviewsResponse.from_dict(await response.json())

		return response

	async def send_answer(self, request: AnswerRequest) -> bool:
		url = self.router.answer()
		cookie_names = {cookie.key for cookie in self.session.cookie_jar}

		if Cookie.I.value not in cookie_names:
			self.session.cookie_jar.update_cookies({Cookie.I.value: ""})

		data = {
			"reviewId": request.review_id,
			"text": request.text,
			"answerCsrfToken": request.answer_csrf_token,
			"reviewsCsrfToken": request.reviews_csrf_token,
		}
		headers = {"X-CSRF-Token": self.csrf_token}
		time_start = monotonic()

		async with self.session.post(url, json=data, headers=headers, allow_redirects=False) as response:
			log.debug(f"A:ANSWER[{response.status}] {monotonic() - time_start:.1f}s")

			if response.status in INVALID_TOKEN_STATUSES:
				raise ValueError("Invalid token")

			assert response.status == 200
			result = await response.text() == SUCCESS_ANSWER_RESPONSE

		return result