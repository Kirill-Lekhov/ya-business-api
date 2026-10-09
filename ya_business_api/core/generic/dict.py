from typing import Any, Union, Dict, Iterable, Hashable


Node = Dict[Hashable, Union["Node", Any]]


class MissingNode:
	pass


def get_from_deep(node: Node, keychain: Iterable[Hashable]) -> Any:
	"""
	Returns value from nested dicts by chain of keys.

	Examples:
		>>> graph = {"A": {"B": {"C": "Hi!"}}}
		>>> get_from_deep(graph, ["A", "B", "C"])
		"Hi!"
	"""
	remaining_keys = [*keychain]

	while remaining_keys:
		if not isinstance(node, dict):
			raise TypeError("Node is not a dictionary")

		key = remaining_keys.pop(0)
		next_node = node.get(key, MissingNode)

		if next_node is MissingNode:
			raise ValueError(f"Key \"{key}\" is missing")

		node = next_node

	return node
