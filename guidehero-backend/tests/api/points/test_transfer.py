from ..base import ApiBaseTestCase
from tests.helpers import factories
from lib.models import transfer


class TransferTestCase(ApiBaseTestCase):

    def __init__(self, *args, **kwargs):
        super(TransferTestCase, self).__init__(*args, **kwargs)
        factories.UserFactory.register_assert(self)
        factories.CardFactory.register_assert(self)
        factories.Transfer.register_assert(self)
        factories.JsonResponseFactory.register_assert(self)

    def call_target(self, **data):
        request_environment = factories.ApiRequestEnvironmentFactory(
            path='/api/v1/points/transfer',
            data=data
        )
        result = self.client.open(**request_environment)
        self.assertEqual(
            result,
            factories.JsonResponseFactory.build()
        )

    def test_send_to_friend(self):
        user_from = factories.UserFactory(silver_points=100, username='un1')
        user_to = factories.UserFactory(silver_points=30, username='un2')
        self.call_target(
            user_from=user_from.id,
            user_to=user_to.id,
            transaction_type='send_to_friend',
            silver_points=50
        )
        self.assertEqual(
            factories.UserFactory.get(user_from.id),
            factories.UserFactory.build(id=user_from.id, silver_points=50, username='un1')
        )
        self.assertEqual(
            factories.UserFactory.get(user_to.id),
            factories.UserFactory.build(id=user_to.id, silver_points=80, username='un2')
        )
        tr = factories.Transfer.get()[0]
        self.assertEqual(
            tr,
            factories.Transfer.build(
                id=tr.id,
                user_from=user_from,
                user_to=user_to,
                silver_points=50,
                transaction_type='send_to_friend',
            )
        )

    def test_create_ask(self):
        with factories.TransferTypeRepository() as transaction_type_repository:
            transaction_type = transaction_type_repository.create(code='create_ask', silver_points=55)
            user_from = factories.UserFactory(silver_points=100, username='un1')
            card_to = factories.DeckFactory(silver_points=0)
            self.call_target(
                user_from=user_from.id,
                card_to=card_to.id,
                transaction_type=transaction_type.code
            )
            self.assertEqual(
                factories.UserFactory.get(user_from.id),
                factories.UserFactory.build(id=user_from.id, silver_points=100 - transaction_type.silver_points, username='un1')
            )
            self.assertEqual(
                factories.CardFactory.get(card_to.id),
                factories.CardFactory.build(id=card_to.id, silver_points=0)
            )
            tr = factories.Transfer.get()[0]
            self.assertEqual(
                tr,
                factories.Transfer.build(
                    id=tr.id,
                    user_from=user_from,
                    card_to=card_to,
                    silver_points=transaction_type.silver_points,
                    transaction_type=transaction_type.code,
                )
            )

    def test_verify_with_facebook(self):
        user_to = factories.UserFactory(silver_points=30, username='un1')
        transaction_type = transfer.TYPES['verify_with_facebook']
        self.call_target(
            user_to=user_to.id,
            transaction_type=transaction_type.code
        )
        self.assertEqual(
            factories.UserFactory.get(user_to.id),
            factories.UserFactory.build(id=user_to.id, silver_points=30 + transaction_type.silver_points, username='un1')
        )
        tr = factories.Transfer.get()[0]
        self.assertEqual(
            tr,
            factories.Transfer.build(
                id=tr.id,
                user_to=user_to,
                silver_points=transaction_type.silver_points,
                transaction_type=transaction_type.code,
            )
        )
