from typing import Any, Iterable, Tuple, Union, get_args, TypeVar, Type


_DMixin = TypeVar('_DMixin', bound='DictMixin')


class ValidatedMixin:
	"""
	Provides data validation methods for dataclasses.

	Notes:
		* The basic implementation of the method does not provide validation of complex data.
	"""
	def __post_init__(self) -> None:
		self._validate_attrs()

	def _validate_attrs(self) -> None:
		for attr_name, annotation in self._get_annotations_to_validate():
			attr_value = getattr(self, attr_name)
			annotation_origin = getattr(annotation, '__origin__', annotation)
			error_msg = f"Attribute {attr_name} must be of the {annotation} type"

			if annotation_origin is Union:
				assert any(map(lambda t: isinstance(attr_value, t), get_args(annotation))), error_msg
			else:
				assert isinstance(attr_value, annotation_origin), error_msg

	def _get_annotations_to_validate(self) -> Iterable[Tuple[str, Any]]:
		return getattr(self, '__annotations__', {}).items()


class DictMixin:
	"""
	Implements methods of dataclass working with dictionaries.
	"""
	@classmethod
	def from_dict(cls: Type[_DMixin], d: dict) -> _DMixin:
		return cls(**d)
