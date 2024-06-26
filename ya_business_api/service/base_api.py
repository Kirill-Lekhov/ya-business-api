from ya_business_api.core.base_api import BaseAPI
from ya_business_api.service.router import ServiceRouter

from typing import Final


class BaseServiceAPI(BaseAPI):
	CSRF_TOKEN_FIELD: Final[str] = "csrf"

	router: ServiceRouter

	def make_router(self) -> ServiceRouter:
		return ServiceRouter()
