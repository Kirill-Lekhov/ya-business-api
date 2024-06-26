from ya_business_api.companies.async_api import AsyncCompaniesAPI
from ya_business_api.companies.dataclasses.companies import CompaniesResponse
from ya_business_api.companies.dataclasses.requests import CompaniesRequest
from tests.aiohttp import Response, RequestContextManager

from json import dumps
from unittest.mock import patch

import pytest
from aiohttp.client import ClientSession


@pytest.mark.asyncio
class TestAsyncCompaniesAPI:
	async def test_get_companies(self):
		session = ClientSession()
		api = AsyncCompaniesAPI(session)
		response = Response()
		data = {'limit': 10, 'listCompanies': [], 'page': 1, 'total': 0}
		response.content = dumps(data)
		request = CompaniesRequest(filter="Company Name", page=10)
		request_context_manager = RequestContextManager(response)

		with patch.object(session, 'get', return_value=request_context_manager) as session_get_method:
			result = await api.get_companies(request)
			assert isinstance(result, CompaniesResponse)
			assert result.limit == 10
			assert result.listCompanies == []
			assert result.page == 1
			assert result.total == 0
			session_get_method.assert_called_once()
			assert session_get_method.call_args_list[0].kwargs['params'] == {"filter": "Company Name", "page": 10}

		with patch.object(session, 'get', return_value=request_context_manager) as session_get_method:
			result = await api.get_companies(request, raw=True)
			assert isinstance(result, dict)
			assert result == data
