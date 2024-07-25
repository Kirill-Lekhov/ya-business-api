from ya_business_api.reviews.dataclasses.reviews import (
	Author, InitChatData, OwnerComment, Review, Pager, Reviews, Filters, CurrentState, ReviewsResponse, Photo,
)
from ya_business_api.reviews.constants import Ranking

import pytest
from pydantic import ValidationError


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


def get_photo() -> dict:
	return {
		"link": "/get-altay/00000000/2a0000018b7b20d860e00002d00a0000a000/orig",
		"width": 1920,
		"height": 1080,
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
	def test_validation(self):
		author = Author(**get_author_data())

		assert isinstance(author, Author)
		assert author.privacy == "privacy"
		assert author.user == "user"
		assert author.uid == 20240503
		assert author.avatar == "avatar"


class TestInitChatData:
	def test_validation(self):
		init_chat_data = InitChatData(**get_init_chat_data())

		assert isinstance(init_chat_data, InitChatData)
		assert init_chat_data.entity_id == "entity id"
		assert init_chat_data.supplier_service_slug == "supplier service slug"
		assert init_chat_data.name == "name"
		assert init_chat_data.description == "description"
		assert init_chat_data.entity_url == "entity url"
		assert init_chat_data.entity_image == "entity image"
		assert init_chat_data.version == 0


class TestOwnerComment:
	def test_validation(self):
		owner_comment = OwnerComment(**get_owner_comment_data())

		assert isinstance(owner_comment, OwnerComment)
		assert owner_comment.time_created == 1714736208
		assert owner_comment.text == "Thanks for review"


class TestPhoto:
	def test_validation(self):
		photo = Photo(**get_photo())

		assert photo.link == "/get-altay/00000000/2a0000018b7b20d860e00002d00a0000a000/orig"
		assert photo.width == 1920
		assert photo.height == 1080


class TestReview:
	def test_validation(self):
		review = Review(**get_review_data())

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
		assert review.photos == []

		data = get_review_data()
		data['owner_comment'] = get_owner_comment_data()
		review = Review(**data)

		assert isinstance(review.owner_comment, OwnerComment)

	def test_validation__extended(self):
		review_data = get_review_data()
		review_data["photos"] = [get_photo(), get_photo(), get_photo()]
		review = Review(**review_data)

		assert len(review.photos) == 3


class TestPager:
	def test_validation(self):
		pager = Pager(**get_pager_data())

		assert isinstance(pager, Pager)
		assert pager.limit == 20
		assert pager.offset == 0
		assert pager.total == 0


class TestReviews:
	def test_validation(self):
		reviews = Reviews(**{
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
	def test_validation(self):
		filters = Filters(ranking="by_time", unread="True")

		assert isinstance(filters, Filters)
		assert filters.ranking is Ranking.BY_TIME
		assert filters.unread == "True"

		filters = Filters(ranking="by_rating_desc", unread="False")

		assert isinstance(filters, Filters)
		assert filters.ranking is Ranking.BY_RATING_DESC
		assert filters.unread == "False"

		with pytest.raises(ValidationError):
			Filters(ranking="UNKNOWN")


class TestCurrentState:
	def test_validation(self):
		current_state = CurrentState(filters=Filters(ranking="by_time"))

		assert isinstance(current_state, CurrentState)
		assert isinstance(current_state.filters, Filters)


class TestReviewsResponse:
	def test_validation(self):
		reviews_response = ReviewsResponse(
			page=1,
			currentState=CurrentState(
				filters=Filters(ranking="by_time"),
			),
			list={
				"pager": get_pager_data(),
				"items": [],
				"csrf_token": "CSRF Token",
			},
		)

		assert isinstance(reviews_response, ReviewsResponse)
		assert reviews_response.page == 1
		assert isinstance(reviews_response.current_state, CurrentState)
		assert isinstance(reviews_response.list, Reviews)
