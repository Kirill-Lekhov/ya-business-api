from ya_business_api.core.mixins.asynchronous import AsyncAPIMixin
from ya_business_api.core.constants import CSRF_TOKEN_HEADER
from ya_business_api.companies.base_api import BaseCompaniesAPI
from ya_business_api.companies.dataclasses.companies import CompaniesResponse
from ya_business_api.companies.dataclasses.chain_list import ChainListResponse
from ya_business_api.companies.dataclasses.requests import CompaniesRequest, ChainListRequest
from ya_business_api.companies.parsers.chain_list_response import ChainListResponseParser

from typing import Optional, Union, Literal, overload
from time import monotonic
from logging import getLogger; log = getLogger(__name__)

from aiohttp.client import ClientSession


class AsyncCompaniesAPI(AsyncAPIMixin, BaseCompaniesAPI):
	chain_list_response_parser_csl = ChainListResponseParser

	def __init__(self, csrf_token: str, session: ClientSession) -> None:
		super().__init__(session, csrf_token)

		self.chain_list_response_parser = self.chain_list_response_parser_csl()

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
		time_start = monotonic()

		async with self.session.get(url, allow_redirects=False, params=request.as_query_params()) as response:
			log.debug(f"A:COMPANIES[{response.status}] {monotonic() - time_start:.1f}s")
			self.check_response(response)

			if raw:
				return await response.json()

			return CompaniesResponse.model_validate_json(await response.text())

	@overload
	async def get_chain_list(self, request: ChainListRequest, *, raw: Literal[True]) -> str: ...

	@overload
	async def get_chain_list(self, request: ChainListRequest, *, raw: Literal[False] = False) -> ChainListResponse: ...

	async def get_chain_list(self, request: ChainListRequest, *, raw: bool = False) -> Union[ChainListResponse, str]:
		url = self.router.chain_list(request.tycoon_id)
		self.set_i_cookie()
		headers = {CSRF_TOKEN_HEADER: self.csrf_token}
		time_start = monotonic()

		async with self.session.post(
			url,
			params=request.as_query_params(),
			headers=headers,
			allow_redirects=False,
		) as response:
			log.debug(f"A:CHAIN_LIST[{response.status}] {monotonic() - time_start:.1f}s")
			self.check_response(response)
			content = await response.text()

			if raw:
				return content

			return self.chain_list_response_parser.parse(content)
