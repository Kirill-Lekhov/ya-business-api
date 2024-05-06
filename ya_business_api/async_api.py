from ya_business_api.reviews.async_api import AsyncReviewsAPI
from ya_business_api.core.constants import Cookie

from aiohttp.client import ClientSession


class AsyncAPI:
	permanent_id: int
	reviews: AsyncReviewsAPI
	session: ClientSession
	csrf_token: str

	def __init__(self, permanent_id: int, csrf_token: str, session: ClientSession) -> None:
		self.permanent_id = permanent_id
		self.csrf_token = csrf_token
		self.session = session
		self.reviews = AsyncReviewsAPI(permanent_id, csrf_token, session)

	@classmethod
	async def build(cls, permanent_id: int, csrf_token: str, session_id: str, session_id2: str) -> "AsyncAPI":
		session = await cls.make_session(session_id, session_id2)
		return cls(permanent_id, csrf_token, session)

	@staticmethod
	async def make_session(session_id: str, session_id2: str) -> ClientSession:
		session = ClientSession()
		session.cookie_jar.update_cookies({
			Cookie.SESSION_ID.value: session_id,
			Cookie.SESSION_ID2.value: session_id2,
		})

		return session
