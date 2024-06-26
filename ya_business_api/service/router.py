from ya_business_api.core.router import Router
from ya_business_api.core.constants import BASE_URL


class ServiceRouter(Router):
	def csrf_token(self) -> str:
		return f"{BASE_URL}/api/view/chain/0/list/"
