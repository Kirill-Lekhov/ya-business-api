from ya_business_api.companies.router import CompaniesRouter


class TestCompaniesRouter:
	def test_get_companies(self):
		router = CompaniesRouter()
		assert router.companies() == "https://yandex.ru/sprav/api/companies"
