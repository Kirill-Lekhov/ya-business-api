from ya_business_api.companies.base_api import BaseCompaniesAPI
from ya_business_api.companies.router import CompaniesRouter


class TestBaseAPI:
	def test_make_router(self):
		api = BaseCompaniesAPI()
		assert isinstance(api.make_router(), CompaniesRouter)

