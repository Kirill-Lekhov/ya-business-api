from ya_business_api.core.exceptions import ParserError
from ya_business_api.companies.dataclasses.chain_list import ChainBranchesList
from ya_business_api.companies.parsers.chain_branches_list import ChainBranchesListParser

from typing import Final

import pytest
from bs4 import BeautifulSoup


INCORRECT_SOUP: Final[BeautifulSoup] = BeautifulSoup("<div></div>", "html.parser")
CORRECT_SOUP: Final[BeautifulSoup] = BeautifulSoup(
	"""<div data-bem='{"chain-branches__list": {"val": [], "chainId": 1, "geoId": 1}}'></div>""",
	"html.parser",
)


class TestChainBranchesListParser:
	def test_parse(self):
		parser = ChainBranchesListParser()
		node = CORRECT_SOUP.select_one("div")
		assert node
		chain_branches_list = parser.parse(node)
		assert isinstance(chain_branches_list, ChainBranchesList)

	def test_parse__parser_error(self):
		parser = ChainBranchesListParser()
		node = INCORRECT_SOUP.select_one("div")
		assert node

		with pytest.raises(ParserError, match="data-bem attribute doesn't exist"):
			parser.parse(node)
