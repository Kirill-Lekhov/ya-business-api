from typing import List

from pydantic.main import BaseModel
from pydantic.fields import Field


class ChainBranchesList(BaseModel):
	val: List[int]
	chain_id: int = Field(alias="chainId")
	geo_id: int = Field(alias="geoId")


class PagerBemJSONMods(BaseModel):
	data_source: str = Field(alias="data-source")
	ajax: bool


class PagerBemJSONPager(BaseModel):
	offset: int
	limit: int
	total: int


class PagerBemJSON(BaseModel):
	total_pages: int = Field(alias="totalPages")
	current_page: int = Field(alias="currentPage")
	params: dict
	url: str
	block: str
	mods: PagerBemJSONMods
	pager: PagerBemJSONPager
	path: str


class Pager(BaseModel):
	bemjson: PagerBemJSON


class CompanyCard(BaseModel):
	title: str
	address: str
	rubrics: str


class CompanyCardWithPhoto(CompanyCard):
	type: str		# ordinal
	company_id: int = Field(alias="companyId")
	permalink: int
	edit_photo_url: str = Field(alias="editPhotoUrl")
	url: str
	no_access: bool = Field(alias="noAccess")
	name: str


class ChainListResponse(BaseModel):
	chain_branches_list: ChainBranchesList
	company_cards: List[CompanyCard]
	pager: Pager
