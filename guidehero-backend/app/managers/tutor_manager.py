# -*- coding: utf-8 -*-
from lib.registry import get_registry


class TutorManager(object):

    def __init__(self):
        registry = get_registry()
        self.user_repo = registry['USER_REPO']

    def search_tutors(self, user, search_key):
        return self.user_repo.search_tutors(user, search_key)
