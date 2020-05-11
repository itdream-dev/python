from ..base import ApiBaseTestCase

import flask
from lib.models.card import Card
from lib.models import card as card_module
from lib.models.user_role_card import UserRoleCard
from lib.models import card_role
from lib.models.user import User


class GetWinnersTestCase(ApiBaseTestCase):

    def setUp(self):
        super(GetWinnersTestCase, self).setUp()

    def test_success(self):
        deck = Card(evaluation_period_status=card_module.EVALUATION_PERIOD_STATUS_DONE)
        self.db.session.add(deck)
        user = User()
        self.db.session.add(user)
        ucr = UserRoleCard(user=user, card=deck, role_id=card_role.CardRole.ASKED, total_likes=10, prize=100)
        self.db.session.add(ucr)

        self.db.session.commit()
        data = {
            'deck_id': deck.id
        }
        response = self.client.get('/api/v1/deck/get_winners', query_string=data, content_type='application/json')
        self.assertEqual(response.status, '200 OK')
        res = flask.json.loads(response.data)

        total_likes = res['total_likes']
        self.assertEqual(total_likes, 10)

        winners = res['winners']
        self.assertEqual(len(winners), 1)
        it = winners[0]
        self.assertEqual(it['user_id'], user.id)
        self.assertEqual(it['likes'], 10)
        self.assertEqual(it['likes_relative'], 100)
        self.assertEqual(it['prize'], 100)
