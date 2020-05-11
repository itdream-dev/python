# -*- coding: utf-8 -*-
import arrow
from lib.registry import get_registry
from lib.models.base_folder import BaseFolder
from lib.models.base_deck import BaseDeck
from lib.models.base_set import BaseSet
from lib.models.base_card import BaseCard
from lib.models.base_card_content import BaseCardContent
from lib.models.card import Card
from lib.models.card_likes import CardLikes
from lib.models.card_comments import CardComments
from lib.models.tag import Tag
from sqlalchemy.exc import IntegrityError
from lib.models.notification import Notification


class DeckRepo(object):

    def __init__(self):
        self.db = get_registry()['DB']

    def add_folder(self, name, creator, image, root_level=False):
        folder = BaseFolder(
            name=name,
            creator=creator,
            image=image,
            root_level=root_level
        )
        self.db.session.add(folder)
        self.db.session.commit()
        return folder

    def add_deck(self, name, creator, image):
        deck = BaseDeck(
            name=name,
            creator=creator,
            image=image
        )
        self.db.session.add(deck)
        self.db.session.commit()
        return deck

    def add_set(self, name, creator):
        base_set = BaseSet(name=name, creator=creator)
        self.db.session.add(base_set)
        self.db.session.commit()
        return base_set

    def add_card(self, name, user_id=None):
        card = BaseCard(name=name, user_id=user_id)
        self.db.session.add(card)
        self.db.session.commit()
        return card

    def add_card_content(self, content_type, content, language):
        card_content = BaseCardContent(
            type=content_type,
            content=content,
            language=language
        )
        self.db.session.add(card_content)
        self.db.session.commit()
        return card_content

    def truncate_tables(self):
        BaseCardContent.query.delete()
        BaseCard.query.delete()
        BaseSet.query.delete()
        BaseDeck.query.delete()
        BaseFolder.query.delete()

    def get_root_folders(self):
        return BaseFolder.query.filter(BaseFolder.root_level).all()

    # V2 starts here
    def create_text_card(self, user, name, content, pronunciation_language,
                         description, tag_names=None):
        now = arrow.utcnow().timestamp
        card = Card(
            type=Card.TEXT,
            name=name,
            content=content,
            language=pronunciation_language,
            pronunciation=bool(pronunciation_language),
            created_at=now,
            updated_at=now,
            description=description
        )
        user.cards.append(card)
        self.append_tags_to_card(card, tag_names=tag_names)
        self.db.session.commit()

    def create_image_card(self, user, name, content, description,
                          image_x, image_y, image_width, image_height, tag_names=None,
                          image_scale=None):
        now = arrow.utcnow().timestamp
        card = Card(
            type=Card.IMAGE,
            name=name,
            content=content,
            created_at=now,
            updated_at=now,
            description=description,
            x_position=image_x,
            y_position=image_y,
            width=image_width,
            height=image_height,
            scale=image_scale,
        )
        user.cards.append(card)
        self.append_tags_to_card(card, tag_names=tag_names)
        self.db.session.commit()
        return card

    def create_video_card(self, user, name, content, sub_content, description,
                          tag_names=None, scale=None, video_length=None):
        now = arrow.utcnow().timestamp
        card = Card(
            type=Card.VIDEO,
            name=name,
            content=content,
            sub_content=sub_content,
            created_at=now,
            updated_at=now,
            description=description,
            scale=scale,
            video_length=video_length,
        )
        user.cards.append(card)
        self.append_tags_to_card(card, tag_names=tag_names)
        self.db.session.commit()
        return card

    def get_card(self, card_id):
        return Card.query.filter(Card.id == card_id).first()

    def get_card_like(self, user_id, card_id):
        return CardLikes.query.filter(
            CardLikes.user_id == user_id,
            CardLikes.card_id == card_id
        ).first()

    def get_cards_liked_by_user(self, user):
        return Card.query.join(CardLikes, Card.id == CardLikes.card_id).filter(CardLikes.user == user).all()

    def get_my_card(self, user, card_id):
        return Card.query.filter(
            Card.id == card_id,
            Card.user_id == user.id
        ).first()

    def get_cards(self, card_ids):
        return Card.query.filter(
            Card.id.in_(card_ids)
        ).all()

    def get_my_cards(self, user, card_ids):
        return Card.query.filter(
            Card.id.in_(card_ids),
            Card.user_id == user.id
        )

    def get_decks(self, user, card_ids):
        return Card.query.filter(
            Card.id.in_(card_ids),
            Card.user_id == user.id,
            Card.type == Card.DECK
        ).all()

    def get_published_decks(self):
        return Card.query.filter(
            Card.type == Card.DECK,
            Card.published == True
        ).order_by(Card.created_at.desc()).all()

    def get_my_published_decks(self, user):
        return Card.query.filter(
            Card.type == Card.DECK,
            Card.published == True,
            Card.user_id == user.id
        ).all()

    def get_my_published_cards(self, user):
        return Card.query.filter(
            Card.published == True,
            Card.user_id == user.id
        ).all()

    def delete_cards(self, cards):
        for card in cards:
            self.delete_card(card)

    def delete_card(self, card):
        if card.type == Card.DECK:
            for child in card.cards:
                self.delete_card(child)
        for likes in card.liked_users:
            self.db.session.delete(likes)
        for card_comment in card.comments:
            self.db.session.delete(card_comment)
        notifications = Notification.query.filter(
            Notification.card_id == card.id
        ).all()
        for notif in notifications:
            self.db.session.delete(notif)
        self.db.session.commit()
        self.db.session.delete(card)
        self.db.session.commit()

    def _get_duplicate(self, user, card, now):
        return Card(
            type=card.type,
            name=card.name,
            content=card.content,
            language=card.language,
            pronunciation=card.pronunciation,
            created_at=now,
            updated_at=now,
            description=card.description,
            x_position=card.x_position,
            y_position=card.y_position,
            width=card.width,
            height=card.height
        )

    def copy_cards(self, user, cards):
        now = arrow.utcnow().timestamp
        for card in cards:
            if card.type == Card.DECK:
                new_deck = Card(
                    type=Card.DECK,
                    name=card.name,
                    created_at=now,
                    updated_at=now
                )
                for child in card.cards:
                    new_card = self._get_duplicate(user, child, now)
                    user.cards.append(new_card)
                    new_deck.cards.append(new_card)
                user.cards.append(new_deck)
            else:
                new_card = self._get_duplicate(user, card, now)
                user.cards.append(new_card)
        self.db.session.commit()

    def _clone_card(self, user, card, now):
        fields_to_copy = [
            'type',
            'name',
            'content',
            'sub_content',
            'language',
            'pronunciation',
            'published',
            'description',
            'creator',
            'x_position',
            'y_position',
            'height',
            'width',
            'scale',
            'silver_points',
            'original_prize_pool',
            'gold_points',
            'prize_to_join',
            'answer_visibility',
            'liked_users',
            'comments',
            'is_ask_mode_enabled',
            'format',
            'distribution_rule',
            'distribution_for',
            'evaluation_start_dt',
            'evaluation_end_dt',
            'evaluation_period_status',
            'is_answer',
            'tags',
            'video_length',
        ]
        kwargs = {name: getattr(card, name) for name in fields_to_copy}
        return Card(**kwargs)

    def copy_card(self, user, card, now=None):
        if now is None:
            now = arrow.utcnow().timestamp
        new_card = self._clone_card(user, card, now)
        self.db.session.add(new_card)
        for child in card.cards:
            new_card.cards.append(self.copy_card(user, child, now))
        return new_card

    def publish_decks(self, decks, publish):
        for deck in decks:
            deck.published = publish
            self.db.session.merge(deck)
        self.db.session.commit()

    def append_tags_to_card(self, card, tag_names=None):
        tags = []
        if tag_names is not None:
            tags = [self.get_or_create_tag(name) for name in tag_names]
        for tag in tags:
            card.tags.append(tag)

    def create_deck(self, user, name, card_ids, public, is_ask_mode_enabled, deck_format, tag_names=None):
        now = arrow.utcnow().timestamp
        deck = Card(
            type=Card.DECK,
            name=name,
            created_at=now,
            updated_at=now,
            is_ask_mode_enabled=is_ask_mode_enabled,
            format=deck_format,
        )
        for card_id in card_ids:
            card = self.get_card(card_id)
            if not card:
                continue
            deck.cards.append(card)
        user.cards.append(deck)
        self.append_tags_to_card(deck, tag_names=tag_names)

        self.db.session.commit()
        return deck

    def append_cards_to_deck(self, deck, card_ids):
        for card_id in card_ids:
            card = self.get_card(card_id)
            if not card:
                continue
            deck.cards.append(card)
        self.db.session.merge(card)
        self.db.session.commit()
        return deck

    def edit_deck(self, cards, deck=None, tag_names=None):
        for i, card in enumerate(cards):
            card.position = i
            self.db.session.merge(card)

        self.append_tags_to_card(deck, tag_names=tag_names)
        self.db.session.commit()

    def like_card(self, user, card_id):
        card = self.get_card(card_id)
        if not card:
            return

        card_likes = CardLikes()
        card_likes.card = card
        card_likes.user = user

        try:
            user.liked_cards.append(card_likes)
            self.db.session.commit()
            return user, card
        except IntegrityError:
            pass

    def unlike_card(self, user, card_id):
        card_like = self.get_card_like(user.id, card_id)
        if not card_like:
            return

        self.db.session.delete(card_like)
        self.db.session.commit()

    def move_out_of_deck_by_id(self, card_ids):
        cards = self.get_cards(card_ids)
        self.move_out_of_deck(cards)

    def move_out_of_deck(self, cards):
        for card in cards:
            parent = card.parent
            if not parent:
                continue
            parent.cards.remove(card)
            card.position = None

            if not len(parent.cards):
                self.delete_card(parent)

        self.db.session.commit()

    def get_nested_deck_ids(self, deck):
        if deck.type != Card.DECK:
            return []
        ids = [deck.id]
        child_decks = [
            child for child in deck.cards if child.type == Card.DECK
        ]
        for child in child_decks:
            ids.extend(self.get_nested_deck_ids(child))
        return ids

    def move_cards(self, cards, move_to_deck):
        # prevent loop within decks
        nested_ids = []
        for card in cards:
            nested_ids.extend(self.get_nested_deck_ids(card))
        if move_to_deck.id in nested_ids:
            return

        for card in cards:
            if card.parent:
                card.parent.cards.remove(card)
            move_to_deck.cards.append(card)
        self.db.session.commit()

    def add_comment(self, user, content, card_id=None, comment_id=None):
        card = self.get_card(card_id)

        if not card:
            return None, None, None

        if len(content) > 10000:
            return None, None, None

        now = arrow.utcnow().timestamp
        card_comments = CardComments()
        card_comments.card = card
        card_comments.user = user
        card_comments.content = content
        card_comments.created_at = now
        card_comments.updated_at = now
        self.db.session.add(card_comments)

    def update_deck(self, deck_id, is_ask_mode_enabled=None, deck_format=None):
        deck = self.get_card(deck_id)
        if is_ask_mode_enabled is not None:
            deck.is_ask_mode_enabled = is_ask_mode_enabled

        if deck_format is not None:
            deck.format = deck_format

    def search_cards(self, keywords=None):
        from sqlalchemy import or_

        q = Card.query.filter(
            Card.published == True
        )
        if keywords is not None:
            for keyword in keywords:
                search_str = '%{}%'.format(keyword)
                q = q.filter(
                    or_(
                        Card.name.like(search_str),
                        Card.description.like(search_str),
                        Card.content.like(search_str),
                    )
                )
        return q.all()

    def get_or_create_tag(self, name):
        name = name.lower()
        with self.db.session.no_autoflush:
            tag = Tag.query.filter(Tag.name == name).first()

        if not tag:
            tag = Tag(name=name)
            self.db.session.add(tag)
        return tag

    def wipe_likes_comments_for_cards(self, cards):
        for card in cards:
            self.wipe_likes_comments(card)

    def wipe_likes_comments(self, card):
        for liked_user in card.liked_users:
            self.db.session.delete(liked_user)
        for card_comment in card.comments:
            self.db.session.delete(card_comment)
        card.liked_users = []
        card.comments = []
        self.db.session.commit()
