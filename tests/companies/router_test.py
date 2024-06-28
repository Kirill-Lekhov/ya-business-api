from ya_business_api.companies.router import CompaniesRouter


class TestCompaniesRouter:
	def test_companies(self):
		router = CompaniesRouter()
		assert router.companies() == "https://yandex.ru/sprav/api/companies"

	def test_chain_list(self):
		router = CompaniesRouter()
		assert router.chain_list(1) == "https://yandex.ru/sprav/api/view/chain/1/list/"
