from ya_business_api.core.mixins.synchronous import SyncAPIMixin
from ya_business_api.service.base_api import BaseServiceAPI

from typing import Optional


class SyncServiceAPI(SyncAPIMixin, BaseServiceAPI):
	def get_csrf_token(self) -> Optional[str]:
		url = self.router.csrf_token()
		self.set_i_cookie()		# Server requires this cookie, but does not check its value.
		response = self.session.post(url, allow_redirects=False)

		if response.status_code == 488:
			return response.json().get(self.CSRF_TOKEN_FIELD)

		return None
