from ya_business_api.core.mixins.asynchronous import AsyncAPIMixin
from ya_business_api.service.base_api import BaseServiceAPI

from typing import Optional
from time import monotonic
from logging import getLogger; log = getLogger(__name__)


class AsyncServiceAPI(AsyncAPIMixin, BaseServiceAPI):
	async def get_csrf_token(self) -> Optional[str]:
		url = self.router.csrf_token()
		time_start = monotonic()

		async with self.session.post(url, allow_redirects=False) as response:
			log.debug(f"A:CSRF_TOKEN[{response.status}] {monotonic() - time_start:.1f}s")

			if response.status == 488:
				return (await response.json()).get(self.CSRF_TOKEN_FIELD)

		return None
