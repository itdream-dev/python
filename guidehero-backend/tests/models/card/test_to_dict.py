from tests.app_base_testcase import AppBaseTestCase
from lib.models.card import Card
from lib.models.user import User
from lib.models.user_role_card import UserRoleCard
from lib.models.card_role import CardRole
from tests.helpers import factories
from datetime import datetime
from pytz import timezone


class CardToDictTestCase(AppBaseTestCase):

    def setUp(self):
        super(CardToDictTestCase, self).setUp()

        self.creator = None
        self.card = None
        self.joined_user1_name = None
        self.joined_user_id1_contribution = None
        self.joined_user_id1 = None
        self.evaluation_period_status = None

        self.result = None
        self.joined_users = None

    def call_target(self, by_user=None):
        if self.card is None:
            self.card = factories.CardFactory(type=Card.DECK, is_ask_mode_enabled=True)
            if self.creator:
                if self.creator.id is None:
                    self.db.session.add(self.creator)
                    self.db.session.commit()

                self.card.creator = self.creator
            if self.evaluation_period_status is not None:
                self.card.evaluation_period_status = self.evaluation_period_status
            self.db.session.add(self.card)
            self.db.session.commit()

        if self.creator is not None:
            urc = UserRoleCard(user_id=self.creator.id, role_id=CardRole.JOINED, card_id=self.card.id)
            self.db.session.add(urc)
            self.db.session.commit()

        if self.joined_user1_name is not None:
            self.joined_user_id1 = User(username=self.joined_user1_name)
            self.db.session.add(self.joined_user_id1)
            self.db.session.commit()

        if self.joined_user_id1 is not None:
            if self.joined_user_id1.id is None:
                self.db.session.add(self.joined_user_id1)
                self.db.session.commit()
            urc = UserRoleCard(user_id=self.joined_user_id1.id, role_id=CardRole.JOINED, card_id=self.card.id)
            if self.joined_user_id1_contribution is not None:
                urc.contribution = self.joined_user_id1_contribution
            self.db.session.add(urc)
            self.db.session.commit()

        res = self.card.to_dict(user=by_user)
        self.result = res
        self.create_expected()
        return self.result

    def create_expected(self):
        self.joined_users = []
        if self.joined_user_id1 is not None:
            self.joined_users.append(self.joined_user_id1)

        if self.creator is not None:
            self.joined_users.append(self.creator)

    def assert_result(self):
        self.assert_joined_users()

    def assert_joined_users(self):
        if self.card.type != Card.DECK:
            return
        real = self.result['joined_users']
        self.assertEqual(len(real), len(self.joined_users))
        real = sorted(real, key=lambda x: x['user_id'])
        self.joined_users = sorted(self.joined_users, key=lambda x: x.id)
        for idx, real_it in enumerate(real):
            exp_it = self.joined_users[idx]
            self.assertEqual(real_it['user_id'], exp_it.id)
            if self.creator and exp_it.id == self.creator.id:
                self.assertEqual(real_it['ask_creator'], True)
            if self.joined_user_id1 and exp_it.id == self.joined_user_id1.id:
                val = self.joined_user_id1_contribution if self.joined_user_id1_contribution is not None else 0
                self.assertEqual(real_it.get('contribution'), val)

    def test_joined_users_serialize(self):
        '''joined users should be serialed in 'joined_users' field'''
        self.joined_user1_name = 'joined_user_id1'
        self.call_target()
        self.joined_users = [self.joined_user_id1]
        self.assert_result()

    def test_joined_users_serialize_with_flag_if_creator(self):
        self.creator = User(username='creator1')
        self.call_target()
        self.joined_users = [self.creator]
        self.assert_result()
        # self.assertEqual(res['joined_users'][0]['ask_creator'], True)

    def test_joined_user_with_contribution(self):
        self.joined_user_id1 = User(username='joined_user1')
        self.joined_user_id1_contribution = 50
        self.call_target()
        self.joined_users = [self.joined_user_id1]
        self.assert_result()

    def test_simple_fields(self):
        from lib.models import card as card_module
        self.creator = User(username='creator')

        self.card = factories.CardFactory(type=Card.DECK, is_ask_mode_enabled=True, creator=self.creator)
        eastern = timezone('US/Eastern')

        self.card.evaluation_period_status = card_module.EVALUATION_PERIOD_STATUS_OPEN
        self.card.distribution_rule = card_module.DISTRIBUTION_RULE_SPLIT_EVENLY
        self.card.distribution_for = 10
        self.card.evaluation_start_dt = datetime(2016, 11, 28, 9, 51, 38, tzinfo=eastern)
        self.card.evaluation_end_dt = datetime(2016, 11, 29, 9, 51, 38, tzinfo=eastern)
        self.card.answer_visibility = card_module.ANSWER_VISIBILITY_ONLY_ASKERS
        self.card.scale = 3
        self.card.original_prize_pool = 123
        self.viewer = factories.UserFactory()
        self.card.views.append(self.viewer)

        self.db.session.add(self.card)
        self.db.session.commit()

        self.call_target()
        self.assert_result()

        self.joined_users = [self.creator]

        self.assertEqual(self.result['evaluation_period_status'], card_module.EVALUATION_PERIOD_STATUS_OPEN)
        self.assertEqual(self.result['distribution_rule'], card_module.DISTRIBUTION_RULE_SPLIT_EVENLY)
        self.assertEqual(self.result['distribution_for'], 10)
        self.assertEqual(self.result['evaluation_start_dt'], datetime(2016, 11, 28, 9, 51, 38, tzinfo=eastern))
        self.assertEqual(self.result['evaluation_end_dt'], datetime(2016, 11, 29, 9, 51, 38, tzinfo=eastern))
        self.assertEqual(self.result['answer_visibility'], card_module.ANSWER_VISIBILITY_ONLY_ASKERS)
        self.assertEqual(self.result['creator_info']['user_id'], self.creator.id)
        self.assertEqual(self.result['scale'], 3)
        self.assertEqual(self.result['original_prize_pool'], 123)
        self.assertEqual(self.result['views_count'], 1)

    def test_for_specific_user_false(self):
        from lib.models import card as card_module
        self.creator = User(username='creator')
        self.card = factories.CardFactory(type=Card.DECK, is_ask_mode_enabled=True, creator=self.creator)
        self.viewer = factories.UserFactory()

        self.db.session.commit()

        self.call_target(by_user=self.viewer)
        self.assert_result()

        self.joined_users = [self.creator]

        self.assertEqual(self.result['views_count'], 0)
        self.assertEqual(self.result['viewed_by_me'], False)
        self.assertEqual(self.result['commented_by_me'], False)
        self.assertEqual(self.result['won_by_me'], False)

    def test_for_specific_user_true(self):
        from lib.models import card as card_module
        self.creator = User(username='creator')

        self.card = factories.CardFactory(type=Card.DECK, is_ask_mode_enabled=True, creator=self.creator)

        self.viewer = factories.UserFactory()
        self.card.views.append(self.viewer)
        self.card.comments.append(factories.Comment(user=self.viewer))

        urc = factories.UserRoleCard(card=self.card, user=self.viewer, prize=56)

        self.db.session.add(self.card)
        self.db.session.commit()

        self.call_target(by_user=self.viewer)

        self.assertEqual(self.result['views_count'], 1)
        self.assertEqual(self.result['viewed_by_me'], True)
        self.assertEqual(self.result['commented_by_me'], True)
        self.assertEqual(self.result['won_by_me'], True)

    def test_image_scale_field(self):
        self.card = factories.CardFactory(type=Card.IMAGE, scale=4)
        self.db.session.commit()

        self.call_target()
        self.assert_result()

        self.assertEqual(self.result['scale'], 4)
        self.assertEqual(self.result['image_scale'], 4)

    def test_givers_and_is_answer_flag(self):
        deck = factories.CardFactory(type=Card.DECK, is_ask_mode_enabled=True)
        self.db.session.add(deck)
        self.db.session.commit()

        question_creator = User(username='question_creator')
        self.db.session.add(question_creator)
        question = Card(type=Card.TEXT, parent_id=deck.id, position=0, is_answer=False, creator=question_creator)
        self.db.session.add(question)

        giver1 = User(username='giver1')
        self.db.session.add(giver1)

        answer = Card(type=Card.TEXT, parent_id=deck.id, creator=giver1, position=1, is_answer=True)
        self.db.session.add(answer)

        answer1 = Card(type=Card.TEXT, parent_id=deck.id, creator=giver1, position=2, is_answer=True)
        self.db.session.add(answer1)

        question1 = Card(type=Card.TEXT, parent_id=deck.id, position=3, is_answer=False, creator=question_creator)
        self.db.session.add(question1)

        self.db.session.commit()

        res = deck.to_dict()
        self.assertEqual(len(res['givers']), 1)
        self.assertEqual(res['givers'][0]['user_id'], giver1.id)

        #check if children elements has correct flag  is_answer
        children = res['children']
        self.assertEqual(len(children), 4)

        self.assertEqual(children[0]['id'], question.id)
        self.assertEqual(children[0]['is_answer'], False)

        self.assertEqual(children[1]['id'], answer.id)
        self.assertEqual(children[1]['is_answer'], True)

        self.assertEqual(children[2]['id'], answer1.id)
        self.assertEqual(children[2]['is_answer'], True)

        self.assertEqual(children[3]['id'], question1.id)
        self.assertEqual(children[3]['is_answer'], False)

    def test_tags_field(self):
        tag = factories.Tag(name='tag1')
        card = factories.CardFactory(tags=[tag])
        self.db.session.commit()

        res = card.to_dict()
        self.assertEqual(len(res['tags']), 1)
        self.assertEqual(res['tags'][0], 'tag1')

    def test_deck_deck_card_structure(self):
        deck = factories.DeckFactory(id="deck", is_ask_mode_enabled=True)
        container = factories.DeckFactory(id='container', parent=deck, is_ask_mode_enabled=False)
        factories.CardFactory(id='card', parent=container)
        self.db.session.commit()

        res = deck.to_dict()
        self.assertEqual(res['id'], 'deck')
        self.assertEqual(len(res['children']), 1)

        c = res['children'][0]
        self.assertEqual(c['id'], 'container')
        self.assertEqual(len(c['children']), 1)

        ca = c['children'][0]
        self.assertEqual(ca['id'], 'card')
        self.assertNotIn('children', ca)

    def test_winners(self):
        ask = factories.AskDeckFactory(id="ask_id")
        user = factories.UserFactory()
        self.db.session.commit()
        urc = UserRoleCard(user_id=user.id, role_id=CardRole.GIVER, card_id=ask.id, prize=15)
        self.db.session.add(urc)
        self.db.session.commit()
        res = ask.to_dict()
        self.assertEqual(len(res['winners']), 1)
        self.assertEqual(res['winners'][0]['user_id'], user.id)
        self.assertEqual(res['winners'][0]['prize'], 15)

    def test_sponsors(self):
        ask = factories.AskDeckFactory(id="ask_id")
        user = factories.UserFactory()
        self.db.session.commit()
        urc = UserRoleCard(user_id=user.id, role_id=CardRole.JOINED, card_id=ask.id, contribution=16)
        self.db.session.add(urc)
        self.db.session.commit()
        res = ask.to_dict()
        self.assertEqual(len(res['sponsors']), 1)
        self.assertEqual(res['sponsors'][0]['user_id'], user.id)
        self.assertEqual(res['sponsors'][0]['contribution'], 16)
