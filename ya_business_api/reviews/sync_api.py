from ya_business_api.core.mixins.synchronous import SyncAPIMixin
from ya_business_api.core.constants import CSRF_TOKEN_HEADER
from ya_business_api.reviews.base_api import BaseReviewsAPI
from ya_business_api.reviews.constants import SUCCESS_ANSWER_RESPONSE
from ya_business_api.reviews.dataclasses.reviews import ReviewsResponse
from ya_business_api.reviews.dataclasses.requests import AnswerRequest, ReviewsRequest

from typing import Union, Literal, overload
from logging import getLogger; log = getLogger(__name__)

from requests.sessions import Session


class SyncReviewsAPI(SyncAPIMixin, BaseReviewsAPI):
	def __init__(self, csrf_token: str, session: Session) -> None:
		super().__init__(session, csrf_token)

	@overload
	def get_reviews(self, request: ReviewsRequest, *, raw: Literal[True]) -> dict: ...

	@overload
	def get_reviews(self, request: ReviewsRequest, *, raw: Literal[False] = False) -> ReviewsResponse: ...

	def get_reviews(self, request: ReviewsRequest, *, raw: bool = False) -> Union[ReviewsResponse, dict]:
		url = self.router.reviews(request.permanent_id)
		response = self.session.get(url, params=request.as_query_params(), allow_redirects=False)
		log.debug(f"REVIEWS[{response.status_code}] {response.elapsed.total_seconds()}s")
		self.check_response(response)

		if raw:
			return response.json()

		return ReviewsResponse.model_validate_json(response.text)

	def send_answer(self, request: AnswerRequest) -> bool:
		"""
		Sends an answer to review.

		Args:
			request: Request data to send.

		Returns:
			True - if answer has been sent successfully, otherwise - False.
		"""
		url = self.router.answer()
		self.set_i_cookie()		# Server requires this cookie, but does not check its value.
		response = self.session.post(
			url,
			json={
				"reviewId": request.review_id,
				"text": request.text,
				"answerCsrfToken": request.answer_csrf_token,
				"reviewsCsrfToken": request.reviews_csrf_token,
			},
			headers={
				CSRF_TOKEN_HEADER: self.csrf_token,
			},
			allow_redirects=False,
		)
		log.debug(f"ANSWER[{response.status_code}] {response.elapsed.total_seconds()}s")
		self.check_response(response)

		return response.text == SUCCESS_ANSWER_RESPONSE
