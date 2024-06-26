from ya_business_api.core.mixins.asynchronous import AsyncAPIMixin
from ya_business_api.companies.base_api import BaseCompaniesAPI
from ya_business_api.companies.dataclasses.companies import CompaniesResponse
from ya_business_api.companies.dataclasses.requests import CompaniesRequest

from typing import Optional, Union, Literal, overload


class AsyncCompaniesAPI(AsyncAPIMixin, BaseCompaniesAPI):
	@overload
	async def get_companies(self, request: Optional[CompaniesRequest] = None, *, raw: Literal[True]) -> dict: ...

	@overload
	async def get_companies(
		self,
		request: Optional[CompaniesRequest] = None,
		*,
		raw: Literal[False] = False,
	) -> CompaniesResponse: ...

	async def get_companies(
		self,
		request: Optional[CompaniesRequest] = None,
		*,
		raw: bool = False,
	) -> Union[CompaniesResponse, dict]:
		url = self.router.companies()
		request = request or CompaniesRequest()

		async with self.session.get(url, allow_redirects=False, params=request.as_query_params()) as response:
			self.check_response(response)

			if raw:
				return await response.json()

			return CompaniesResponse.model_validate_json(await response.text())
