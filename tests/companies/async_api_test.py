from ya_business_api.companies.async_api import AsyncCompaniesAPI
from ya_business_api.companies.dataclasses.companies import CompaniesResponse
from ya_business_api.companies.dataclasses.requests import CompaniesRequest, ChainBranchesRequest
from ya_business_api.companies.dataclasses.chain_branches import ChainBranchesResponse
from tests.aiohttp import Response, RequestContextManager

from json import dumps
from unittest.mock import patch

import pytest
from aiohttp.client import ClientSession


@pytest.mark.asyncio
class TestAsyncCompaniesAPI:
	async def test_get_companies(self):
		session = ClientSession()
		api = AsyncCompaniesAPI("TOKEN", session)
		response = Response()
		data = {'limit': 10, 'listCompanies': [], 'page': 1, 'total': 0}
		response.content = dumps(data)
		request = CompaniesRequest(filter="Company Name", page=10)
		request_context_manager = RequestContextManager(response)

		with patch.object(session, 'get', return_value=request_context_manager) as session_get_method:
			result = await api.get_companies(request)
			assert isinstance(result, CompaniesResponse)
			assert result.limit == 10
			assert result.list_companies == []
			assert result.page == 1
			assert result.total == 0
			session_get_method.assert_called_once()
			assert session_get_method.call_args_list[0].kwargs['params'] == {"filter": "Company Name", "page": 10}

		with patch.object(session, 'get', return_value=request_context_manager):
			result = await api.get_companies(request, raw=True)
			assert isinstance(result, dict)
			assert result == data

	async def test_get_chain_branches(self):
		session = ClientSession()
		api = AsyncCompaniesAPI("TOKEN", session)
		response = Response()
		data = {
			"companyIds": [1, 2, 3],
			"companyList": {
				"pager": {
					"offset": 0, "limit": 20, "total": 100,
				},
				"companies": [],
				"chain": None,
			},
		}
		response.content = dumps(data)
		request = ChainBranchesRequest(tycoon_id=1, permanent_id=2, geo_id=3, page=64)
		request_context_manager = RequestContextManager(response)

		with patch.object(session, "get", return_value=request_context_manager) as session_get_method:
			result = await api.get_chain_branches(request)
			assert isinstance(result, ChainBranchesResponse)
			assert result.company_ids == [1, 2, 3]
			assert result.chain_data.pager.offset == 0
			assert result.chain_data.pager.limit == 20
			assert result.chain_data.pager.total == 100
			assert result.chain_data.companies == []
			assert result.chain_data.chain is None
			session_get_method.assert_called_once()
			assert session_get_method.call_args_list[0].kwargs["params"] == {
				"page": 64,
				"chainPermalink": 2,
				"geoId": 3,
			}

		with patch.object(session, "get", return_value=request_context_manager):
			result = await api.get_chain_branches(request, raw=True)
			assert isinstance(result, dict)
			assert result == data
