from ya_business_api.companies.router import CompaniesRouter


class TestCompaniesRouter:
	def test_companies(self):
		router = CompaniesRouter()
		assert router.companies() == "https://yandex.ru/sprav/api/companies"

	def test_chain_branches(self):
		router = CompaniesRouter()
		assert router.chain_branches(1) == "https://yandex.ru/sprav/api/chain/1/branches/"
