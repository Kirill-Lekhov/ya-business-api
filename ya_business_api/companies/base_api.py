from ya_business_api.core.base_api import BaseAPI
from ya_business_api.companies.router import CompaniesRouter


class BaseCompaniesAPI(BaseAPI):
	csrf_token: str
	router: CompaniesRouter

	def __init__(self, csrf_token: str) -> None:
		self.csrf_token = csrf_token

		super().__init__()

	def make_router(self) -> CompaniesRouter:
		return CompaniesRouter()
