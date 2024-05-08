from ya_business_api.reviews.async_api import AsyncReviewsAPI
from ya_business_api.core.constants import Cookie
from ya_business_api.companies.async_api import AsyncCompaniesAPI

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
		self.companies = AsyncCompaniesAPI(self.session)

	@classmethod
	async def build(cls, csrf_token: str, session_id: str, session_id2: str) -> "AsyncAPI":
		session = await cls.make_session(session_id, session_id2)
		return cls(csrf_token, session)

	@staticmethod
	async def make_session(session_id: str, session_id2: str) -> ClientSession:
		session = ClientSession()
		session.cookie_jar.update_cookies({
			Cookie.SESSION_ID.value: session_id,
			Cookie.SESSION_ID2.value: session_id2,
		})

		return session
