from ..base import ApiBaseTestCase
from tests.helpers import factories
import factory
from app.api.account_api import GET_POINTS_DUMMY_RESPONSE
from lib.models import transfer


def create_data(o):

    dt = GET_POINTS_DUMMY_RESPONSE.copy()
    if o.total_points is not None:
        dt['total_points'] = o.total_points
    if o.cumulative_earnings is not None:
        dt['cumulative_earnings'] = o.cumulative_earnings
    if o.points_purchased is not None:
        dt['points_purchased'] = o.points_purchased
    if o.points_used is not None:
        dt['points_used'] = o.points_used
    return dt


class GetPointsResponse(factories.JsonResponseFactory):
    data = factory.LazyAttribute(create_data)
    total_points = None
    cumulative_earnings = None
    points_purchased = None
    points_used = None

    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        for n in ['total_points', 'cumulative_earnings', 'points_purchased', 'points_used']:
            kwargs.pop(n)
        return factories.JsonResponseFactory._adjust_kwargs(**kwargs)


class UserFactory(factories.UserFactory):
    total_points = {'gold': 0, 'silver': 0}
    cumulative_earnings = None
    points_purchased = None
    points_used = None

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        total_points = kwargs.pop('total_points')
        cumulative_earnings = kwargs.pop('cumulative_earnings')
        points_purchased = kwargs.pop('points_purchased')
        points_used = kwargs.pop('points_used')

        if total_points:
            kwargs['silver_points'] = total_points['silver']
            kwargs['gold_points'] = total_points['gold']
        obj = super(UserFactory, cls)._create(model_class, *args, **kwargs)

        if cumulative_earnings:
            tr_earnings = factories.Transfer(
                user_to=obj,
                transaction_type=transfer.TYPES['earn'].code,
                silver_points=cumulative_earnings['silver'],
                gold_points=cumulative_earnings['gold']
            )
            cls._meta.sqlalchemy_session.add(tr_earnings)

        if points_purchased:
            tr_purchased = factories.Transfer(
                user_to=obj,
                transaction_type=transfer.TYPES['purchase'].code,
                silver_points=points_purchased['silver'],
                gold_points=points_purchased['gold'],
            )
            cls._meta.sqlalchemy_session.add(tr_purchased)

        if points_used:
            tr_used = factories.Transfer(
                user_from=obj,
                transaction_type=transfer.TYPES['earn'].code,
                silver_points=points_used['silver'],
                gold_points=points_used['gold'],
            )
            cls._meta.sqlalchemy_session.add(tr_used)

        return obj


class GetProfileTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(GetProfileTestCase, self).__init__(*args, **kwargs)
        factories.JsonResponseFactory.register_assert(self)
        GetPointsResponse.register_assert(self)

    def test_success(self):
        user = UserFactory(
            id='WFT',
            total_points={'gold': 81, 'silver': 80},
            cumulative_earnings={'gold': 46, 'silver': 45},
            points_purchased={'gold': 34, 'silver': 33},
            points_used={'gold': 24, 'silver': 23},
        )
        self.db.session.commit()
        self.set_current_user(user)

        request_environment = factories.ApiRequestEnvironmentFactory(
            path='/api/v1/account/get_points'
        )

        response = self.client.open(**request_environment)
        self.assertEqual(response, GetPointsResponse(
            total_points={'gold': 81, 'silver': 80},
            cumulative_earnings={'gold': 46, 'silver': 45},
            points_purchased={'gold': 34, 'silver': 33},
            points_used={'gold': 24, 'silver': 23},

            # total_silver_points=80,
            # cumulative_earnings=45,
            # points_purchased=33,
            # points_used=23
        ))

    def test_no_points(self):
        user = UserFactory(
            id='WFT',
        )
        self.db.session.commit()
        self.set_current_user(user)

        request_environment = factories.ApiRequestEnvironmentFactory(
            path='/api/v1/account/get_points'
        )

        response = self.client.open(**request_environment)
        self.assertEqual(response, GetPointsResponse(
            total_points={'gold': 0, 'silver': 0},
            cumulative_earnings={'gold': 0, 'silver': 0},
            points_purchased={'gold': 0, 'silver': 0},
            points_used={'gold': 0, 'silver': 0},
        ))
