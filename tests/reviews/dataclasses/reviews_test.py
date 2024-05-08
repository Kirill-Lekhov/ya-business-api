from ya_business_api.reviews.dataclasses.reviews import (
	Author, InitChatData, OwnerComment, Review, Pager, Reviews, Filters, CurrentState, ReviewsResponse,
)
from ya_business_api.reviews.constants import Ranking

import pytest


def get_author_data() -> dict:
	return {
		"privacy": "privacy",
		"user": "user",
		"uid": 20240503,
		"avatar": "avatar",
	}


def get_init_chat_data() -> dict:
	return {
		"entityId": "entity id",
		"supplierServiceSlug": "supplier service slug",
		"name": "name",
		"description": "description",
		"entityUrl": "entity url",
		"entityImage": "entity image",
		"version": 0,
	}


def get_owner_comment_data() -> dict:
	return {
		"time_created": 1714736208,
		"text": "Thanks for review",
	}


def get_review_data() -> dict:
	return {
		"id": "review id",
		"lang": "ru",
		"author": get_author_data(),
		"time_created": 1714736208,
		"snippet": "snippet",
		"full_text": "full text",
		"rating": 5,
		"cmnt_entity_id": "cmnt entity id",
		"comments_count": 0,
		"cmnt_official_token": "cmnt official token",
		"init_chat_data": get_init_chat_data(),
		"init_chat_token": "init chat token",
		"public_rating": True,
		"business_answer_csrf_token": "business answer csrf token",
		"owner_comment": None,
	}


def get_pager_data() -> dict:
	return {
		"limit": 20,
		"offset": 0,
		"total": 0,
	}


class TestAuthor:
	def test_from_dict(self):
		author = Author.from_dict(get_author_data())

		assert isinstance(author, Author)
		assert author.privacy == "privacy"
		assert author.user == "user"
		assert author.uid == 20240503
		assert author.avatar == "avatar"


class TestInitChatData:
	def test_from_dict(self):
		init_chat_data = InitChatData.from_dict(get_init_chat_data())

		assert isinstance(init_chat_data, InitChatData)
		assert init_chat_data.entityId == "entity id"
		assert init_chat_data.supplierServiceSlug == "supplier service slug"
		assert init_chat_data.name == "name"
		assert init_chat_data.description == "description"
		assert init_chat_data.entityUrl == "entity url"
		assert init_chat_data.entityImage == "entity image"
		assert init_chat_data.version == 0


class TestOwnerComment:
	def test_from_dict(self):
		owner_comment = OwnerComment.from_dict(get_owner_comment_data())

		assert isinstance(owner_comment, OwnerComment)
		assert owner_comment.time_created == 1714736208
		assert owner_comment.text == "Thanks for review"


class TestReview:
	def test_from_dict(self):
		review = Review.from_dict(get_review_data())

		assert isinstance(review, Review)
		assert review.id == "review id"
		assert review.lang == "ru"
		assert isinstance(review.author, Author)
		assert review.time_created == 1714736208
		assert review.snippet == "snippet"
		assert review.full_text == "full text"
		assert review.rating == 5
		assert review.cmnt_entity_id == "cmnt entity id"
		assert review.comments_count == 0
		assert review.cmnt_official_token == "cmnt official token"
		assert isinstance(review.init_chat_data, InitChatData)
		assert review.init_chat_token == "init chat token"
		assert review.public_rating == True
		assert review.business_answer_csrf_token == "business answer csrf token"
		assert review.owner_comment is None

		data = get_review_data()
		data['owner_comment'] = get_owner_comment_data()
		review = Review.from_dict(data)

		assert isinstance(review.owner_comment, OwnerComment)

	def test___repr__(self):
		review = Review.from_dict(get_review_data())
		assert review.__repr__() == "<Review: review id>"


class TestPager:
	def test_from_dict(self):
		pager = Pager.from_dict(get_pager_data())

		assert isinstance(pager, Pager)
		assert pager.limit == 20
		assert pager.offset == 0
		assert pager.total == 0


class TestReviews:
	def test___post_init__(self):
		with pytest.raises(AssertionError, match="Each item of the reviews attr must be of the Review type"):
			Reviews(
				pager=Pager(**get_pager_data()),
				items=["hello"],		# type: ignore - For testing purposes
				csrf_token="CSRF Token",
			)

	def test_from_dict(self):
		reviews = Reviews.from_dict({
			"pager": get_pager_data(),
			"items": [get_review_data(), get_review_data()],
			"csrf_token": "CSRF Token",
		})

		assert isinstance(reviews, Reviews)
		assert isinstance(reviews.pager, Pager)
		assert reviews.csrf_token == "CSRF Token"

		for review in reviews.items:
			assert isinstance(review, Review)


class TestFilters:
	def test___post_init__(self):
		with pytest.raises(AssertionError):
			Filters(ranking="unknown")		# type: ignore - For testing purposes

		with pytest.raises(AssertionError):
			Filters(ranking=Ranking.BY_RATING_ASC, unread=123)		# type: ignore - For testing purposes

	def test_from_dict(self):
		filters = Filters.from_dict({
			"ranking": "by_time",
			"unread": "True",
		})

		assert isinstance(filters, Filters)
		assert filters.ranking is Ranking.BY_TIME
		assert filters.unread

		filters = Filters.from_dict({
			"ranking": "by_rating_desc",
			"unread": "False",
		})
		assert isinstance(filters, Filters)
		assert filters.ranking is Ranking.BY_RATING_DESC
		assert not filters.unread

		with pytest.raises(ValueError):
			Filters.from_dict({"ranking": "UNKNOWN"})


class TestCurrentState:
	def test_from_dict(self):
		current_state = CurrentState.from_dict({
			"filters": {"ranking": "by_time"},
		})

		assert isinstance(current_state, CurrentState)
		assert isinstance(current_state.filters, Filters)


class TestReviewsResponse:
	def test_from_dict(self):
		reviews_response = ReviewsResponse.from_dict({
			"page": 1,
			"currentState": {
				"filters": {"ranking": "by_time"},
			},
			"list": {
				"pager": get_pager_data(),
				"items": [],
				"csrf_token": "CSRF Token",
			},
		})

		assert isinstance(reviews_response, ReviewsResponse)
		assert reviews_response.page == 1
		assert isinstance(reviews_response.currentState, CurrentState)
		assert isinstance(reviews_response.list, Reviews)
