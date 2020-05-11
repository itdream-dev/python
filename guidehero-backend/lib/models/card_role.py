from lib.registry import get_registry

db = get_registry()['DB']


class CardRole(db.Model):
    __tablename__ = 'card_role'

    OWNER = 'owner'
    JOINED = 'joined'
    ASKED = 'asked'
    JOIN_CANDIDATE = 'join_candidate'
    VIEWER = 'viewer'
    GIVER = 'giver'

    id = db.Column(db.String(255), primary_key=True)
