from typing import Any, Iterable, Tuple


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

			assert isinstance(attr_value, annotation_origin), f"Attribute {attr_name} must be of the {annotation} type"

	def _get_annotations_to_validate(self) -> Iterable[Tuple[str, Any]]:
		return getattr(self, '__annotations__', {}).items()
