from ya_business_api.core.mixins.asynchronous import AsyncAPIMixin
from ya_business_api.reviews.base_api import BaseReviewsAPI
from ya_business_api.reviews.constants import SUCCESS_ANSWER_RESPONSE
from ya_business_api.reviews.dataclasses.reviews import ReviewsResponse
from ya_business_api.reviews.dataclasses.requests import AnswerRequest, ReviewsRequest

from typing import Union, Literal, overload
from time import monotonic
from logging import getLogger; log = getLogger(__name__)

from aiohttp.client import ClientSession


class AsyncReviewsAPI(AsyncAPIMixin, BaseReviewsAPI):
	def __init__(self, csrf_token: str, session: ClientSession) -> None:
		super().__init__(session, csrf_token)

	@overload
	async def get_reviews(self, request: ReviewsRequest, *, raw: Literal[True]) -> dict: ...

	@overload
	async def get_reviews(self, request: ReviewsRequest, *, raw: Literal[False] = False) -> ReviewsResponse: ...

	async def get_reviews(self, request: ReviewsRequest, *, raw: bool = False) -> Union[ReviewsResponse, dict]:
		url = self.router.reviews(request.permanent_id)
		time_start = monotonic()

		async with self.session.get(url, params=request.as_query_params(), allow_redirects=False) as response:
			log.debug(f"A:REVIEWS[{response.status}] {monotonic() - time_start:.1f}s")
			self.check_response(response)

			if raw:
				return await response.json()

			return ReviewsResponse.model_validate_json(await response.text())

	async def send_answer(self, request: AnswerRequest) -> bool:
		url = self.router.answer()
		self.set_i_cookie()
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
			self.check_response(response)
			result = await response.text() == SUCCESS_ANSWER_RESPONSE

		return result
