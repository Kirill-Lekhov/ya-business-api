from ya_business_api.core.parser import BaseParser
from ya_business_api.core.exceptions import ParserError
from ya_business_api.companies.dataclasses.chain_list import CompanyCard

from bs4.element import Tag


class CompanyCardParser(BaseParser):
	def parse(self, node: Tag) -> CompanyCard:
		title_node = node.select_one("div.company-card__title")
		address_node = node.select_one("div.company-card__address")
		rubrics_node = node.select_one("div.company-card__rubrics")

		if not title_node:
			raise ParserError("Title doesn't exist")

		if not address_node:
			raise ParserError("Address doesn't exist")

		if not rubrics_node:
			raise ParserError("Rubrics doesn't exist")

		title_link_node = title_node.select_one('a.link.link__control')

		if not title_link_node:
			raise ParserError("Link doesn't exist in the title node")

		return CompanyCard(
			title=title_link_node.text.strip(),
			address=address_node.text.strip(),
			rubrics=rubrics_node.text.strip(),
		)
