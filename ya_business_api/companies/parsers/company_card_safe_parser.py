from ya_business_api.core.parser import BaseParser
from ya_business_api.companies.dataclasses.chain_list import CompanyCard
from ya_business_api.companies.parsers.company_card import CompanyCardParser
from ya_business_api.companies.parsers.company_card_with_photo import CompanyCardWithPhotoParser

from bs4.element import Tag


class CompanyCardSafeParser(BaseParser):
	"""
	Tries to parse company card with different parsers.
	"""
	company_card_with_photo_parser_cls = CompanyCardWithPhotoParser
	company_card_parser_cls = CompanyCardParser

	def __init__(self):
		self.company_card_with_photo_parser = self.company_card_with_photo_parser_cls()
		self.company_card_parser = self.company_card_parser_cls()

	def parse(self, node: Tag) -> CompanyCard:
		if node.select_one('div.company-card-with-photo.i-bem'):
			return self.company_card_with_photo_parser.parse(node)

		return self.company_card_parser.parse(node)
