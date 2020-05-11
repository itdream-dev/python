from lib.registry import get_registry

db = get_registry()['DB']


class CardPermission(db.Model):
    __tablename__ = 'card_permission'
    permissions = ('view', 'add_card', 'edit', 'delete', 'join_to_ask', 'view_children')

    VIEW = 'view'
    ADD_CARD = 'add_card'
    EDIT = 'edit'
    DELETE = 'delete'
    JOIN_TO_ASK = 'join_to_ask'
    VIEW_CHILDREN = 'view_children'
    id = db.Column(db.String(255), primary_key=True)
