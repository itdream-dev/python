from tests.app_base_testcase import AppBaseTestCase
from lib.models.card import Card
from lib.models.user import User
from lib.models.user_role_card import UserRoleCard
from lib.models.card_role import CardRole
from tests.helpers import factories
from datetime import datetime
from pytz import timezone


class CommentToDictTestCase(AppBaseTestCase):

    def test_liked_by_user(self):
        user = factories.UserFactory()
        comment = factories.Comment()
        comment_like = factories.CommentLike(user=user, comment=comment)
        self.db.session.add(user)
        self.db.session.add(comment)
        self.db.session.add(comment_like)
        self.db.session.commit()
        result = comment.to_dict(user)
        self.assertEqual(result['likes'], 1)
        self.assertEqual(result['liked_by_current_user'], True)

    def test_not_liked_by_user(self):
        user = factories.UserFactory()
        comment = factories.Comment()
        self.db.session.add(user)
        self.db.session.add(comment)
        self.db.session.commit()
        result = comment.to_dict(user)
        self.assertEqual(result['likes'], 0)
        self.assertEqual(result['liked_by_current_user'], False)

    def test_default_fields(self):
        writer = factories.UserFactory()
        comment = factories.Comment(user=writer)
        self.db.session.add(comment)
        self.db.session.commit()
        result = comment.to_dict()
        self.assertEqual(result['likes'], 0)
        self.assertEqual(result['liked_by_current_user'], None)
        self.assertEqual(result['user_id'], writer.id)
