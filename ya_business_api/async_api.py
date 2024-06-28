from ya_business_api.reviews.async_api import AsyncReviewsAPI
from ya_business_api.companies.async_api import AsyncCompaniesAPI
from ya_business_api.service.async_api import AsyncServiceAPI
from ya_business_api.core.constants import Cookie
from ya_business_api.core.exceptions import CSRFTokenError

from typing import Optional
from logging import getLogger; log = getLogger(__name__)

from aiohttp.client import ClientSession


class AsyncAPI:
	reviews: AsyncReviewsAPI
	companies: AsyncCompaniesAPI
	session: ClientSession
	csrf_token: str

	def __init__(self, csrf_token: str, session: ClientSession) -> None:
		self.csrf_token = csrf_token
		self.session = session
		self.reviews = AsyncReviewsAPI(csrf_token, session)
		self.companies = AsyncCompaniesAPI(csrf_token, session)
		self.service = AsyncServiceAPI(session)

	@classmethod
	async def build(cls, session_id: str, session_id2: str, csrf_token: Optional[str] = None) -> "AsyncAPI":
		session = await cls.make_session(session_id, session_id2)

		if csrf_token is None:
			log.info("CSRF token was not specified. Attempting to receive a token automatically...")
			service_api = AsyncServiceAPI(session)
			csrf_token = await service_api.get_csrf_token()

			if csrf_token is None:
				raise CSRFTokenError("Failed to get CSRF token. It is not possible to create a client instance")

		return cls(csrf_token, session)

	@staticmethod
	async def make_session(session_id: str, session_id2: str) -> ClientSession:
		session = ClientSession()
		session.cookie_jar.update_cookies({
			Cookie.SESSION_ID.value: session_id,
			Cookie.SESSION_ID2.value: session_id2,
		})

		return session
