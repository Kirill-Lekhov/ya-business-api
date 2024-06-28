from ya_business_api.core.mixins.synchronous import SyncAPIMixin
from ya_business_api.core.constants import CSRF_TOKEN_HEADER
from ya_business_api.companies.base_api import BaseCompaniesAPI
from ya_business_api.companies.dataclasses.companies import CompaniesResponse
from ya_business_api.companies.dataclasses.chain_list import ChainListResponse
from ya_business_api.companies.dataclasses.requests import CompaniesRequest, ChainListRequest
from ya_business_api.companies.parsers.chain_list_response import ChainListResponseParser

from typing import Optional, Union, Literal, overload

from requests.sessions import Session


class SyncCompaniesAPI(SyncAPIMixin, BaseCompaniesAPI):
	chain_list_response_parser_cls = ChainListResponseParser

	def __init__(self, csrf_token: str, session: Session) -> None:
		super().__init__(session, csrf_token)

		self.chain_list_response_parser = self.chain_list_response_parser_cls()

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
	def get_chain_list(self, request: ChainListRequest, *, raw: Literal[True]) -> str: ...

	@overload
	def get_chain_list(self, request: ChainListRequest, *, raw: Literal[False] = False) -> ChainListResponse: ...

	def get_chain_list(self, request: ChainListRequest, *, raw: bool = False) -> Union[ChainListResponse, str]:
		url = self.router.chain_list(request.tycoon_id)
		self.set_i_cookie()
		headers = {CSRF_TOKEN_HEADER: self.csrf_token}
		response = self.session.post(url, allow_redirects=False, params=request.as_query_params(), headers=headers)
		self.check_response(response)
		content = response.text

		if raw:
			return content

		return self.chain_list_response_parser.parse(content)
