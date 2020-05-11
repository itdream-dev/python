

class UserExtended(object):

    def __init__(self, user):
        self.user = user

    def to_dict(self):
        from lib.models.user import serialize_user_extended
        return serialize_user_extended(self.user)


class Card(object):
    def __init__(self, card):
        self.card = card

    def to_dict(self):
        return self.card.to_dict()
