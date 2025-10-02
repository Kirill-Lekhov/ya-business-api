from ya_business_api.core.mixins.asynchronous import AsyncAPIMixin
from ya_business_api.companies.base_api import BaseCompaniesAPI
from ya_business_api.companies.dataclasses.companies import CompaniesResponse
from ya_business_api.companies.dataclasses.chain_branches import ChainBranchesResponse
from ya_business_api.companies.dataclasses.requests import CompaniesRequest, ChainBranchesRequest

from typing import Optional, Union, Literal, overload
from time import monotonic
from logging import getLogger; log = getLogger(__name__)

from aiohttp.client import ClientSession


class AsyncCompaniesAPI(AsyncAPIMixin, BaseCompaniesAPI):
	def __init__(self, csrf_token: str, session: ClientSession) -> None:
		super().__init__(session, csrf_token)

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
	async def get_chain_branches(self, request: ChainBranchesRequest, *, raw: Literal[True]) -> dict: ...

	@overload
	async def get_chain_branches(
		self,
		request: ChainBranchesRequest,
		*,
		raw: Literal[False] = False,
	) -> ChainBranchesResponse: ...

	async def get_chain_branches(
		self,
		request: ChainBranchesRequest,
		*,
		raw: bool = False,
	) -> Union[ChainBranchesResponse, dict]:
		url = self.router.chain_branches(request.tycoon_id)
		time_start = monotonic()

		async with self.session.get(url, params=request.as_query_params(), allow_redirects=False) as response:
			log.debug(f"A:CHAIN_BRANCHES[{response.status}] {monotonic() - time_start:.1f}s")
			self.check_response(response)

			if raw:
				return await response.json()

			return ChainBranchesResponse.model_validate_json(await response.text())
