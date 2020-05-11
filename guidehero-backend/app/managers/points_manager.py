from lib.registry import get_registry
from lib.models import transfer


class PointsManager(object):
    def __init__(self):
        registry = get_registry()
        self.deck_repo = registry['DECK_REPO']
        self.user_repo = registry['USER_REPO']
        self.db = registry['DB']

    def transfer(self, user_from=None, user_to=None, card_to=None,
                 silver_points=None, transaction_type=None):
        transaction_type = transfer.TYPES[transaction_type]
        tr = None
        if transaction_type == transfer.TYPES['send_to_friend']:
            sender = self.user_repo.get_user(user_from)
            recipient = self.user_repo.get_user(user_to)
            recipient.silver_points += silver_points
            sender.silver_points -= silver_points
            tr = transfer.Transfer(
                user_from=sender,
                user_to=recipient,
                silver_points=silver_points,
                transaction_type=transaction_type.code
            )

        if transaction_type == transfer.TYPES['create_ask']:
            silver_points = transaction_type.silver_points
            sender = self.user_repo.get_user(user_from)
            recipient = self.deck_repo.get_card(card_to)
            recipient.silver_points += silver_points
            sender.silver_points -= silver_points
            tr = transfer.Transfer(
                user_from=sender,
                card_to=recipient,
                silver_points=silver_points,
                transaction_type=transaction_type.code
            )

        if transaction_type == transfer.TYPES['verify_with_facebook']:
            user_to = self.user_repo.get_user(user_to)
            user_to.silver_points += transaction_type.silver_points
            tr = transfer.Transfer(
                user_to=user_to,
                silver_points=transaction_type.silver_points,
                transaction_type=transaction_type.code
            )

        if tr is None:
            raise ValueError(
                'No handler for transaction type: {}'.format(transaction_type)
            )
        self.db.session.add(tr)
        self.db.session.commit()
