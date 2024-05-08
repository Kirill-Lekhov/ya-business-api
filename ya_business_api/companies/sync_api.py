from ya_business_api.core.mixins.synchronous import SyncAPIMixin
from ya_business_api.companies.base_api import BaseCompaniesAPI
from ya_business_api.companies.dataclasses.companies import CompaniesResponse
from ya_business_api.companies.dataclasses.requests import CompaniesRequest

from typing import Optional


class SyncCompaniesAPI(SyncAPIMixin, BaseCompaniesAPI):
	def get_companies(self, request: Optional[CompaniesRequest] = None) -> CompaniesResponse:
		url = self.router.companies()
		request = request or CompaniesRequest()
		response = self.session.get(url, allow_redirects=False, params=request.as_query_params())
		self.check_response(response)
		return CompaniesResponse.from_dict(response.json())
