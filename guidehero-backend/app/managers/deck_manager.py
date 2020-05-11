# -*- coding: utf-8 -*-
import arrow
from lib.registry import get_registry
from lib.upload_helper import UploadHelper
from lib.bing_image_search import BingImageSearch
from lib.models.card import Card
from lib.models.card_comments import CardComments
from lib.models.comment_like import CommentLike


class DeckManager(object):

    JP = 'ja-JP'
    EN = 'en-US'

    def __init__(self):
        registry = get_registry()
        self.deck_repo = registry['DECK_REPO']
        self.db = registry['DB']
        self.upload_helper = UploadHelper()
        self.notification_repo = registry['NOTIFICATION_REPO']
        self.user_repo = registry['USER_REPO']

    def get_decks(self):
        root_folders = self.deck_repo.get_root_folders()
        return [
            folder.to_dict() for folder in root_folders
        ]

    def get_card(self, card_id):
        return self.deck_repo.get_card(card_id)

    def get_public_decks(self):
        return self.deck_repo.get_published_decks()

    def get_my_published_decks(self, user):
        return sorted(
            self.deck_repo.get_my_published_decks(user),
            key=lambda x: -x.created_at
        )

    def create_text_card(self, user, card_title, card_content,
                         pronunciation_language, description, tag_names=None):
        self.deck_repo.create_text_card(
            user, card_title, card_content, pronunciation_language,
            description, tag_names=tag_names
        )

    def create_image_card(self, user, card_title, s3_file_name, description,
                          image_x, image_y, image_width, image_height,
                          tag_names=None, image_scale=None):
        image_path = '%s/%s' % (
            self.upload_helper.s3_image_cloudfront, s3_file_name
        )
        return self.deck_repo.create_image_card(
            user, card_title, image_path, description,
            image_x, image_y, image_width, image_height,
            tag_names=tag_names, image_scale=image_scale
        )

    def edit_image_card(self, user, card_id, s3_file_name=None,
                        tag_names=None, **data):
        data['content'] = '%s/%s' % (
            self.upload_helper.s3_image_cloudfront, s3_file_name
        )
        card = self.deck_repo.get_card(card_id)
        for key, value in data.items():
            setattr(card, key, value)
        self.deck_repo.append_tags_to_card(card, tag_names)
        self.db.session.commit()
        return card

    def edit_video_card(self, user=None, card_id=None, s3_file_name=None,
                        thumbnail_url=None, tag_names=None, video_length=None,
                        **data):
        card = self.deck_repo.get_card(card_id)
        data['content'] = '%s/%s' % (
            self.upload_helper.s3_video_cloudfront, s3_file_name
        )
        data['sub_content'] = '%s/%s' % (
            self.upload_helper.s3_video_cloudfront, thumbnail_url
        )
        data['video_length'] = video_length

        for key, value in data.items():
            setattr(card, key, value)
        self.deck_repo.append_tags_to_card(card, tag_names)
        self.db.session.commit()
        return card

    def create_video_card(self, user, card_title, s3_file_name, thumbnail_url,
                          description, tag_names=None, scale=None,
                          video_length=None):
        video_path = '%s/%s' % (
            self.upload_helper.s3_video_cloudfront, s3_file_name
        )
        thumb_path = '%s/%s' % (
            self.upload_helper.s3_image_cloudfront, thumbnail_url
        )
        return self.deck_repo.create_video_card(
            user, card_title, video_path, thumb_path, description,
            tag_names=tag_names,
            scale=scale,
            video_length=video_length
        )

    def generate_image_upload_params(self, file_name):
        return self.upload_helper.generate_image_upload_params(file_name)

    def generate_video_upload_params(self, file_name):
        return self.upload_helper.generate_video_upload_params(file_name)

    def create_deck(self, user, deck_title, card_ids, public,
                    is_ask_mode_enabled, deck_format, tag_names=None):
        self.deck_repo.create_deck(
            user,
            deck_title,
            card_ids,
            public,
            is_ask_mode_enabled=is_ask_mode_enabled,
            deck_format=deck_format,
            tag_names=tag_names
        )

    def get_image_search_urls(self, key):
        return BingImageSearch().get_image_urls(key)

    def delete_cards(self, user, card_ids):
        cards = self.deck_repo.get_my_cards(user, card_ids)
        self.deck_repo.delete_cards(cards)

    def copy_cards(self, user, card_ids):
        cards = self.deck_repo.get_cards(card_ids)
        self.deck_repo.copy_cards(user, cards)

    def copy_card(self, user, card_id):
        card = self.deck_repo.get_card(card_id)
        if card.creator.id != user.id:
            raise ValueError('User does not have permission to move card')
        new_card = self.deck_repo.copy_card(user, card)
        self.db.session.commit()
        return new_card

    def publish_decks(self, user, card_ids, publish):
        decks = self.deck_repo.get_decks(user, card_ids)
        self.deck_repo.publish_decks(decks, publish)

    def edit_deck(self, user, deck_id, card_ids, tag_names=None):
        deck = self.deck_repo.get_my_card(user, deck_id)
        if not deck:
            return
        cards = []
        for card_id in card_ids:
            card = self.deck_repo.get_my_card(user, card_id)
            if card:
                cards.append(card)
        self.deck_repo.edit_deck(cards, deck=deck, tag_names=tag_names)

    def get_cards_for_drafts(self, user):
        cards = [
            card for card in user.cards
            if card.parent is None and card.published is False
        ]
        return sorted(
            cards,
            key=lambda x: ((0 if x.position is None else x.position), (
                -1000000000 if x.created_at is None else -x.created_at)
            )
        )

    def like_card(self, user, card_id):
        user, card = self.deck_repo.like_card(user, card_id)
        self.notification_repo.create_like_notification(user, card)

    def like_comment(self, user, comment_id):
        comment = CardComments.query.get(comment_id)
        it = CommentLike(user=user, comment=comment)
        self.db.session.add(it)
        self.db.session.commit()
        return it

    def unlike_comment(self, user, comment_id):
        comment = CardComments.query.get(comment_id)
        it = CommentLike.query.filter(
            CommentLike.user == user,
            CommentLike.comment == comment
        ).first()
        self.db.session.delete(it)
        self.db.session.commit()

    def unlike_card(self, user, card_id):
        self.deck_repo.unlike_card(user, card_id)

    def view_card(self, user, card_id):
        card = self.deck_repo.get_card(card_id)
        card.views.append(user)
        self.db.session.commit()

    def move_card(self, user, card_id, move_to):
        cards = self.deck_repo.get_my_cards(user, card_id).all()
        if len(cards) < 1:
            raise ValueError(
                'No cards found for current user for ids: {}'.format(card_id)
            )

        if not move_to:
            self.deck_repo.move_out_of_deck(cards)
            return

        move_to_deck = self.deck_repo.get_my_card(user, move_to)
        if move_to and not move_to_deck:
            raise ValueError(
                'No cards found current user for ids: {}'.format(card_id)
            )

        if move_to_deck.type == Card.DECK:
            self.deck_repo.move_cards(cards, move_to_deck)
            return

        # if move_to_deck is not DECK
        card_ids = [move_to_deck.id] + [c.id for c in cards]
        self.deck_repo.create_deck(
            user=user,
            name='',
            card_ids=card_ids,
            public=move_to_deck.published,
            is_ask_mode_enabled=False,
            deck_format=None
        )

    def convert_card_to_deck(self, user, card_id):
        card = self.deck_repo.get_card(card_id)
        if card.creator.id != user.id:
            raise ValueError('card does not belong to current user')
        if card.type == Card.DECK:
            raise ValueError('Card is deck and can not be converted to deck')

        deck = self.deck_repo.create_deck(
            user=user,
            name=card.name,
            card_ids=[card_id],
            public=card.published,
            is_ask_mode_enabled=False,
            deck_format=None
        )
        deck.description = card.description

        for tag in card.tags:
            deck.tags.append(tag)
        self.db.session.commit()
        return deck

    def add_comment(self, user, content, card_id=None, comment_id=None):

        if card_id is None and comment_id is None:
            raise ValueError('card_id or comment_id should be defined')
        if card_id is not None and comment_id is not None:
            raise ValueError('Only card_id or comment_id should be defined')

        card = (
            self.deck_repo.get_card(card_id) if card_id is not None else None
        )
        comment = (
            CardComments.query.get(comment_id)
            if comment_id is not None else None
        )

        now = arrow.utcnow().timestamp
        item = CardComments(
            user=user,
            content=content,
            card=card,
            comment=comment,
            created_at=now,
            updated_at=now
        )
        self.db.session.add(item)
        self.db.session.commit()
        if card is not None:
            self.notification_repo.create_comment_notification(
                user, card, content
            )
            self.create_mention_notifications(user, card, content)
        return item

    def create_mention_notifications(self, created_user, card, content):
        words = content.split()
        for word in words:
            if word[0] != '@':
                continue
            username = word[1:]
            target_user = self.user_repo.get_user_from_username(username)
            if not target_user:
                continue
            self.notification_repo.create_mention_notification(
                target_user, created_user, card, content
            )

    def search_cards(self, keywords=None):
        return self.deck_repo.search_cards(keywords=keywords)

    def change_order(self, user, card_id, position):
        card = self.deck_repo.get_card(card_id)

        if card is None:
            raise ValueError('No card found for id {}'.format(card_id))

        if card.published is False and card.parent is None:
            return self.change_order_for_draft(user, card, position)

        deck = card.parent
        if deck is None:
            raise ValueError(
                'The card does not belong to any deck and has no position'
            )

        if deck.published:
            raise ValueError(
                'Card deck is published. you can not change order'
            )

        if deck.creator.id != user.id:
            raise ValueError(
                'Deck with id {}, does not belong to user {}'.format(
                    deck.id, user.id
                )
            )

        deck.cards.remove(card)
        deck.cards.reorder()
        deck.cards.insert(position, card)
        self.db.session.commit()

    def change_order_for_draft(self, user, card, position):
        drafts = list(self.get_cards_for_drafts(user))
        drafts.remove(card)
        drafts.insert(position, card)
        for idx, it in enumerate(drafts):
            it.position = idx
        self.db.session.commit()
