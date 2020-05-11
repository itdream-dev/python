from ..base import ApiBaseTestCase

import flask
from lib.models.card import Card
from lib.models import card as card_module
from lib.models.user_role_card import UserRoleCard
from lib.models import card_role
from lib.models.user import User


class GetSponsorsTestCase(ApiBaseTestCase):

    def test_success(self):
        deck = Card(evaluation_period_status=card_module.EVALUATION_PERIOD_STATUS_DONE)
        self.db.session.add(deck)
        user = User()
        self.db.session.add(user)
        ucr = UserRoleCard(user=user, card=deck, role_id=card_role.CardRole.JOINED, total_likes=10, prize=100, contribution=10)
        self.db.session.add(ucr)

        self.db.session.commit()
        data = {
            'deck_id': deck.id
        }
        response = self.client.get('/api/v1/deck/get_sponsors', data=flask.json.dumps(data), content_type='application/json')
        self.assertEqual(response.status, '200 OK')
        res = flask.json.loads(response.data)

        sponsors = res['sponsors']
        self.assertEqual(len(sponsors), 1)
        it = sponsors[0]
        self.assertEqual(it['user_id'], user.id)
        self.assertEqual(it['contribution'], 10)
