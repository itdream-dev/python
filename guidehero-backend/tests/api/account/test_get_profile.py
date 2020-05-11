from ..base import ApiBaseTestCase
from tests.helpers import factories
import flask


class GetProfileTestCase(ApiBaseTestCase):

    def setUp(self):
        super(GetProfileTestCase, self).setUp()
        factories.JsonResponseFactory.register_assert(self)

    def call_target(self, user_id):
        request_env = factories.ApiRequestEnvironmentFactory(
            path='/api/v1/account/get_profile',
            data=dict(user_id=user_id)
        )
        response = self.client.open(**request_env)
        self.assertEqual(response.status, '200 OK')
        return response

    def test_success(self):
        user = factories.UserFactory(silver_points=39, gold_points=44)
        card = factories.CardFactory(creator=user, likes=4)
        self.db.session.commit()
        response = self.call_target(user_id=user.id)

        res = flask.json.loads(response.data)

        self.assertEqual(res['user_info']['user_id'], user.id)
        self.assertEqual(len(res['cards']), 1)
        self.assertEqual(res['cards'][0]['id'], card.id)

        stats = res['stats']

        self.assertEqual(stats['total_followers'], 0)
        self.assertEqual(stats['total_followings'], 0)
        self.assertEqual(stats['total_likes'], 4)
        self.assertEqual(stats['total_shared'], 113)
        self.assertEqual(stats['total_points'], {'silver': 39, 'gold': 44})

    def test_followers(self):
        user = factories.UserFactory()
        self.db.session.add(user)

        follower = factories.UserFactory()
        user.followers.append(follower)
        self.db.session.add(follower)

        current_user = factories.UserFactory()
        self.db.session.add(current_user)
        follower.followers.append(current_user)

        self.db.session.commit()

        self.set_current_user(current_user)

        response = self.call_target(user_id=user.id)

        res = flask.json.loads(response.data)

        followers = res['followers']
        stats = res['stats']
        self.assertEqual(stats['total_followers'], 1)
        self.assertEqual(len(followers), 1)
        self.assertEqual(followers[0]['user_id'], follower.id)
        self.assertEqual(followers[0]['follow_by_current_user'], True)

    def test_followings(self):
        user = factories.UserFactory()
        self.db.session.add(user)

        following = factories.UserFactory()
        user.followings.append(following)
        self.db.session.add(following)
        
        current_user = factories.UserFactory()
        self.db.session.add(current_user)
        following.followers.append(current_user)

        self.db.session.commit()

        self.set_current_user(current_user)

        response = self.call_target(user_id=user.id)

        res = flask.json.loads(response.data)

        followings = res['followings']
        stats = res['stats']
        self.assertEqual(stats['total_followings'], 1)
        self.assertEqual(len(followings), 1)
        self.assertEqual(followings[0]['user_id'], following.id)
        self.assertEqual(followings[0]['follow_by_current_user'], True)
