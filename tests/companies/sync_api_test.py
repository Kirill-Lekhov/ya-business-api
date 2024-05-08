from ya_business_api.companies.sync_api import SyncCompaniesAPI
from ya_business_api.companies.dataclasses.companies import CompaniesResponse
from ya_business_api.companies.dataclasses.requests import CompaniesRequest

from json import dumps
from unittest.mock import patch

from requests.sessions import Session
from requests.models import Response


class TestSyncCompaniesAPI:
	def test_get_companies(self):
		session = Session()
		api = SyncCompaniesAPI(session)
		response = Response()
		response.status_code = 200
		response._content = dumps({'limit': 10, 'listCompanies': [], 'page': 1, 'total': 0}).encode()
		request = CompaniesRequest(filter="Company Name", page=10)

		with patch.object(session, 'get', return_value=response) as session_get_method:
			result = api.get_companies(request)
			assert isinstance(result, CompaniesResponse)
			assert result.limit == 10
			assert result.listCompanies == []
			assert result.page == 1
			assert result.total == 0
			session_get_method.assert_called_once()
			assert session_get_method.call_args_list[0].kwargs['params'] == {"filter": "Company Name", "page": 10}
