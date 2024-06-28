from ya_business_api.core.exceptions import ParserError
from ya_business_api.companies.parsers.pager import PagerParser
from ya_business_api.companies.dataclasses.chain_list import Pager

from typing import Final

import pytest
from bs4 import BeautifulSoup


INCORRECT_SOUP: Final[BeautifulSoup] = BeautifulSoup("<div></div>", "html.parser")
CORRECT_SOUP: Final[BeautifulSoup] = BeautifulSoup(
	"""
	<div data-bem='{
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
	}'></div>
	""",
	"html.parser",
)


class TestPagerParser:
	def test_parse(self):
		parser = PagerParser()
		node = CORRECT_SOUP.select_one("div")
		assert node
		pager = parser.parse(node)
		assert isinstance(pager, Pager)

	def test_parser__parser_error(self):
		parser = PagerParser()
		node = INCORRECT_SOUP.select_one("div")
		assert node

		with pytest.raises(ParserError, match="data-bem attribute doesn't exist"):
			parser.parse(node)
