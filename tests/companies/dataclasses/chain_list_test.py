from ya_business_api.companies.dataclasses.chain_list import (
	ChainBranchesList, Pager, PagerBemJSON, PagerBemJSONMods, PagerBemJSONPager, CompanyCard, CompanyCardWithPhoto,
	ChainListResponse,
)


def make_chain_branches_list() -> dict:
	return {
		"val": [1, 2, 3],
		"chainId": 0,
		"geoId": 0,
	}


def make_pager_bem_json_mods() -> dict:
	return {
		"data-source": "test",
		"ajax": True,
	}


def make_pager_bem_json_pager() -> dict:
	return {
		"offset": 20,
		"limit": 20,
		"total": 1000,
	}


def make_pager_bem_json() -> dict:
	return {
		"totalPages": 100,
		"currentPage": 1,
		"params": {"unknown": "params"},
		"url": "localhost",
		"block": "of gold",
		"mods": make_pager_bem_json_mods(),
		"pager": make_pager_bem_json_pager(),
		"path": "to happiness",
	}


def make_pager() -> dict:
	return {
		"bemjson": make_pager_bem_json(),
	}


def make_company_card() -> dict:
	return {
		"title": "Anecdote",
		"address": "Pushkin Street, Kolotushkin house",
		"rubrics": "jokes",
	}


def make_company_card_with_photo() -> dict:
	return {
		"type": "ordinal",
		"companyId": 1,
		"permalink": 1,
		"editPhotoUrl": "localhost:80",
		"url": "localhost:443",
		"noAccess": False,
		"name": "Nameless",
		**make_company_card(),
	}


def make_chain_list_response() -> dict:
	return {
		"chain_branches_list": make_chain_branches_list(),
		"company_cards": [],
		"pager": make_pager(),
	}


class TestChainBranchesList:
	def test_validation(self):
		chain_branches_list = ChainBranchesList(**make_chain_branches_list())
		assert isinstance(chain_branches_list, ChainBranchesList)
		assert chain_branches_list.val == [1, 2, 3]
		assert chain_branches_list.chain_id == 0
		assert chain_branches_list.geo_id == 0


class TestPagerBemJSONMods:
	def test_validation(self):
		pager_bem_json_mods = PagerBemJSONMods(**make_pager_bem_json_mods())
		assert isinstance(pager_bem_json_mods, PagerBemJSONMods)
		assert pager_bem_json_mods.data_source == "test"
		assert pager_bem_json_mods.ajax == True


class TestPagerBemJSONPager:
	def test_validation(self):
		pager_bem_json_pager = PagerBemJSONPager(**make_pager_bem_json_pager())
		assert isinstance(pager_bem_json_pager, PagerBemJSONPager)
		assert pager_bem_json_pager.offset == 20
		assert pager_bem_json_pager.limit == 20
		assert pager_bem_json_pager.total == 1000


class TestPagerBemJSON:
	def test_validation(self):
		pager_bem_json = PagerBemJSON(**make_pager_bem_json())
		assert isinstance(pager_bem_json, PagerBemJSON)
		assert isinstance(pager_bem_json.mods, PagerBemJSONMods)
		assert isinstance(pager_bem_json.pager, PagerBemJSONPager)
		assert pager_bem_json.total_pages == 100
		assert pager_bem_json.current_page == 1
		assert pager_bem_json.params == {"unknown": "params"}
		assert pager_bem_json.url == "localhost"
		assert pager_bem_json.block == "of gold"
		assert pager_bem_json.path == "to happiness"


class TestPager:
	def test_validation(self):
		pager = Pager(**make_pager())
		assert isinstance(pager, Pager)
		assert isinstance(pager.bemjson, PagerBemJSON)


class TestCompanyCard:
	def test_validation(self):
		company_card = CompanyCard(**make_company_card())
		assert isinstance(company_card, CompanyCard)
		assert company_card.title == "Anecdote"
		assert company_card.address == "Pushkin Street, Kolotushkin house"
		assert company_card.rubrics == "jokes"


class TestCompanyCardWithPhoto:
	def test_validation(self):
		company_card_with_photo = CompanyCardWithPhoto(**make_company_card_with_photo())
		assert isinstance(company_card_with_photo, CompanyCardWithPhoto)
		assert company_card_with_photo.title == "Anecdote"
		assert company_card_with_photo.address == "Pushkin Street, Kolotushkin house"
		assert company_card_with_photo.rubrics == "jokes"
		assert company_card_with_photo.type == "ordinal"
		assert company_card_with_photo.company_id == 1
		assert company_card_with_photo.permalink == 1
		assert company_card_with_photo.edit_photo_url == "localhost:80"
		assert company_card_with_photo.url == "localhost:443"
		assert company_card_with_photo.no_access == False
		assert company_card_with_photo.name == "Nameless"


class TestChainListResponse:
	def test_validation(self):
		chain_list_response_raw = make_chain_list_response()
		chain_list_response_raw['company_cards'] = [
			make_company_card(),
			make_company_card_with_photo(),
		]
		chain_list_response = ChainListResponse(**chain_list_response_raw)
		assert isinstance(chain_list_response, ChainListResponse)
		assert isinstance(chain_list_response.chain_branches_list, ChainBranchesList)
		assert isinstance(chain_list_response.pager, Pager)
		assert isinstance(chain_list_response.company_cards, list)
		assert len(chain_list_response.company_cards) == 2
		assert isinstance(chain_list_response.company_cards[0], CompanyCard)
		assert isinstance(chain_list_response.company_cards[1], CompanyCard)

		chain_list_response_raw['company_cards'] = [
			CompanyCard(**make_company_card()),
			CompanyCardWithPhoto(**make_company_card_with_photo()),
		]
		chain_list_response = ChainListResponse(**chain_list_response_raw)
		assert len(chain_list_response.company_cards) == 2
		assert isinstance(chain_list_response.company_cards[0], CompanyCard)
		assert isinstance(chain_list_response.company_cards[1], CompanyCardWithPhoto)
