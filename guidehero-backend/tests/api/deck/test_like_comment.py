from ..base import ApiBaseTestCase
from tests.helpers import factories


class AddCommentTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(AddCommentTestCase, self).__init__(*args, **kwargs)
        factories.Comment.register_assert(self)
        factories.JsonResponseFactory.register_assert(self)

    def call_target(self, **request_data):
        input_obj = factories.ApiRequestEnvironmentFactory(
            path='/api/v1/deck/like_comment',
            data=dict(**request_data)
        )
        response = self.client.open(**input_obj)
        return response

    def test_succcess(self):
        comment = factories.Comment()
        self.db.session.commit()
        result = self.call_target(
            comment_id=comment.id
        )
        self.assertEqual(result, factories.JsonResponseFactory.build())

        comment = factories.Comment.get(comment.id)
        self.assertEqual(comment.likes, 1)
        self.assertIsNotNone(
            factories.CommentLike.get(user=self.user, comment=comment),
        )
