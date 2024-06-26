from ya_business_api.reviews.constants import Ranking

from typing import List, Optional

from pydantic import BaseModel


class Author(BaseModel):
	privacy: str
	user: str
	uid: int
	avatar: str


class InitChatData(BaseModel):
	entityId: str
	supplierServiceSlug: str
	name: str
	description: str
	entityUrl: str
	entityImage: str
	version: int


class OwnerComment(BaseModel):
	time_created: int
	text: str


class Review(BaseModel):
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

	# Optional fields
	owner_comment: Optional[OwnerComment] = None


class Pager(BaseModel):
	limit: int
	offset: int
	total: int


class Reviews(BaseModel):
	pager: Pager
	items: List[Review]
	csrf_token: str


class Filters(BaseModel):
	ranking: Ranking

	# Optional fields
	unread: Optional[str] = None


class CurrentState(BaseModel):
	filters: Filters


class ReviewsResponse(BaseModel):
	page: int
	currentState: CurrentState
	list: Reviews
