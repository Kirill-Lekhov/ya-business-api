from ya_business_api.core.exceptions import ParserError
from ya_business_api.companies.parsers.chain_list_response import ChainListResponseParser
from ya_business_api.companies.dataclasses.chain_list import ChainListResponse

from typing import Final

import pytest
from bs4 import BeautifulSoup


CORRECT_CONTENT: Final[str] = """
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
CONTENT_WITHOUT_CHAIN_BRANCHES_LIST: Final[str] = "<div></div>"
CONTENT_WITHOUT_PAGER: Final[str] = """
<div
	class="chain-branches__list i-bem"
	data-bem='{"chain-branches__list": {"val": [], "chainId": 1, "geoId": 1}}'
></div>
"""


class TestChainListResponseParser:
	def test_parse(self):
		parser = ChainListResponseParser()
		chain_list_response = parser.parse(CORRECT_CONTENT)
		assert isinstance(chain_list_response, ChainListResponse)

	def test_parse__without_chain_branches_list(self):
		parser = ChainListResponseParser()

		with pytest.raises(ParserError, match="Chain branches list node doesn't exist"):
			parser.parse(CONTENT_WITHOUT_CHAIN_BRANCHES_LIST)

	def test_parse__without_pager(self):
		parser = ChainListResponseParser()

		with pytest.raises(ParserError, match="Pager node doesn't exist"):
			parser.parse(CONTENT_WITHOUT_PAGER)

	def test_parser_company_cards(self):
		parser = ChainListResponseParser()
		assert parser.parse_company_cards([]) == []

		soup = BeautifulSoup(CORRECT_CONTENT, "html.parser")
		nodes = soup.select("div.chain-branches__item")
		company_cards = parser.parse_company_cards(nodes)
		assert len(company_cards) == 1
