from ya_business_api.companies.sync_api import SyncCompaniesAPI
from ya_business_api.companies.dataclasses.companies import CompaniesResponse
from ya_business_api.companies.dataclasses.chain_list import ChainListResponse
from ya_business_api.companies.dataclasses.requests import CompaniesRequest, ChainListRequest

from typing import Final
from json import dumps
from unittest.mock import patch

from requests.sessions import Session
from requests.models import Response


CHAIN_LIST_CONTENT: Final[str] = """
<div
	class="chain-branches__list i-bem"
	data-bem='{"chain-branches__list": {"val": [], "chainId": 1, "geoId": 1}}'
>
	<div class="list-view list-view_ajax i-bem" data-bem='{"list-view":{}}'>
		<div class="list-view__items">
			<div class="chain-branches__item">
				<div class="chain-branches__item-inner">
					<div class="chain-branches__cell">
						<div
							class="company-card-with-photo i-bem"
							data-bem='{
								"company-card-with-photo": {
									"type": "ordinal",
									"companyId": 0,
									"permalink": 0,
									"editPhotoUrl": "/sprav/0/p/edit/photos/",
									"url": "/sprav/0/p/edit/main",
									"noAccess": false,
									"name": "TITLE"
								}
							}'
						>
							<div class="company-card i-bem" data-bem='{"company-card":{}}'>
								<div class="company-card__title">
									<a
										class="link link_theme_islands link__control i-bem"
										data-bem='{"link":{}}' role="link" href="/sprav/0/p/edit/main"
									>
										TITLE
									</a>
								</div>
								<div class="company-card__content">
									<div class="company-card__address">ADDRESS</div>
									<div class="company-card__rubrics">RUBRICS</div>
									<div class="company-card__diffs">
										<a
											class="link link_theme_full-black company-card__diff link__control i-bem"
											data-bem='{"link":{}}' role="link" href="/sprav/0/p/edit/reviews"
										>
											0 отзыва
										</a>
										<a
											class="link link_theme_full-black company-card__diff link__control i-bem"
											data-bem='{"link":{}}' role="link" href="/sprav/0/p/edit/photos"
										>
											Фото
										</a>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div
			class="pager pager_data-source_tds pager_ajax i-bem"
			data-bem='{
				"pager": {
					"bemjson": {
						"totalPages": 2,
						"currentPage": 1,
						"params": {},
						"url": "localhost",
						"block": "pager",
						"mods": {
							"data-source": "tds",
							"ajax": true
						},
						"pager": {
							"offset": 0,
							"limit": 20,
							"total": 38
						},
						"path": "to happiness"
					}
				}
			}'
		>
			<div class="control-group" role="group">
				<button
					class="button button_theme_islands button_size_m button_togglable_radio button_checked button__control i-bem"
					data-bem='{"button":{"page":1}}'
					role="button"
					type="button"
					aria-pressed="true"
				>
					<span class="button__text">1</span>
				</button>
				<a
					class="button button_theme_islands button_size_m button_type_link button_togglable_radio button__control i-bem"
					data-bem='{"button":{"page":2}}'
					role="link"
					aria-pressed="false"
				>
					<span class="button__text">2</span>
				</a>
				<a
					class="button button_theme_islands button_size_m button_type_link button_togglable_radio button__control i-bem"
					data-bem='{"button":{"page":3}}'
					role="link"
					aria-pressed="false"
				>
					<span class="button__text">3</span>
				</a>
				<a
					class="button button_theme_islands button_size_m button_type_link button_togglable_radio button__control i-bem"
					data-bem='{"button":{"page":4}}'
					role="link"
					aria-pressed="false"
				>
					<span class="button__text">4</span>
				</a>
				<a
					class="button button_theme_islands button_size_m button_type_link button_togglable_radio button__control i-bem"
					data-bem='{"button":{"page":5}}'
					role="link"
					aria-pressed="false"
				>
					<span class="button__text">5</span>
				</a>
				<a
					class="button button_theme_islands button_size_m button_type_link button__control i-bem"
					data-bem='{"button":{"page":2}}'
					role="link"
				><span class="button__text">→</span></a>
			</div>
		</div>
		<span class="spin spin_theme_islands spin_size_m"></span>
		<div class="list-view__list-paranja"></div>
	</div>
</div>
"""


class TestSyncCompaniesAPI:
	def test_get_companies(self):
		session = Session()
		api = SyncCompaniesAPI("TOKEN", session)
		response = Response()
		response.status_code = 200
		data = {'limit': 10, 'listCompanies': [], 'page': 1, 'total': 0}
		response._content = dumps(data).encode()
		request = CompaniesRequest(filter="Company Name", page=10)

		with patch.object(session, 'get', return_value=response) as session_get_method:
			result = api.get_companies(request)
			assert isinstance(result, CompaniesResponse)
			assert result.limit == 10
			assert result.list_companies == []
			assert result.page == 1
			assert result.total == 0
			session_get_method.assert_called_once()
			assert session_get_method.call_args_list[0].kwargs['params'] == {"filter": "Company Name", "page": 10}

		with patch.object(session, 'get', return_value=response):
			result = api.get_companies(request, raw=True)
			assert isinstance(result, dict)
			assert result == data

	def test_get_chain_list(self):
		session = Session()
		api = SyncCompaniesAPI("TOKEN", session)
		response = Response()
		response.status_code = 200
		response._content = CHAIN_LIST_CONTENT.encode()
		request = ChainListRequest(tycoon_id=1, geo_id=5, page=10)

		with patch.object(session, 'post', return_value=response) as session_post_method:
			result = api.get_chain_list(request)
			assert isinstance(result, ChainListResponse)
			assert result.pager.bemjson.pager.total == 38
			assert result.chain_branches_list.chain_id == 1
			assert len(result.company_cards) == 1
			session_post_method.assert_called_once()
			assert session_post_method.call_args_list[0].kwargs['params'] == {"geo_id": 5, "page": 10}

		with patch.object(session, 'post', return_value=response):
			result = api.get_chain_list(request, raw=True)
			assert isinstance(result, str)
			assert result == CHAIN_LIST_CONTENT
