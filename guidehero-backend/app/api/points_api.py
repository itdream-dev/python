from flask import Blueprint, current_app, request
from flask_security.decorators import auth_token_required
from app.api.utils import dict_to_response


points_api = Blueprint('points', __name__)


@points_api.route('/transfer', methods=['POST'])
@auth_token_required
@dict_to_response
def transfer():
    params = request.json
    points_manager = current_app.managers.points_manager
    points_manager.transfer(
        user_from=params.get('user_from'),
        user_to=params.get('user_to'),
        card_to=params.get('card_to'),
        silver_points=params.get('silver_points'),
        transaction_type=params['transaction_type']
    )

    return {}
