import flask
from lib.models import card as card_module
from lib.models.user import User
from lib.models.user_role_card import UserRoleCard
from ..base import ApiBaseTestCase
from tests.helpers import factories
from lib.models import transfer


class EndEvaluationPeriodTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(EndEvaluationPeriodTestCase, self).__init__(*args, **kwargs)
        factories.Transfer.register_assert(self)

    def setUp(self):
        super(EndEvaluationPeriodTestCase, self).setUp()
        self.answers_data = []
        self.silver_points = 0
        self.distribution_rule = card_module.DISTRIBUTION_RULE_SPLIT_EVENLY
        self.distribution_for = 0
        self.evaluation_period_status = card_module.EVALUATION_PERIOD_STATUS_OPEN
        self.users_data = [
            {'username': '1', 'silver_points': 30},
            {'username': '2', 'silver_points': 0},
            {'username': '3', 'silver_points': 0},
        ]

        self.response = None
        self.deck = None

    def get_urc(self, user_id):
        urc = list(UserRoleCard.query.filter(
            UserRoleCard.user_id == user_id
        ).all())
        if len(urc) == 1:
            return urc[0]
        if len(urc) == 0:
            return UserRoleCard(prize=0, total_likes=0)
        raise Exception('Find more than one user_role_card for user_id={}'.format(user_id))

    def assert_expected_data(self, data):
        for it in data:
            user = User.query.filter(User.username == it['username']).first()
            # inp_user = [u for u in self.users_data if u['username'] == it['username']][0]
            self.assertEqual(user.silver_points, it["silver_points"])
            urc = self.get_urc(user.id)
            self.assertEqual(urc.prize, it.get('prize', 0))
            self.assertEqual(urc.total_likes, it.get('likes', 0))
            if it.get('prize', 0) > 0:
                tr1 = factories.Transfer.get(card_from=self.deck, user_to=user)[0]
                self.assertEqual(
                    tr1,
                    factories.Transfer.build(
                        id=tr1.id,
                        card_from=self.deck,
                        user_to=user,
                        silver_points=it['prize'],
                        transaction_type=transfer.TYPES['prize_for_answer'].code
                    )
                )

    def call_target(self):
        card_factory = factories.CardFactory
        user_factory = factories.UserFactory
        answers = [
            card_factory.create(
                likes=it['likes'],
                creator=user_factory.create(username=it['username'], silver_points=it.get('silver_points', 0))
            )
            for it in self.answers_data
        ]
        deck = factories.AskDeckFactory.create(
            evaluation_period_status=self.evaluation_period_status,
            answers=answers,
            silver_points=self.silver_points,
            distribution_rule=self.distribution_rule,
            distribution_for=self.distribution_for
        )
        self.db.session.commit()
        data = {
            'deck_id': deck.id
        }
        response = self.client.post('/api/v1/deck/end_evaluation_period', data=flask.json.dumps(data), content_type='application/json')
        self.response = response
        self.deck = card_module.Card.query.get(deck.id)

    def assert_shared(self):
        self.assertEqual(self.response.status, '200 OK')
        self.assertEqual(self.deck.silver_points, 0)
        self.assertEqual(self.deck.evaluation_period_status, card_module.EVALUATION_PERIOD_STATUS_DONE)

    def test_distribute_evenly(self):
        self.silver_points = 100
        self.distribution_for = 2
        self.distribution_rule = card_module.DISTRIBUTION_RULE_SPLIT_EVENLY
        self.answers_data = [
            {'likes': 5, 'username': '1', 'silver_points': 30},
            {'likes': 3, 'username': '2', 'silver_points': 0},
            {'likes': 1, 'username': '3', 'silver_points': 0},
        ]
        self.call_target()
        self.assert_shared()
        self.assert_expected_data([
            {'username': '1', 'silver_points': 80, 'prize': 50, 'likes': 5},
            {'username': '2', 'silver_points': 50, 'prize': 50, 'likes': 3},
            {'username': '3', 'silver_points': 0},
        ])

    def test_distribute_proportionally(self):
        self.silver_points = 100
        self.distribution_for = 2
        self.distribution_rule = card_module.DISTRIBUTION_RULE_SPLIT_PROPORTIONALLY
        self.answers_data = [
            {'likes': 5, 'username': '1', 'silver_points': 30},
            {'likes': 3, 'username': '2', 'silver_points': 0},
            {'likes': 1, 'username': '3', 'silver_points': 0},
        ]
        self.call_target()
        self.assert_shared()
        self.assert_expected_data([
            {'username': '1', 'silver_points': 92, 'prize': 62, 'likes': 5},
            {'username': '2', 'silver_points': 37, 'prize': 37, 'likes': 3},
            {'username': '3', 'silver_points': 0},
        ])
