from lib.models.user import User
from ..base import ApiBaseTestCase
from lib.models import card_role
from tests.helpers import factories
import flask


class GetUserInfoTestCase(ApiBaseTestCase):
    def setUp(self):
        super(GetUserInfoTestCase, self).setUp()
        user = User(id='TestUser', username='test', email='test@test.com', password='12345')
        self.db.session.add(user)
        self.db.session.commit()
        self.set_current_user(user)
        self.user = user

        self.data = {}

    def call_target(self):
        response = self.client.post('/api/v1/auth/get_user_info', data=flask.json.dumps(self.data), content_type='application/json')
        return response

    def test_basic_info(self):
        response = self.call_target()
        self.assertEqual(response.status, '200 OK')
        data = flask.json.loads(response.data)
        self.assertEqual(data['id'], self.user.id)

    def test_basic_info_for_another_user(self):
        user = factories.UserFactory()
        self.db.session.add(user)
        self.db.session.commit()
        self.data['user_id'] = user.id
        response = self.call_target()
        self.assertEqual(response.status, '200 OK')
        data = flask.json.loads(response.data)
        self.assertEqual(data['id'], user.id)

    def test_many_fields(self):
        self.data['fields'] = 'gives,asks'
        response = self.call_target()

        self.assertEqual(response.status, '200 OK')
        data = flask.json.loads(response.data)

        self.assertEqual(len(data['gives']), 0)
        self.assertEqual(len(data['asks']), 0)

    def test_gives(self):
        card = factories.CardFactory()
        self.db.session.add(card)
        urc = factories.UserRoleCard(card=card, user=self.user, role_id=card_role.CardRole.GIVER)
        self.db.session.add(urc)
        self.db.session.commit()

        self.data['fields'] = 'gives'
        response = self.call_target()

        self.assertEqual(response.status, '200 OK')
        data = flask.json.loads(response.data)

        gives = data['gives']
        self.assertEqual(len(gives), 1)
        self.assertEqual(gives[0]['id'], card.id)

    def test_asks(self):
        card = factories.CardFactory()
        self.db.session.add(card)
        urc = factories.UserRoleCard(card=card, user=self.user, role_id=card_role.CardRole.JOINED)
        self.db.session.add(urc)
        self.db.session.commit()

        self.data['fields'] = 'asks'
        response = self.call_target()

        self.assertEqual(response.status, '200 OK')
        data = flask.json.loads(response.data)

        asks = data['asks']
        self.assertEqual(len(asks), 1)
        self.assertEqual(asks[0]['id'], card.id)

    def test_wins(self):
        ask = factories.CardFactory()
        self.db.session.add(ask)
        urc = factories.UserRoleCard(card=ask, user=self.user, role_id=card_role.CardRole.GIVER, prize=10)
        self.db.session.add(urc)
        self.db.session.commit()

        self.data['fields'] = 'wins'
        response = self.call_target()

        self.assertEqual(response.status, '200 OK')
        data = flask.json.loads(response.data)

        asks = data['wins']
        self.assertEqual(len(asks), 1)
        self.assertEqual(asks[0]['id'], ask.id)

    def test_likes(self):
        '''Get all card liked by user'''
        card = factories.CardFactory()
        self.db.session.add(card)
        user = factories.UserFactory()
        self.db.session.add(user)
        like = factories.CardLikesFactory(card=card, user=user)
        self.db.session.add(like)
        self.db.session.commit()

        self.data['fields'] = 'likes'
        self.data['user_id'] = user.id
        response = self.call_target()

        self.assertEqual(response.status, '200 OK')
        data = flask.json.loads(response.data)

        cards = data['likes']
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]['id'], card.id)

    def test_published(self):
        '''Get all card published by user'''
        user = factories.UserFactory()
        self.db.session.add(user)
        card = factories.CardFactory(user_id=user.id, published=True, creator=user)
        self.db.session.add(card)
        self.db.session.commit()

        self.data['fields'] = 'published'
        self.data['user_id'] = user.id
        response = self.call_target()

        self.assertEqual(response.status, '200 OK')
        data = flask.json.loads(response.data)

        cards = data['published']
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]['id'], card.id)
