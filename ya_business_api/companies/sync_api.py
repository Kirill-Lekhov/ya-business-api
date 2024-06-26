from ya_business_api.core.mixins.synchronous import SyncAPIMixin
from ya_business_api.companies.base_api import BaseCompaniesAPI
from ya_business_api.companies.dataclasses.companies import CompaniesResponse
from ya_business_api.companies.dataclasses.requests import CompaniesRequest

from typing import Optional, Union, Literal, overload


class SyncCompaniesAPI(SyncAPIMixin, BaseCompaniesAPI):
	@overload
	def get_companies(self, request: Optional[CompaniesRequest] = None, *, raw: Literal[True]) -> dict: ...

	@overload
	def get_companies(
		self,
		request: Optional[CompaniesRequest] = None,
		*,
		raw: Literal[False] = False,
	) -> CompaniesResponse: ...

	def get_companies(
		self,
		request: Optional[CompaniesRequest] = None,
		*,
		raw: bool = False,
	) -> Union[CompaniesResponse, dict]:
		url = self.router.companies()
		request = request or CompaniesRequest()
		response = self.session.get(url, allow_redirects=False, params=request.as_query_params())
		self.check_response(response)

		if raw:
			return response.json()

		return CompaniesResponse.model_validate_json(response.text)
