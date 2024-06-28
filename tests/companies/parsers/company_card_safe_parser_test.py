from ya_business_api.companies.dataclasses.chain_list import CompanyCard, CompanyCardWithPhoto
from ya_business_api.companies.parsers.company_card_safe_parser import CompanyCardSafeParser

from typing import Final

from bs4 import BeautifulSoup


CARD_WITH_PHOTO_SOUP: Final[BeautifulSoup] = BeautifulSoup(
	"""
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
						data-bem='{"link":{}}' role="link"
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
	""",
	"html.parser",
)
SIPLE_CARD_SOUP: Final[BeautifulSoup] = BeautifulSoup(
	"""
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
	""",
	"html.parser",
)


class TestCompanyCardSafeParser:
	def test_parse(self):
		parser = CompanyCardSafeParser()
		node = CARD_WITH_PHOTO_SOUP.select_one("div")
		assert node
		company_card = parser.parse(node)
		assert isinstance(company_card, CompanyCardWithPhoto)

		node = SIPLE_CARD_SOUP.select_one("div")
		assert node
		company_card = parser.parse(node)
		assert isinstance(company_card, CompanyCard)
