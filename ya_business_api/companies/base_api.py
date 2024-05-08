from ya_business_api.core.base_api import BaseAPI
from ya_business_api.companies.router import CompaniesRouter


class BaseCompaniesAPI(BaseAPI):
	router: CompaniesRouter

	def make_router(self) -> CompaniesRouter:
		return CompaniesRouter()
