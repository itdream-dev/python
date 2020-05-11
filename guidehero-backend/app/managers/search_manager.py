from lib.registry import get_registry
from lib.exceptions import InvalidArguments


class SearchManager(object):

    def __init__(self):
        registry = get_registry()
        self.search_repo = registry['SEARCH_REPO']
        self.user_repo = registry['USER_REPO']

    def search_tutors(self, user, keywords):
        self.search_repo.add_searches(user, keywords)
        return self.user_repo.get_tutors_with_skill(user, keywords)

    def request_help(self, user, expert_id, skill_id):
        expert = self.user_repo.get_user(expert_id)
        user_skill = self.user_repo.get_user_skill(expert_id, skill_id)
        self.search_repo.request_help(user, expert, user_skill)

    def cancel_help(self, user, expert_id, skill_id):
        expert = self.user_repo.get_user(expert_id)
        user_skill = self.user_repo.get_user_skill(expert_id, skill_id)
        self.search_repo.cancel_help(user, expert, user_skill)

    def request_experts(self, user, approx_call_time, price_per_min, max_wait,
                        experts):
        if not (user and approx_call_time and max_wait and experts):
            raise InvalidArguments
        self.search_repo.request_experts(
            user, approx_call_time, price_per_min, max_wait, experts)

    def get_offers(self, user):
        return self.search_repo.get_offers(user)
