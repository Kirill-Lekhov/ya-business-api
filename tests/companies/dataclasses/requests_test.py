from ya_business_api.companies.dataclasses.requests import CompaniesRequest


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
