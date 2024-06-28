from ya_business_api.core.exceptions import ParserError
from ya_business_api.companies.dataclasses.chain_list import CompanyCardWithPhoto
from ya_business_api.companies.parsers.company_card import CompanyCardParser

from json import loads

from bs4.element import Tag


class CompanyCardWithPhotoParser(CompanyCardParser):
	def parse(self, node: Tag) -> CompanyCardWithPhoto:
		company_card_with_photo_node = node.select_one('div.company-card-with-photo')

		if not company_card_with_photo_node:
			raise ParserError("Company card with photo doesn't exist")

		raw_data = company_card_with_photo_node.get("data-bem")

		if not isinstance(raw_data, str):
			raise ParserError("data-bem attribute doesn't exist")

		unvalidated_data = loads(raw_data)
		card_data = super().parse(node)

		return CompanyCardWithPhoto(**unvalidated_data.get("company-card-with-photo"), **card_data.model_dump())
