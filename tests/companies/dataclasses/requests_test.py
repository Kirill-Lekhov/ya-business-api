from ya_business_api.companies.dataclasses.requests import CompaniesRequest, ChainListRequest


class TestCompaniesRequest:
	def test_as_query_params(self):
		request = CompaniesRequest()
		assert request.as_query_params() == {}

		request = CompaniesRequest(filter="Filter value")
		assert request.as_query_params() == {"filter": "Filter value"}

		request = CompaniesRequest(page=10)
		assert request.as_query_params() == {"page": 10}

		request = CompaniesRequest(filter="Filter value", page=10)
		assert request.as_query_params() == {"filter": "Filter value", "page": 10}


class TestChainListRequest:
	def test_as_query_params(self):
		request = ChainListRequest(tycoon_id=1)
		assert request.as_query_params() == {}

		request = ChainListRequest(tycoon_id=1, geo_id=10)
		assert request.as_query_params() == {"geo_id": 10}

		request = ChainListRequest(tycoon_id=1, page=100)
		assert request.as_query_params() == {"page": 100}

		request = ChainListRequest(tycoon_id=1, geo_id=10, page=100)
		assert request.as_query_params() == {"geo_id": 10, "page": 100}
