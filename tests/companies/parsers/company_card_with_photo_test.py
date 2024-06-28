from ya_business_api.core.exceptions import ParserError
from ya_business_api.companies.dataclasses.chain_list import CompanyCardWithPhoto
from ya_business_api.companies.parsers.company_card_with_photo import CompanyCardWithPhotoParser

from typing import Final

import pytest
from bs4 import BeautifulSoup


SOUP_WITHOUT_COMPANY_CARD_INFO: Final[BeautifulSoup] = BeautifulSoup(
	"""
	<div class="chain-branches__item">
		<div class="chain-branches__item-inner">
			<div class="chain-branches__cell">
			</div>
		</div>
	</div>
	""",
	"html.parser",
)
SOUP_WITHOUT_DATA_BEM: Final[BeautifulSoup] = BeautifulSoup(
	"""
	<div class="chain-branches__item">
		<div class="chain-branches__item-inner">
			<div class="chain-branches__cell">
				<div
					class="company-card-with-photo i-bem"
				>
				</div>
			</div>
		</div>
	</div>
	""",
	"html.parser",
)
CORRECT_SOUP: Final[BeautifulSoup] = BeautifulSoup(
	"""
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
								data-bem='{"link":{}}'
								role="link"
								href="/sprav/0/p/edit/main"
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
									data-bem='{"link":{}}'
									role="link"
									href="/sprav/0/p/edit/reviews"
								>
									0 отзыва
								</a>
								<a
									class="link link_theme_full-black company-card__diff link__control i-bem"
									data-bem='{"link":{}}'
									role="link"
									href="/sprav/0/p/edit/photos"
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
	""",
	"html.parser",
)


class TestCompanyCardWithPhotoParser:
	def test_parse(self):
		parser = CompanyCardWithPhotoParser()
		node = CORRECT_SOUP.select_one("div")
		assert node
		company_card_with_photo = parser.parse(node)
		assert isinstance(company_card_with_photo, CompanyCardWithPhoto)

	def test_parse__without_company_card_info(self):
		parser = CompanyCardWithPhotoParser()
		node = SOUP_WITHOUT_COMPANY_CARD_INFO.select_one("div")
		assert node

		with pytest.raises(ParserError, match="Company card with photo doesn't exist"):
			parser.parse(node)

	def test_parse__without_data_bem(self):
		parser = CompanyCardWithPhotoParser()
		node = SOUP_WITHOUT_DATA_BEM.select_one("div")
		assert node

		with pytest.raises(ParserError, match="data-bem attribute doesn't exist"):
			parser.parse(node)
