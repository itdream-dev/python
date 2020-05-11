from datetime import datetime
import pytz
from lib.registry import get_registry
from lib.models import card
from lib.models import card as card_module
from lib.models.card import Card
from lib.models import user
from lib.models import transfer
import lib.exceptions as exceptions


class AskManager(object):
    def __init__(self):
        registry = get_registry()
        self.deck_repo = registry['DECK_REPO']
        self.ask_repo = registry['ASK_REPO']
        self.user_repo = registry['USER_REPO']
        self.db = registry['DB']

    def add_mode(
        self,
        deck_id,
        is_ask_mode_enabled,
        deck_format,
        asked_user_ids,
        initial_prize=0,
        prize_to_join=0,
        distribution_rule=card.DISTRIBUTION_RULE_SPLIT_PROPORTIONALLY,
        distribution_for=None,
        evaluation_start_dt=None,
        evaluation_end_dt=None,
        tag_names=None
    ):
        card = self.deck_repo.get_card(deck_id)
        # disable ask mode
        if not is_ask_mode_enabled:
            card = self._disable_ask_mode_for_card(card)
            self.db.session.commit()
            return card

        # enable ask mode
        deck = card
        if not card.is_ask_mode_enabled:
            deck = self._enable_ask_mode_for_card(deck, initial_prize)

        # set asked users
        if asked_user_ids is None or asked_user_ids == []:
            asked_user_ids = [user.User.ANYONE_ID]
        asked_users = [self.user_repo.get_user(id) for id in asked_user_ids]

        if deck.is_ask_mode_enabled != is_ask_mode_enabled:
            for asked_user in asked_users:
                asked_user.silver_points = asked_user.silver_points - join_prize
                tr = transfer.Transfer(
                    user_from=asked_user,
                    card_to=deck,
                    silver_points=prize_to_join,
                    transaction_type=transfer.TYPES['create_ask'].code
                )
                self.db.session.add(tr)

        self.ask_repo.asked_repo.set(deck, asked_users)

        self._set_evaluation_period(deck, evaluation_start_dt, evaluation_end_dt)

        deck.format = deck_format
        deck.prize_to_join = prize_to_join
        deck.distribution_for = distribution_for
        deck.distribution_rule = distribution_rule
        deck.silver_points = initial_prize
        deck.original_prize_pool = initial_prize
        self.db.session.commit()
        self.deck_repo.append_tags_to_card(deck, tag_names)
        self.db.session.commit()
        deck = self.deck_repo.get_card(deck.id)
        return deck

    def _set_evaluation_period(self, deck, evaluation_start_dt, evaluation_end_dt):
        deck.evaluation_start_dt = evaluation_start_dt
        deck.evaluation_end_dt = evaluation_end_dt
        if deck.evaluation_start_dt and deck.evaluation_end_dt:
            now_datetime = datetime.now(pytz.utc)
            if now_datetime >= deck.evaluation_start_dt and now_datetime <= deck.evaluation_end_dt:
                deck.evaluation_period_status = card.EVALUATION_PERIOD_STATUS_OPEN

    def _enable_ask_mode_for_card(self, card, initial_prize):
        if card.type != Card.DECK:
            if card.parent_id is not None:
                parent = self.deck_repo.get_card(card.parent_id)
                if parent.is_ask_mode_enabled:
                    raise Exception('You can not enable ask mode on the card, that was already belong to deck with ask_mode')
            owner = card.creator
            deck_container = self.deck_repo.create_deck(owner, card.name, [card.id], False, is_ask_mode_enabled=False, deck_format='')
            deck = self.deck_repo.create_deck(owner, card.name, [deck_container.id], False, is_ask_mode_enabled=True, deck_format='')
        else:
            name = card.name
            owner = card.creator
            deck_container = card
            deck = self.deck_repo.create_deck(owner, name, [deck_container.id], False, is_ask_mode_enabled=True, deck_format='')
        deck.is_ask_mode_enabled = True
        self.ask_repo.asker_repo.remove_all(deck)
        if deck.creator:
            self.ask_repo.asker_repo.add(deck, deck.creator, contribution=initial_prize)
        return deck

    def _disable_ask_mode_for_card(self, card):
        if not card.is_ask_mode_enabled:
            raise ValueError('Card {} is not in ask mode, you can not diable it')
        card.is_ask_mode_enabled = False
        return card

    def _add_submission_to_deck(self, deck, card):
        if len(deck.cards) == 1:
            deck.cards.append(card)
            return

        if len(deck.cards) > 1 and deck.cards[1].type == Card.DECK:
            card.parent = deck.cards[1]
            return

        if len(deck.cards) > 1 and deck.cards[1].type != Card.DECK:
            submission1 = deck.cards[1]
            deck.cards.remove(submission1)
            answer_deck = self.deck_repo.create_deck(card.creator, card.name, [submission1.id, card.id], False, is_ask_mode_enabled=False, deck_format='')
            answer_deck.is_answer = True
            answer_deck.parent = deck
            self.db.session.add(answer_deck)
            return

    def give_card_to_deck(self, deck_id, card_id, viewer_ids=None, answer_visibility=None , tag_names=None):
        deck = self.deck_repo.get_card(deck_id)
        card_module.assert_ask_deck_open(deck)
        card = self.deck_repo.get_card(card_id)

        if len(deck.cards) < 1:
            raise ValueError('Deck has not question deck')

        self._add_submission_to_deck(deck, card)

        if answer_visibility is None:
            answer_visibility = card_module.ANSWER_VISIBILITY_ANYONE
        card.answer_visibility = answer_visibility
        card.is_answer = True
        self.deck_repo.append_tags_to_card(card, tag_names)
        self.db.session.commit()
        deck = self.deck_repo.get_card(deck_id)
        self.db.session.refresh(deck)
        return deck

    def give_card_to_deck_v2(self, deck_id, card_id, submitter,
                             viewer_ids=None, answer_visibility=None,
                             tag_names=None):
        deck = self.deck_repo.get_card(deck_id)
        card_module.assert_ask_deck_open(deck)
        card = self.deck_repo.get_card(card_id)
        card_ids = []
        if card.type == Card.DECK:
            card_ids = [child.id for child in card.cards]
            self.deck_repo.move_out_of_deck_by_id(card_ids)
        else:
            if card.parent_id:
                raise exceptions.AlreadySubmitted()
            card_ids = [card.id]

        if len(deck.cards) < 1:
            raise ValueError('Deck has not question deck')

        submitted_deck = self._find_already_submitted_deck(submitter, deck)
        if submitted_deck:
            self.deck_repo.append_cards_to_deck(
                submitted_deck, card_ids
            )
            return deck

        # user has not submitted previously
        new_submission_containter = self.deck_repo.create_deck(
            submitter, '', card_ids, False, False, '',
            tag_names=tag_names
        )

        if answer_visibility is None:
            answer_visibility = card_module.ANSWER_VISIBILITY_ANYONE
        new_submission_containter.answer_visibility = answer_visibility
        new_submission_containter.is_answer = True

        deck.cards.append(new_submission_containter)
        self.db.session.commit()
        return deck

    def _find_already_submitted_deck(self, user, deck):
        if len(deck.cards) < 2:
            return None
        for submission_deck in deck.cards[1:]:
            if submission_deck.user_id == user.id:
                return submission_deck
        return None

    def revoke_card_from_deck(self, card_id):
        card = self.deck_repo.get_card(card_id)
        if not card.parent_id:
            raise ValueError(
                'The card with id={} does not belong to any deck'.format(
                    card.id
                )
            )
        deck = self.deck_repo.get_card(card.parent_id)
        card_module.assert_ask_deck_open(deck)
        card.parent = None
        self.db.session.commit()
        deck = self.deck_repo.get_card(deck.id)
        return deck

    def revoke_card_from_ask(self, submitter, card_id):
        card = self.deck_repo.get_card(card_id)
        if not card.parent_id:
            raise ValueError(
                'The card with id={} does not belong to any deck'.format(
                    card.id
                )
            )

        if card.type == Card.DECK:
            ask_deck = card.parent
            # return this entire card
            children = [child for child in card.cards]

            # take out children from container
            self.deck_repo.move_out_of_deck(children)

            # wipe out likes and comments
            self.deck_repo.wipe_likes_comments_for_cards(children)

            return ask_deck

        # else we are just removing one card
        user_containter = card.parent
        if not user_containter.parent_id:
            raise ValueError(
                'The card with id={} does not belong to any deck'.format(
                    user_containter.id
                )
            )
        ask_deck = user_containter.parent
        # take out children from container
        self.deck_repo.move_out_of_deck([card])

        # wipe out likes and comments
        self.deck_repo.wipe_likes_comments_for_cards([card])

        return ask_deck

    def join_ask(self, deck_id, user_ids, custom_join_prize=None):
        deck = self.deck_repo.get_card(deck_id)
        if not deck.is_ask_mode_enabled:
            raise ValueError('Deck {} must be in ask mode')

        join_prize = custom_join_prize
        if custom_join_prize is None:
            join_prize = deck.prize_to_join

        if join_prize < deck.prize_to_join:
            raise ValueError('Custom_join_prize {} is less than prize_to_join for deck {}'.format(join_prize, deck.prize_to_join))

        users = [self.user_repo.get_user(id) for id in user_ids]
        for user in users:
            user.silver_points = user.silver_points - join_prize
            tr = transfer.Transfer(
                user_from=user,
                card_to=deck,
                silver_points=join_prize,
                transaction_type=transfer.TYPES['join_ask'].code
            )
            self.db.session.add(tr)
            self.ask_repo.asker_repo.add(deck, user, contribution=join_prize)

        deck.silver_points += join_prize
        self.db.session.commit()
        return deck

    def unjoin_ask(self, deck_id, user_id):
        deck = self.deck_repo.get_card(deck_id)
        if not deck.is_ask_mode_enabled:
            raise ValueError('Deck {} must be in ask mode')

        self.ask_repo.asker_repo.remove(deck, self.user_repo.get_user(user_id))
        self.db.session.commit()
        return deck

    def end_evaluation_period(self, deck_id):
        deck = self.deck_repo.get_card(deck_id)
        card_module.assert_ask_deck_open(deck)

        if deck.distribution_rule == card_module.DISTRIBUTION_RULE_SPLIT_EVENLY:
            silver_points_per_user = deck.silver_points / deck.distribution_for
            for card in list(deck.get_answers())[:deck.distribution_for]:
                card.creator.silver_points += silver_points_per_user
                self.ask_repo.giver_repo.add(
                    deck,
                    user=card.creator,
                    prize=silver_points_per_user,
                    total_likes=len(card.liked_users),
                )
                tr = transfer.Transfer(card_from=deck, user_to=card.creator, silver_points=silver_points_per_user, transaction_type=transfer.TYPES['prize_for_answer'].code)
                self.db.session.add(tr)
        else:
            total = sum([len(card.liked_users) for card in list(deck.get_answers())[:deck.distribution_for]])
            for card in list(deck.get_answers())[:deck.distribution_for]:
                silver_points_per_user = len(card.liked_users) * deck.silver_points / total
                card.creator.silver_points += silver_points_per_user
                self.ask_repo.giver_repo.add(
                    deck,
                    user=card.creator,
                    prize=silver_points_per_user,
                    total_likes=len(card.liked_users),
                )
                tr = transfer.Transfer(card_from=deck, user_to=card.creator, silver_points=silver_points_per_user, transaction_type=transfer.TYPES['prize_for_answer'].code)
                self.db.session.add(tr)

        deck.silver_points = 0
        deck.evaluation_period_status = card_module.EVALUATION_PERIOD_STATUS_DONE
        self.db.session.commit()
        return deck

    def get_winners(self, deck_id):
        deck = self.deck_repo.get_card(deck_id)
        if deck.evaluation_period_status != card_module.EVALUATION_PERIOD_STATUS_DONE:
            raise ValueError('Evaluation period is not done')
        return deck.get_winners()

    def get_sponsors(self, deck_id):
        deck = self.deck_repo.get_card(deck_id)
        return list(self.ask_repo.get_sponsors(deck))
