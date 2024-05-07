from ya_business_api.core.constants import INVALID_TOKEN_STATUSES, PASSPORT_URL
from ya_business_api.core.exceptions import CSRFTokenError, AuthenticationError

from requests.sessions import Session
from requests.models import Response


class SyncAPIMixin:
	session: Session

	def __init__(self, session: Session, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)

		self.session = session

	@staticmethod
	def check_response(response: Response) -> None:
		if response.status_code == 302 and getattr(response.next, 'url', "").startswith(PASSPORT_URL):
			raise AuthenticationError()

		if response.status_code in INVALID_TOKEN_STATUSES:
			raise CSRFTokenError()

		assert response.status_code == 200
