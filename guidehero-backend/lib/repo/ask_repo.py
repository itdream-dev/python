from lib.repo.deck_repo import DeckRepo
from lib.models import user_role_card
from lib.models import card_role
from lib.models.user_role_card import UserRoleCard
from lib.registry import get_registry


class UserRelationRepo(object):
    def __init__(self, role_id):
        self.db = get_registry()['DB']
        self.role_id = role_id
        self.model = user_role_card.UserRoleCard

    def search(self, deck=None, user=None):
        return self._filter_urc(
            deck=deck,
            user=user
        ).all()

    def _filter_urc(self, deck=None, user=None):
        q = self.model.query.filter(self.model.role_id == self.role_id)
        if deck is not None:
            q = q.filter(self.model.card == deck)
        if user is not None:
            q = q.filter(self.model.user == user)
        return q

    def exists(self, deck, user):
        res = self.db.session.query(self._filter_urc(deck).filter(self.model.user == user).exists()).scalar()
        return res

    def get_all(self, deck):
        return self._filter_urc(deck).all()

    def add(self, deck, user, **kwargs):
        it = self.model(user=user, card=deck, role_id=self.role_id, **kwargs)
        self.db.session.add(it)

    def remove(self, card, user):
        self._filter_urc(card).filter(self.model.user == user).delete()

    def remove_all(self, card):
        self._filter_urc(card).delete()

    def set(self, deck, users):
        self.remove_all(deck)
        for user in users:
            self.add(deck, user)


class AskRepo(DeckRepo):

    def __init__(self, *args, **kwargs):
        super(AskRepo, self).__init__(*args, **kwargs)
        self.asker_repo = UserRelationRepo(role_id=card_role.CardRole.JOINED)
        self.asked_repo = UserRelationRepo(role_id=card_role.CardRole.ASKED)
        self.giver_repo = UserRelationRepo(role_id=card_role.CardRole.GIVER)

    def get_winners(self, deck):
        return UserRoleCard.query.filter(UserRoleCard.card == deck, UserRoleCard.prize > 0).all()

    def get_wins(self, user):
        return self.giver_repo._filter_urc(user=user).filter(UserRoleCard.prize > 0).all()

    def get_sponsors(self, deck):
        return UserRoleCard.query.filter(UserRoleCard.card == deck, UserRoleCard.contribution > 0).all()
