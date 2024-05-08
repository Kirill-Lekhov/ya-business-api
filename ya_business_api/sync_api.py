from ya_business_api.reviews.sync_api import SyncReviewsAPI
from ya_business_api.companies.sync_api import SyncCompaniesAPI
from ya_business_api.core.constants import Cookie

from requests.sessions import Session


class SyncAPI:
	reviews: SyncReviewsAPI
	session: Session
	csrf_token: str

	def __init__(self, csrf_token: str, session: Session) -> None:
		self.csrf_token = csrf_token
		self.session = session
		self.reviews = SyncReviewsAPI(csrf_token, session)
		self.companies = SyncCompaniesAPI(session)

	@classmethod
	def build(cls, csrf_token: str, session_id: str, session_id2: str) -> "SyncAPI":
		session = cls.make_session(session_id, session_id2)
		return cls(csrf_token, session)

	@staticmethod
	def make_session(session_id, session_id2) -> Session:
		session = Session()
		session.cookies.set(Cookie.SESSION_ID.value, session_id)
		session.cookies.set(Cookie.SESSION_ID2.value, session_id2)

		return session
