from ya_business_api.core.parser import BaseParser
from ya_business_api.core.exceptions import ParserError
from ya_business_api.companies.dataclasses.chain_list import ChainBranchesList

from json import loads

from bs4.element import Tag


class ChainBranchesListParser(BaseParser):
	def parse(self, node: Tag) -> ChainBranchesList:
		raw_data = node.get("data-bem")

		if isinstance(raw_data, str):
			unvalidated_data = loads(raw_data)
			return ChainBranchesList(**unvalidated_data.get("chain-branches__list", {}))

		raise ParserError("data-bem attribute doesn't exist")
