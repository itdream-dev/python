import mock
from ..base import ApiBaseTestCase
from tests.helpers import factories
from flask import current_app


class EditVideoCardTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(EditVideoCardTestCase, self).__init__(*args, **kwargs)
        factories.CardFactory.register_assert(self)
        factories.JsonResponseFactory.register_assert(self)

    def call_target(self, **request_data):
        input_obj = factories.ApiRequestEnvironmentFactory(
            path='/api/v1/deck/edit_video_card',
            data=dict(**request_data)
        )
        response = self.client.open(**input_obj)
        return response

    def test_check_smiple_fields(self):
        upload_helper = current_app.managers.deck_manager.upload_helper
        with mock.patch.object(upload_helper, "s3_video_cloudfront", 'helper'):
            card = factories.ImageCardFactory.create(name='name1', creator=self.user)
            result = self.call_target(
                card_id=card.id,
                s3_file_name='s3_file_name',
                card_title='card_title',
                card_description='card_description',
                thumbnail_url='thumbnail_url',
                scale=8,
                tags=['tag1'],
            )
            card = factories.ImageCardFactory.get(card.id)
            self.assertEqual(
                card,
                factories.ImageCardFactory.build(
                    id=card.id,
                    name='card_title',
                    content='helper/s3_file_name',
                    description='card_description',
                    scale=8,
                    sub_content='helper/thumbnail_url',
                    tags=[factories.Tag.build(name='tag1')]
                )
            )
            self.assertEqual(
                result,
                factories.JsonResponseFactory.build(
                    data=card.to_dict()
                )
            )
