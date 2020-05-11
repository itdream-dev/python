import unittest

from lib.registry import get_registry
from tests import environment


class AppBaseTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(AppBaseTestCase, self).__init__(*args, **kwargs)
        self.url = ''

    def setUp(self):
        self.app = environment.get_app()
        self.db = get_registry()['DB']
        self.clean_db()

        self.test_request_context = self.app.test_request_context(self.url)
        self.test_request_context.push()

        self.client = self.app.test_client()

    def tearDown(self):
        self.test_request_context.pop()

    def clean_db(self):
        meta = self.db.metadata
        session = self.db.session
        exclude_tables = ('card_role', 'card_permission', 'card_role_permission', 'role')
        tables = [t for t in reversed(meta.sorted_tables) if t.name not in exclude_tables]
        for table in tables:
            session.execute(table.delete())
        session.commit()
        self.__insert_initial_data()

    def __insert_initial_data(self):
        from lib.models.user import User
        u = User(id=User.ANYONE_ID, username='Anyone')
        self.db.session.add(u)
        self.db.session.commit()
