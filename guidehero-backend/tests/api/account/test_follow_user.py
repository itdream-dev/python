from ..base import ApiBaseTestCase
from tests.helpers import factories


class FollowUserTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(FollowUserTestCase, self).__init__(*args, **kwargs)
        factories.JsonResponseFactory.register_assert(self)

    def call_target(self, **request_data):
        input_obj = factories.ApiRequestEnvironmentFactory(
            path='/api/v1/account/follow_user',
            data=dict(**request_data)
        )
        response = self.client.open(**input_obj)
        return response

    def test_follow_user(self):
        follower = factories.UserFactory(id="follower")
        self.db.session.add(follower)

        following = factories.UserFactory(id="following")
        self.db.session.add(following)

        self.set_current_user(follower)

        self.db.session.commit()

        result = self.call_target(
            following_id="following"
        )

        # self.assertEqual(result, factories.JsonResponseFactory.build())
        self.assertEqual(result.status, '200 OK')

        follower = factories.UserFactory.get("follower")
        self.assertEqual(len(follower.followings), 1)
        self.assertEqual(follower.followings[0].id, following.id)

        following = factories.UserFactory.get("following")
        self.assertEqual(len(following.followers), 1)
        self.assertEqual(following.followers[0].id, follower.id)
