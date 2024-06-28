from typing import List

from pydantic import BaseModel, Field


class ChainBranchesList(BaseModel):
	val: List[int]
	chainId: int
	geoId: int


class PagerBemJSONMods(BaseModel):
	data_source: str = Field(alias="data-source")
	ajax: bool


class PagerBemJSONPager(BaseModel):
	offset: int
	limit: int
	total: int


class PagerBemJSON(BaseModel):
	totalPages: int
	currentPage: int
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
	companyId: int
	permalink: int
	editPhotoUrl: str
	url: str
	noAccess: bool
	name: str


class ChainListResponse(BaseModel):
	chain_branches_list: ChainBranchesList
	company_cards: List[CompanyCard]
	pager: Pager
