import mock
from ..base import ApiBaseTestCase
from tests.helpers import factories
from flask import current_app


class EditImageCardTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(EditImageCardTestCase, self).__init__(*args, **kwargs)
        factories.CardFactory.register_assert(self)
        factories.JsonResponseFactory.register_assert(self)
        self.url = '/api/v1/deck/edit_image_card'

    def call_target(self, **request_data):
        input_obj = factories.ApiRequestEnvironmentFactory(
            path='/api/v1/deck/edit_image_card',
            data=dict(**request_data)
        )
        response = self.client.open(**input_obj)
        return response

    def test_check_smiple_fields(self):
        upload_helper = current_app.managers.deck_manager.upload_helper
        with mock.patch.object(upload_helper, "s3_image_cloudfront", 'helper'):
            card = factories.ImageCardFactory.create(name='name1', creator=self.user)
            result = self.call_target(
                card_id=card.id,
                s3_file_name='s3_file_name',
                card_title='card_title',
                card_description='card_description',
                image_x=10,
                image_y=11,
                image_width=12,
                image_height=13,
                tags=['tag1'],
                image_scale=8,
            )

            card = factories.ImageCardFactory.get(card.id)
            self.assertEqual(
                card,
                factories.ImageCardFactory.build(
                    id=card.id,
                    name='card_title',
                    content='helper/s3_file_name',
                    description='card_description',
                    x_position=10,
                    y_position=11,
                    width=12,
                    height=13,
                    scale=8,
                    tags=[factories.Tag.build(name='tag1')]
                )
            )
            self.assertEqual(
                result,
                factories.JsonResponseFactory.build(
                    data=card.to_dict()
                )
            )
