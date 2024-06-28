from ya_business_api.reviews.sync_api import SyncReviewsAPI
from ya_business_api.companies.sync_api import SyncCompaniesAPI
from ya_business_api.service.sync_api import SyncServiceAPI
from ya_business_api.core.constants import Cookie
from ya_business_api.core.exceptions import CSRFTokenError

from typing import Optional
from logging import getLogger; log = getLogger(__name__)

from requests.sessions import Session


class SyncAPI:
	reviews: SyncReviewsAPI
	session: Session
	csrf_token: str

	def __init__(self, csrf_token: str, session: Session) -> None:
		self.csrf_token = csrf_token
		self.session = session
		self.reviews = SyncReviewsAPI(csrf_token, session)
		self.companies = SyncCompaniesAPI(csrf_token, session)
		self.service = SyncServiceAPI(session)

	@classmethod
	def build(cls, session_id: str, session_id2: str, csrf_token: Optional[str] = None) -> "SyncAPI":
		session = cls.make_session(session_id, session_id2)

		if csrf_token is None:
			log.info("CSRF token was not specified. Attempting to receive a token automatically...")
			service_api = SyncServiceAPI(session)
			csrf_token = service_api.get_csrf_token()

			if csrf_token is None:
				raise CSRFTokenError("Failed to get CSRF token. It is not possible to create a client instance")

		return cls(csrf_token, session)

	@staticmethod
	def make_session(session_id, session_id2) -> Session:
		session = Session()
		session.cookies.set(Cookie.SESSION_ID.value, session_id)
		session.cookies.set(Cookie.SESSION_ID2.value, session_id2)

		return session
