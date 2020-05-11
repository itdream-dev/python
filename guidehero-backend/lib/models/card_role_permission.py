from lib.registry import get_registry

db = get_registry()['DB']


class CardRolePermission(db.Model):
    __tablename__ = 'card_role_permission'
    role_id = db.Column(db.String(255), db.ForeignKey('card_role.id'), primary_key=True)
    permission_id = db.Column(db.String(255), db.ForeignKey('card_permission.id'), primary_key=True)
