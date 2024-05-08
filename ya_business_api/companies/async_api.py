from ya_business_api.core.mixins.asynchronous import AsyncAPIMixin
from ya_business_api.companies.base_api import BaseCompaniesAPI
from ya_business_api.companies.dataclasses.companies import CompaniesResponse
from ya_business_api.companies.dataclasses.requests import CompaniesRequest

from typing import Optional


class AsyncCompaniesAPI(AsyncAPIMixin, BaseCompaniesAPI):
	async def get_companies(self, request: Optional[CompaniesRequest] = None) -> CompaniesResponse:
		url = self.router.companies()
		request = request or CompaniesRequest()

		async with self.session.get(url, allow_redirects=False, params=request.as_query_params()) as response:
			self.check_response(response)
			return CompaniesResponse.from_dict(await response.json())
