from ya_business_api.core.mixins.synchronous import SyncAPIMixin
from ya_business_api.companies.base_api import BaseCompaniesAPI
from ya_business_api.companies.dataclasses.companies import CompaniesResponse
from ya_business_api.companies.dataclasses.chain_branches import ChainBranchesResponse
from ya_business_api.companies.dataclasses.requests import CompaniesRequest, ChainBranchesRequest

from typing import Optional, Union, Literal, overload

from requests.sessions import Session


class SyncCompaniesAPI(SyncAPIMixin, BaseCompaniesAPI):
	def __init__(self, csrf_token: str, session: Session) -> None:
		super().__init__(session, csrf_token)

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

	@overload
	def get_chain_branches(self, request: ChainBranchesRequest, *, raw: Literal[True]) -> dict: ...

	@overload
	def get_chain_branches(
		self,
		request: ChainBranchesRequest,
		*,
		raw: Literal[False] = False,
	) -> ChainBranchesResponse: ...

	def get_chain_branches(
		self,
		request: ChainBranchesRequest,
		*,
		raw: bool = False,
	) -> Union[ChainBranchesResponse, dict]:
		url = self.router.chain_branches(request.tycoon_id)
		response = self.session.get(url, allow_redirects=False, params=request.as_query_params())
		self.check_response(response)

		if raw:
			return response.json()

		return ChainBranchesResponse.model_validate_json(response.text)
