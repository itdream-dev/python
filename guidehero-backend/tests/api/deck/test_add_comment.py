from ..base import ApiBaseTestCase
from tests.helpers import factories
import unittest


class AddCommentTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(AddCommentTestCase, self).__init__(*args, **kwargs)
        factories.CardFactory.register_assert(self)
        factories.Comment.register_assert(self)
        factories.JsonResponseWithResultStatusFactory.register_assert(self)

    def call_target(self, **request_data):
        input_obj = factories.ApiRequestEnvironmentFactory(
            path='/api/v1/deck/add_comment',
            data=dict(**request_data)
        )
        response = self.client.open(**input_obj)
        return response

    def test_succcess(self):
        card = factories.ImageCardFactory.create(name='name1', creator=factories.UserFactory())
        self.db.session.commit()
        result = self.call_target(
            card_id=card.id,
            comment_content='comment_content1',
        )
        card = factories.ImageCardFactory.get(card.id)
        self.assertEqual(len(card.comments), 1)
        comment = card.comments[0]
        self.assertEqual(comment.card, card)
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.id, comment.id)
        self.assertEqual(comment.content, 'comment_content1')
        self.assertEqual(
            result,
            factories.JsonResponseWithResultStatusFactory.build(
                extra_data={
                    'comment': comment.to_dict()
                }
            )
        )

    @unittest.skip('dffff')
    def test_add_sub_comment(self):
        card = factories.ImageCardFactory.create(name='name1', creator=factories.UserFactory())
        self.db.session.add(card)

        comment = factories.Comment(card=card)
        self.db.session.add(comment)

        self.db.session.commit()

        result = self.call_target(
            comment_id=comment.id,
            comment_content='sub_comment',
        )
        self.assertEqual(1, len(comment.sub_comments))
        sub_comment = comment.sub_comments[0]
        self.assertEqual(sub_comment.card, None)
        self.assertEqual(sub_comment.user, self.user)
        self.assertEqual(sub_comment.comment.id, comment.id)
        self.assertEqual(sub_comment.content, 'sub_comment')
        self.assertEqual(
            result,
            factories.JsonResponseWithResultStatusFactory.build(
                extra_data={
                    'comment': sub_comment.to_dict()
                }
            )
        )
