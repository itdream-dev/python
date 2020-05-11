
from ..base import ApiBaseTestCase
from tests.helpers import factories


class UnlikeCommentTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(UnlikeCommentTestCase, self).__init__(*args, **kwargs)
        factories.JsonResponseFactory.register_assert(self)

    def call_target(self, **request_data):
        input_obj = factories.ApiRequestEnvironmentFactory(
            path='/api/v1/deck/unlike_comment',
            data=dict(**request_data)
        )
        response = self.client.open(**input_obj)
        return response

    def test_succcess(self):
        comment = factories.Comment()
        self.db.session.add(comment)
        like = factories.CommentLike(user=self.user, comment=comment)
        self.db.session.add(like)
        self.db.session.commit()
        self.assertEqual(comment.likes, 1)

        result = self.call_target(
            comment_id=comment.id

        )
        self.assertEqual(result, factories.JsonResponseFactory.build())

        comment1 = factories.Comment.get(comment.id)
        self.assertEqual(comment1.likes, 0)
