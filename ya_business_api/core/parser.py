from abc import ABC, abstractmethod
from typing import Collection, Union

from pydantic.main import BaseModel
from bs4.element import Tag


class BaseParser(ABC):
	@abstractmethod
	def parse(self, node_or_content: Union[Tag, str]) -> Union[Collection[BaseModel], BaseModel]: ...
