from ya_business_api.core.constants import INVALID_TOKEN_STATUSES, PASSPORT_URL
from ya_business_api.core.exceptions import CSRFTokenError, AuthenticationError

from aiohttp.client import ClientSession, ClientResponse


class AsyncAPIMixin:
	session: ClientSession

	def __init__(self, session: ClientSession, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)

		self.session = session

	@staticmethod
	def check_response(response: ClientResponse) -> None:
		if response.status == 302 and response.headers.get('Location', '').startswith(PASSPORT_URL):
			raise AuthenticationError()

		if response.status in INVALID_TOKEN_STATUSES:
			raise CSRFTokenError()

		assert response.status == 200
