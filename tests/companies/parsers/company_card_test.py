from ya_business_api.core.exceptions import ParserError
from ya_business_api.companies.dataclasses.chain_list import CompanyCard
from ya_business_api.companies.parsers.company_card import CompanyCardParser

from typing import Final

import pytest
from bs4 import BeautifulSoup


SOUP_WITHOUT_TITLE: Final[BeautifulSoup] = BeautifulSoup(
	"""
	<div class="company-card i-bem" data-bem='{"company-card":{}}'>
	</div>
	""",
	"html.parser"
)
SOUP_WITHOUT_ADDRESS: Final[BeautifulSoup] = BeautifulSoup(
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
	</div>
	""",
	"html.parser"
)
SOUP_WITHOUT_RUBRICS: Final[BeautifulSoup] = BeautifulSoup(
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
		</div>
	</div>
	""",
	"html.parser"
)
SOUP_WITHOUT_LINK_CONTROL: Final[BeautifulSoup] = BeautifulSoup(
	"""
	<div class="company-card i-bem" data-bem='{"company-card":{}}'>
		<div class="company-card__title"></div>
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
	"html.parser"
)
CORRECT_SOUP: Final[BeautifulSoup] = BeautifulSoup(
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
	"html.parser"
)


class TestCompanyCardParser:
	def test_parse(self):
		parser = CompanyCardParser()
		node = CORRECT_SOUP.select_one('div')
		assert node
		company_card = parser.parse(node)
		assert isinstance(company_card, CompanyCard)
		assert company_card.title == "TITLE"
		assert company_card.address == "ADDRESS"
		assert company_card.rubrics == "RUBRICS"

	def test_parse__without_title(self):
		parser = CompanyCardParser()
		node = SOUP_WITHOUT_TITLE.select_one('div')
		assert node

		with pytest.raises(ParserError, match="Title doesn't exist"):
			parser.parse(node)

	def test_parse__without_address(self):
		parser = CompanyCardParser()
		node = SOUP_WITHOUT_ADDRESS.select_one('div')
		assert node

		with pytest.raises(ParserError, match="Address doesn't exist"):
			parser.parse(node)

	def test_parse__without_rubrics(self):
		parser = CompanyCardParser()
		node = SOUP_WITHOUT_RUBRICS.select_one('div')
		assert node

		with pytest.raises(ParserError, match="Rubrics doesn't exist"):
			parser.parse(node)

	def test_parse__without_link_control(self):
		parser = CompanyCardParser()
		node = SOUP_WITHOUT_LINK_CONTROL.select_one('div')
		assert node

		with pytest.raises(ParserError, match="Link doesn't exist in the title node"):
			parser.parse(node)
