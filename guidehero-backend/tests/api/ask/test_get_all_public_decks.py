import json
from ..base import ApiBaseTestCase
from tests.helpers import factories

from lib.models.card import Card


class GetAllPublicDecksTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(GetAllPublicDecksTestCase, self).__init__(*args, **kwargs)
        self.url = '/api/v1/deck/get_all_public_decks'

    def test_success(self):

        deck1 = factories.CardFactory(type=Card.DECK, name='1 Test DEck', published=True)
        self.db.session.add(deck1)
        deck2 = factories.CardFactory(type=Card.DECK, name='2 Test Deck', published=True)
        self.db.session.add(deck2)
        deck_not_published = factories.CardFactory(type=Card.DECK, name='3 Not published Deck', published=False)
        self.db.session.add(deck_not_published)
        self.db.session.commit()

        data = {}

        response = self.client.get(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status, '200 OK')
        decks = json.loads(response.data)['all_decks']
        decks = sorted(decks, key=lambda c: c['name'])
        self.assertEqual(len(decks), 2)
        self.assertEqual(decks[0]["id"], deck1.id)
        self.assertEqual(decks[1]["id"], deck2.id)

    def test_ordet_by(self):

        deck1 = factories.CardFactory(type=Card.DECK, name='1 Test DEck', published=True, created_at=1)
        self.db.session.add(deck1)
        deck2 = factories.CardFactory(type=Card.DECK, name='2 Test Deck', published=True, created_at=2)  # newer than deck1
        self.db.session.add(deck2)
        self.db.session.commit()

        data = {}

        response = self.client.get(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status, '200 OK')
        decks = json.loads(response.data)['all_decks']
        self.assertEqual(len(decks), 2)
        self.assertEqual(decks[0]["id"], deck2.id)
        self.assertEqual(decks[1]["id"], deck1.id)

    def test_ask_deck_should_return_format_and_users(self):
        from lib.models.card_role import CardRole
        from lib.models.user_role_card import UserRoleCard
        from lib.models.user import User

        deck1 = factories.CardFactory(type=Card.DECK, name='1 Test DEck', published=True, is_ask_mode_enabled=True, format='test format')
        self.db.session.add(deck1)

        user = User(username='john smith', active=True)
        self.db.session.add(user)
        self.db.session.commit()

        urc = UserRoleCard(user_id=user.id, role_id=CardRole.ASKED, card_id=deck1.id)

        self.db.session.add(urc)

        self.db.session.commit()

        data = {}

        response = self.client.get(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status, '200 OK')
        decks = json.loads(response.data)['all_decks']
        self.assertEqual(len(decks), 1)

        d = decks[0]
        self.assertEqual(d['ask_enabled'], True)
        self.assertEqual(d['format'], 'test format')
        self.assertEqual(len(d['asked_users']), 1)
        asked_user = d['asked_users'][0]
        self.assertEqual(asked_user['user_id'], user.id)
        self.assertEqual(asked_user['username'], user.username)
