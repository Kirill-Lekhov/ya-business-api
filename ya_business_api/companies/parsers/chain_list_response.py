from ya_business_api.core.parser import BaseParser
from ya_business_api.core.exceptions import ParserError
from ya_business_api.companies.dataclasses.chain_list import ChainListResponse, CompanyCard
from ya_business_api.companies.parsers.pager import PagerParser
from ya_business_api.companies.parsers.chain_branches_list import ChainBranchesListParser
from ya_business_api.companies.parsers.company_card_safe_parser import CompanyCardSafeParser

from typing import Iterable, List

from bs4 import BeautifulSoup
from bs4.element import Tag


class ChainListResponseParser(BaseParser):
	chain_branches_list_parser_cls = ChainBranchesListParser
	company_card_parser_cls = CompanyCardSafeParser
	pager_parser_cls = PagerParser

	def __init__(self):
		self.pager_parser = self.pager_parser_cls()
		self.company_card_parser = self.company_card_parser_cls()
		self.chain_branches_list_parser = self.chain_branches_list_parser_cls()

	def parse(self, content: str) -> ChainListResponse:
		soup = BeautifulSoup(content, "html.parser")
		chain_branches_list_node = soup.select_one("div.chain-branches__list.i-bem")
		pager_node = soup.select_one("div.pager.i-bem")

		if not chain_branches_list_node:
			raise ParserError("Chain branches list node doesn't exist")

		if not pager_node:
			raise ParserError("Pager node doesn't exist")

		chain_branches_list = self.chain_branches_list_parser.parse(chain_branches_list_node)
		company_cards = self.parse_company_cards(soup.select("div.chain-branches__item"))
		pager = self.pager_parser.parse(pager_node)

		return ChainListResponse(chain_branches_list=chain_branches_list, company_cards=company_cards, pager=pager)

	def parse_company_cards(self, nodes: Iterable[Tag]) -> List[CompanyCard]:
		items = []

		for node in nodes:
			items.append(self.company_card_parser.parse(node))

		return items
