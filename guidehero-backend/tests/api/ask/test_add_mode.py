from ..base import ApiBaseTestCase
import flask
from datetime import datetime
from pytz import timezone
import pytz
import mock

from lib.models.card import Card
from lib.models import card
from lib.models.user import User
from lib.models.user_role_card import UserRoleCard
from lib.models.card_role import CardRole
from app.app_json_coder import encode_datetime
from tests.helpers import factories


class DeskAddModeTestCase(ApiBaseTestCase):
    def setUp(self):
        super(DeskAddModeTestCase, self).setUp()

        # input data
        self.owner = None
        self.card = None
        self.card_type = Card.DECK
        self.card_name = 'test_card1'
        self.asked_users = None
        self.asked_user1 = None
        self.initial_prize = None
        self.prize_to_join = None
        self.evaluation_start_dt = None
        self.evaluation_end_dt = None
        self.distribution_rule = card.DISTRIBUTION_RULE_SPLIT_PROPORTIONALLY
        self.distribution_for = None
        self.questions = None

        # output data
        self.output_card = None
        self.permissions = None
        self.response_status = '200 OK'
        self.response = None
        self.output_asked_users = None
        self.output_join_users = None
        self.output_silver_points = 0
        self.output_prize_to_join = 0

    def create_input_data(self):
        if self.owner is None:
            self.owner = User(username='owner')
            self.db.session.add(self.owner)

        if self.card is None:
            self.card = Card(type=self.card_type, name=self.card_name, creator=self.owner)
            self.db.session.add(self.card)
        self.db.session.commit()

        if self.questions is not None:
            for idx, c in enumerate(self.questions):
                c.position = idx
                self.card.cards.append(c)
            self.db.session.commit()

        if self.asked_users is None:
            if self.asked_user1 is None:
                self.asked_user1 = User(username='asked_user1')
                self.db.session.add(self.asked_user1)
                self.db.session.commit()
            self.asked_users = [self.asked_user1]

    def create_output_data(self):
        if self.output_card is None:
            self.output_card = self.card

        if self.output_asked_users is None:
            self.output_asked_users = self.asked_users

        if self.output_join_users is None:
            initial_prize = self.initial_prize if self.initial_prize else 0
            self.output_join_users = [
                UserRoleCard(user_id=self.owner.id, card_id=self.output_card.id, role_id=CardRole.JOINED, contribution=initial_prize)
            ]

    def call_target(self):
        self.create_input_data()
        data = {
            'deck_id': self.card.id,
            'format': 'format_test',
            'is_ask_mode_enabled': True,
            'asked_user_ids': [u.id for u in self.asked_users],
            'distribution_rule': self.distribution_rule,
            'distribution_for': self.distribution_for,
        }
        if self.initial_prize is not None:
            data['initial_prize'] = self.initial_prize
        if self.prize_to_join is not None:
            data['prize_to_join'] = self.prize_to_join
        if self.evaluation_start_dt is not None:
            data['evaluation_start_dt'] = encode_datetime(self.evaluation_start_dt)
        if self.evaluation_end_dt is not None:
            data['evaluation_end_dt'] = encode_datetime(self.evaluation_end_dt)

        data_json = flask.json.dumps(data)

        response = self.client.post('/api/v1/deck/add_mode', data=data_json, content_type='application/json')
        self.response = response
        self.create_output_data()
        return response

    def assert_questions(self):
        if self.questions is None:
            return
        for idx, child in enumerate(self.card.cards):
            self.assertEqual(child.id, self.questions[idx].id)
            self.assertEqual(child.is_answer, False)

    def assert_date_time(self, dt1, dt2):
        if dt1 is None or dt2 is None:
            self.assertEqual(dt1, dt2)
            return
        dt1 = dt1.astimezone(pytz.utc)
        dt2 = dt2.astimezone(pytz.utc)
        self.assertEqual(dt1, dt2)

    def assert_deck(self):
        deck = Card.query.get(self.output_card.id)

        if len(deck.cards) > 0:
            container = deck.cards[0]
            if container.is_ask_mode_enabled == False and container.type == Card.DECK:
                self.assertEqual(container.name, 'CONTAINER')
                self.assertEqual(container.is_ask_mode_enabled, False)
                self.assertEqual(container.format, '')
                self.assertEqual(container.distribution_for, self.distribution_for)

        self.assertEqual(deck.name, self.card_name)
        self.assertEqual(deck.is_ask_mode_enabled, True)
        self.assertEqual(deck.format, 'format_test')
        self.assertEqual(deck.distribution_for, self.distribution_for)
        self.assertEqual(deck.distribution_rule, self.distribution_rule)
        self.assert_date_time(deck.evaluation_start_dt, self.evaluation_start_dt)
        self.assert_date_time(deck.evaluation_end_dt, self.evaluation_end_dt)

    def assert_asked_users(self):
        self.check_users_in_user_card_roles(
            list(UserRoleCard.query.filter(
                UserRoleCard.card_id == self.output_card.id,
                UserRoleCard.role_id == CardRole.ASKED
            )),
            self.output_asked_users
        )

    def assert_join_users(self):
        joined_urcs = list(UserRoleCard.query.filter(
            UserRoleCard.card_id == self.output_card.id,
            UserRoleCard.role_id == CardRole.JOINED
        ))
        for idx, actual in enumerate(joined_urcs):
            expected = self.output_join_users[idx]
            self.assertEqual(actual.user_id, expected.user_id)
            self.assertEqual(actual.contribution, expected.contribution)

    def check_users_in_user_card_roles(self, user_card_roles, users):
        self.assertEqual(len(user_card_roles), len(users))
        user_card_roles = sorted(user_card_roles, key=lambda obj: obj.user_id)
        expecteds = sorted(users, key=lambda obj: obj.id)
        for idx, actual in enumerate(user_card_roles):
            expected = expecteds[idx]
            self.assertEqual(actual.user_id, expected.id)

    def assert_response(self):
        self.assertEqual(self.response.status, self.response_status)

    def assert_prizes(self):
        self.assertEqual(self.card.silver_points, self.output_silver_points)
        self.assertEqual(self.card.prize_to_join, self.output_prize_to_join)
        self.assertEqual(self.card.original_prize_pool, self.output_silver_points)

    def assert_output(self):
        self.assert_response()
        self.assert_deck()
        self.assert_asked_users()
        self.assert_join_users()
        self.assert_prizes()
        self.assert_questions()

    def test_success(self):
        self.call_target()
        self.assert_output()

    def test_many_questions(self):
        self.questions = [factories.CardFactory(), factories.CardFactory()]
        self.call_target()
        self.assert_output()

    def test_success_for_card(self):
        '''if we enable ask_mode for card, we have to create new deck and assign this card as firch child to new deck'''
        self.card_type = Card.TEXT
        self.call_target()
        self.output_card = Card.query.get(self.card.parent_id)
        self.assert_output()

    def test_asked_users_is_anyone(self):
        '''if we enable ask_mode for card, we have to create new deck and assign this card as firch child to new deck'''
        self.asked_users = []
        self.call_target()
        # if deck was already ask mode, be sure that new data overwrite old one - delete UserRoleCard
        self.call_target()
        anyone_user = User.query.get(User.ANYONE_ID)
        self.output_asked_users = [anyone_user]
        self.assert_output()

    def test_inititial_prize(self):
        self.initial_prize = 100
        self.prize_to_join = 10

        self.call_target()
        self.output_silver_points = 100
        self.output_prize_to_join = 10

        self.assert_output()

    def test_distribution(self):
        self.distribution_for = 10
        self.distribution_rule = card.DISTRIBUTION_RULE_SPLIT_EVENLY
        self.call_target()
        self.assert_output()

    @mock.patch('app.managers.ask_manager.datetime')
    def test_evaluation_period(self, datetime_mock):
        eastern = timezone('US/Eastern')
        self.evaluation_start_dt = datetime(2016, 11, 28, 9, 51, 38, tzinfo=eastern)
        self.evaluation_end_dt = datetime(2016, 11, 29, 9, 51, 38, tzinfo=eastern)
        now_datetime = datetime(2015, 11, 28, 10, 51, 38, tzinfo=eastern).astimezone(pytz.utc)
        datetime_mock.now.return_value = now_datetime
        self.call_target()
        self.assert_output()
        self.assertEqual(self.output_card.evaluation_period_status, card.EVALUATION_PERIOD_STATUS_CLOSE)

    @mock.patch('app.managers.ask_manager.datetime')
    def test_evaluation_period_is_open(self, datetime_mock):
        eastern = timezone('US/Eastern')
        self.evaluation_start_dt = datetime(2016, 11, 28, 9, 51, 38, tzinfo=eastern)
        self.evaluation_end_dt = datetime(2016, 11, 29, 9, 51, 38, tzinfo=eastern)
        now_datetime = datetime(2016, 11, 28, 10, 51, 38, tzinfo=eastern).astimezone(pytz.utc)
        datetime_mock.now.return_value = now_datetime
        self.call_target()
        self.assert_output()
        self.assertEqual(self.output_card.evaluation_period_status, card.EVALUATION_PERIOD_STATUS_OPEN)
