from ya_business_api.core.dataclasses import ValidatedMixin
from ya_business_api.reviews.constants import Ranking

from typing import TypeVar, List, Optional
from dataclasses import dataclass


T = TypeVar('T')


@dataclass
class Author(ValidatedMixin):
	__slots__ = 'privacy', 'user', 'uid', 'avatar'

	privacy: str
	user: str
	uid: int
	avatar: str

	@classmethod
	def from_dict(cls, d: dict) -> "Author":
		return cls(**d)


@dataclass
class InitChatData(ValidatedMixin):
	__slots__ = 'entityId', 'supplierServiceSlug', 'name', 'description', 'entityUrl', 'entityImage', 'version'

	entityId: str
	supplierServiceSlug: str
	name: str
	description: str
	entityUrl: str
	entityImage: str
	version: int

	@classmethod
	def from_dict(cls, d: dict) -> "InitChatData":
		return cls(**d)


@dataclass
class OwnerComment(ValidatedMixin):
	time_created: int
	text: str

	@classmethod
	def from_dict(cls, d: dict) -> "OwnerComment":
		return cls(**d)


@dataclass
class Review(ValidatedMixin):
	__slots__ = (
		'id', 'lang', 'author', 'time_created', 'snippet', 'full_text', 'rating', 'cmnt_entity_id',
		'comments_count', 'cmnt_official_token', 'init_chat_data', 'init_chat_token', 'public_rating',
		'business_answer_csrf_token', 'owner_comment'
	)

	id: str
	lang: str
	author: Author
	time_created: int
	snippet: str
	full_text: str
	rating: int
	cmnt_entity_id: str
	comments_count: int
	cmnt_official_token: str
	init_chat_data: InitChatData
	init_chat_token: str
	public_rating: bool
	business_answer_csrf_token: str
	owner_comment: Optional[OwnerComment]

	@classmethod
	def from_dict(cls, d: dict) -> "Review":
		d['author'] = Author.from_dict(d.get('author', {}))
		d['init_chat_data'] = InitChatData.from_dict(d.get('init_chat_data', {}))

		if raw_owner_comment := d.get('owner_comment'):
			d['owner_comment'] = OwnerComment.from_dict(raw_owner_comment)
		else:
			d['owner_comment'] = None

		return cls(**d)

	def _validate_attrs(self) -> None:
		super()._validate_attrs()
		assert (
			self.owner_comment is None or isinstance(self.owner_comment, OwnerComment)
		), "The owner comment must be None or OwnerComment instance"

	def _get_annotations_to_validate(self):
		attrs_to_skip = {'owner_comment'}

		for i in self.__annotations__.items():
			if i[0] not in attrs_to_skip:
				yield i

	def __repr__(self) -> str:
		return f"<{self.__class__.__qualname__}: {self.id}>"


@dataclass
class Pager(ValidatedMixin):
	limit: int
	offset: int
	total: int

	@classmethod
	def from_dict(cls, d: dict) -> "Pager":
		return cls(**d)


@dataclass
class Reviews(ValidatedMixin):
	pager: Pager
	items: List[Review]
	csrf_token: str

	def __post_init__(self) -> None:
		super().__post_init__()

		for item in self.items:
			assert isinstance(item, Review), "Each item of the reviews attr must be of the Review type"

	@classmethod
	def from_dict(cls, d: dict) -> "Reviews":
		d['pager'] = Pager.from_dict(d.get('pager', {}))
		d['items'] = [Review.from_dict(i) for i in d.get('items', [])]
		return cls(**d)


@dataclass
class Filters(ValidatedMixin):
	ranking: Ranking
	unread: Optional[bool] = None

	def __post_init__(self) -> None:
		assert isinstance(self.ranking, Ranking)
		assert self.unread is None or isinstance(self.unread, bool)

	@classmethod
	def from_dict(cls, d: dict) -> "Filters":
		d['unread'] = True if d.get('unread') == 'True' else False
		d['ranking'] = Ranking(d.get('ranking'))
		return cls(**d)


@dataclass
class CurrentState(ValidatedMixin):
	filters: Filters

	@classmethod
	def from_dict(cls, d: dict) -> "CurrentState":
		d['filters'] = Filters.from_dict(d.get('filters', {}))

		return cls(**d)


@dataclass
class ReviewsResponse(ValidatedMixin):
	page: int
	currentState: CurrentState
	list: Reviews

	@classmethod
	def from_dict(cls, d: dict) -> "ReviewsResponse":
		d['currentState'] = CurrentState.from_dict(d.get('currentState', {}))
		d['list'] = Reviews.from_dict(d.get('list', {}))

		return cls(**d)
