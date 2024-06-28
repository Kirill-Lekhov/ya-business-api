from ya_business_api.core.router import Router
from ya_business_api.core.constants import BASE_URL


class CompaniesRouter(Router):
	def companies(self) -> str:
		return f"{BASE_URL}/api/companies"

	def chain_list(self, tycoon_id: int) -> str:
		return f"{BASE_URL}/api/view/chain/{tycoon_id}/list/"
