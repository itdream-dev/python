# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, current_app, request
from flask_security.decorators import auth_token_required
from flask_security.core import current_user
from app.api.utils import dict_to_response
from lib.registry import get_registry
from lib.email import EmailHelper
import logging

_logger = logging.getLogger(__name__)

account_api = Blueprint('account', __name__)


@account_api.route('/get_usernames', methods=['POST'])
@auth_token_required
def get_usernames():
    params = request.json
    try:
        search_key = params.get('search_key')
        if not search_key:
            return jsonify({'usernames': []})
        account_manager = current_app.managers.account_manager
        users = account_manager.get_usernames(search_key)
        users_data = [
            {
                'user_id': u.id,
                'username': u.username,
            }
            for u in users
        ]
        return jsonify({
            'result': 'success',
            'users': users_data
        })
    except Exception as e:
        # TODO
        # report to sentry
        _logger.exception(e)
        return jsonify({'error': 'unknown_error'}), 400


@account_api.route('/does_user_exist', methods=['POST'])
@auth_token_required
@dict_to_response
def does_user_exist():
    params = request.json
    username = params['username']
    registry = get_registry()
    user_repo = registry['USER_REPO']
    user = user_repo.get_user_from_username(username)
    return {'result': user is not None}


@account_api.route('/follow_user', methods=['POST'])
@auth_token_required
@dict_to_response
def follow_user():
    registry = get_registry()
    user_repo = registry['USER_REPO']
    account_manager = current_app.managers.account_manager

    params = request.json
    following_id = params['following_id']

    account_manager.follow_user(
        follower=current_user,
        following=user_repo.get_user(following_id)
    )
    return  account_manager.get_profile(user_repo.get_user(following_id), current_user)
        


@account_api.route('/unfollow_user', methods=['POST'])
@auth_token_required
@dict_to_response
def unfollow_user():
    registry = get_registry()
    user_repo = registry['USER_REPO']
    account_manager = current_app.managers.account_manager

    params = request.json
    following_id = params['following_id']

    account_manager.unfollow_user(
        follower=current_user,
        following=user_repo.get_user(following_id)
    )
    return account_manager.get_profile(user_repo.get_user(following_id), current_user)


@account_api.route('/get_profile', methods=['POST'])
@auth_token_required
@dict_to_response
def get_profile():
    params = request.json
    user_id = params.get('user_id')
    manager = current_app.managers.account_manager
    user = manager.get_user(user_id)
    return manager.get_profile(user, current_user)


GET_POINTS_DUMMY_RESPONSE = {
    'total_silver_points': {'silver': 113, 'gold': 113},
    'cumulative_earnings': {'silver': 113, 'gold': 113},
    'points_purchased': {'silver': 113, 'gold': 113},
    'points_used': {'silver': 113, 'gold': 113},
    'use_points': [
        {'id': 'donate_to_charity', 'name': 'Donate to charity'},
        {'id': 'donate_to_category', 'name': 'Donate to a category'},
        {'id': 'send_to_friend', 'name': 'Send to a friend'},
        {'id': 'convert_to_venmo_credit', 'name': 'Convert to  Venmo credit'},
        {'id': 'convert_to_amazon_gift_card', 'name': 'Convert to Amazon Gift card'},  # NOQA
        {'id': 'convert_to_starbucks_gift_card', 'name': 'Convert to Starbucks Gift card'},  # NOQA
    ],
    'get_points': [
        {'id': 'use_promo_code', 'name': 'Use Promo/Gift code'},
        {'id': '0.99', 'name': '$ 0.99', 'silver_points': 100},
        {'id': '4.99', 'name': '$ 4.99', 'silver_points': 550},
        {'id': '9.99', 'name': '$ 9.99', 'silver_points': 1200},
        {'id': 'verify_with_facebook', 'name': 'Verify with Facebook', 'silver_points': 25},  # NOQA
        {'id': 'verify_with_twitter', 'name': 'Verify with Twitter', 'silver_points': 25},  # NOQA
        {'id': 'verify_with_linkedin', 'name': 'Verify with LinkedIn', 'silver_points': 25},  # NOQA
        {'id': 'verify_with_instagram', 'name': 'Verify with Instagram', 'silver_points': 25},  # NOQA
        {'id': 'invite_3_friends', 'name': 'Invite 3 friends', 'silver_points': 50},  # NOQA
        {'id': 'invite_10_friends', 'name': 'Invite 10 friends', 'silver_points': 50},  # NOQA
        {'id': 'invite_30_friends', 'name': 'Invite 30 friends', 'silver_points': 100},  # NOQA
        {'id': 'first_time_prize_bonus', 'name': 'First time prize bonus', 'silver_points': 500},  # NOQA
    ]
}


@account_api.route('/get_points', methods=['POST'])
@auth_token_required
@dict_to_response
def get_points():
    user = current_user
    dt = GET_POINTS_DUMMY_RESPONSE.copy()
    account_manager = current_app.managers.account_manager
    points_summary = account_manager.get_user_points_summary(user)
    dt.update(points_summary)
    return dt


@account_api.route('/use_points', methods=['POST'])
@auth_token_required
@dict_to_response
def use_points():
    params = request.json

    user_id = params.get('user_id')
    account_manager = current_app.managers.account_manager
    user = account_manager.adjust_gold_points(user_id, -2500)
    dt = GET_POINTS_DUMMY_RESPONSE.copy()
    points_summary = account_manager.get_user_points_summary(user)
    dt.update(points_summary)

    payment_type = params.get('payment_type')
    email = params.get('email')
    if payment_type == 'Venmo':
        username = params.get('username')
        EmailHelper().send_venmo_transfer_email(user, username, email)
    else:
        EmailHelper().send_card_transfer_email(user, payment_type, email)

    return dt


@account_api.route('/get_points_from_venmo', methods=['POST'])
@auth_token_required
@dict_to_response
def get_points_from_venmo():
    params = request.json

    user_id = params.get('user_id')
    amount = params.get('amount')

    silver_points = 0
    if amount == 0.99:
        silver_points = 100
    elif amount == 4.99:
        silver_points = 550
    elif amount == 9.99:
        silver_points = 1200

    account_manager = current_app.managers.account_manager
    user = account_manager.adjust_silver_points(user_id, silver_points)
    dt = GET_POINTS_DUMMY_RESPONSE.copy()
    points_summary = account_manager.get_user_points_summary(user)
    dt.update(points_summary)

    email = params.get('email')
    username = params.get('username')
    EmailHelper().send_get_point_email(
        user, username, email, amount, silver_points
    )

    return dt
