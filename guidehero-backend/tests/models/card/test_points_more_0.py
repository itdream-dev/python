from tests.app_base_testcase import AppBaseTestCase
from tests.helpers import factories


class PointsMoreThanTestCase(AppBaseTestCase):

    def test_points_cannot_be_less_than_0(self):
        try:
            factories.CardFactory(silver_points = -1, gold_points = -1)
            self.fail('Value error shoulb be thrown')
        except ValueError:
            pass
