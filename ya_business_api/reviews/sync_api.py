from ya_business_api.core.mixins.synchronous import SyncAPIMixin
from ya_business_api.core.constants import Cookie
from ya_business_api.reviews.base_api import BaseReviewsAPI
from ya_business_api.reviews.constants import SUCCESS_ANSWER_RESPONSE
from ya_business_api.reviews.dataclasses.reviews import ReviewsResponse
from ya_business_api.reviews.dataclasses.requests import AnswerRequest, ReviewsRequest

from logging import getLogger; log = getLogger(__name__)

from requests.sessions import Session


class SyncReviewsAPI(SyncAPIMixin, BaseReviewsAPI):
	def __init__(self, csrf_token: str, session: Session) -> None:
		super().__init__(session, csrf_token)

	def get_reviews(self, request: ReviewsRequest) -> ReviewsResponse:
		url = self.router.reviews(request.permanent_id)
		response = self.session.get(url, params=request.as_query_params(), allow_redirects=False)
		log.debug(f"REVIEWS[{response.status_code}] {response.elapsed.total_seconds()}s")
		self.check_response(response)

		return ReviewsResponse.from_dict(response.json())

	def send_answer(self, request: AnswerRequest) -> bool:
		"""
		Sends an answer to review.

		Args:
			request: Request data to send.

		Returns:
			True - if answer has been sent successfully, otherwise - False.
		"""
		url = self.router.answer()

		# Server requires this cookie, but does not check its value.
		if not self.session.cookies.get(Cookie.I.value):
			self.session.cookies.set(Cookie.I.value, "")

		response = self.session.post(
			url,
			json={
				"reviewId": request.review_id,
				"text": request.text,
				"answerCsrfToken": request.answer_csrf_token,
				"reviewsCsrfToken": request.reviews_csrf_token,
			},
			headers={
				"X-CSRF-Token": self.csrf_token,
			},
			allow_redirects=False,
		)
		log.debug(f"ANSWER[{response.status_code}] {response.elapsed.total_seconds()}s")
		self.check_response(response)

		return response.text == SUCCESS_ANSWER_RESPONSE
