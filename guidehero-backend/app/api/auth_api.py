# -*- coding: utf-8 -*-
import lib.exceptions as exceptions
from flask import Blueprint, jsonify, request, current_app
from flask_security.core import current_user
from flask_security.decorators import auth_token_required
from lib.registry import get_registry
import logging
from utils import dict_to_response
_logger = logging.getLogger(__name__)

auth_api = Blueprint('auth', __name__)


@auth_api.route('/signup', methods=['POST'])
@dict_to_response
def signup():
    params = request.json
    account_manager = current_app.managers.account_manager
    try:
        user = account_manager.create_inactive_account(
            username=params['username'],
            email=params['email']
        )
    except account_manager.CreateInactiveUserException as ex:
        return {'error': str(ex)}
    return {'verification_code': user.verification_code}


@auth_api.route('/verify_email', methods=['POST'])
@dict_to_response
def verify_email():
    params = request.json
    account_manager = current_app.managers.account_manager
    account_manager.verify_email(
        email=params['email'],
        code=params['code']
    )
    return {}


@auth_api.route('/signin', methods=['POST'])
@dict_to_response
def signin():
    params = request.json
    try:
        email = params.get('email', '').lower()
        account_manager = current_app.managers.account_manager
        user = account_manager.login_with_email(email)
        return get_signin_user_info(user)
    except exceptions.RegistrationNotComplete as e:
        return jsonify({
            'error': e.message,
            'auth_token': e.auth_token
        }), 400
    except (
        exceptions.UserDoesntExist,
        exceptions.LoginFailed,
    ) as e:
        return jsonify({'error': e.message}), 400
    except Exception as e:
        # TODO
        # report to sentry
        _logger.exception(e)
        return jsonify({'error': 'unknown_error'}), 400


@auth_api.route('/get_user_info', methods=['POST'])
@auth_token_required
@dict_to_response
def get_user_info():
    # params = request.GET
    registry = get_registry()
    ask_repo = registry['ASK_REPO']
    deck_repo = registry['DECK_REPO']

    params = request.json

    fields = params.get('fields', '').split(',')
    user = current_user
    if params.get('user_id'):
        user_repo = registry['USER_REPO']
        user = user_repo.get_user(params['user_id'])
    else:
        if params.get('username'):
            user_repo = registry['USER_REPO']
            try:
                user = user_repo.get_user_from_username(params['username'])
            except Exception:
                return jsonify({'error': 'user_not_found'}), 400

    data = get_base_user_info(user)

    if 'gives' in fields:
        data['gives'] = [
            it.card.to_dict() for it in ask_repo.giver_repo.search(user=user)
        ]

    if 'asks' in fields:
        data['asks'] = [
            it.card.to_dict() for it in ask_repo.asker_repo.search(user=user)
        ]

    if 'wins' in fields:
        data['wins'] = [
            it.card.to_dict() for it in ask_repo.get_wins(user=user)
        ]

    if 'likes' in fields:
        data['likes'] = [
            it.to_dict() for it in deck_repo.get_cards_liked_by_user(user=user)
        ]

    if 'published' in fields:
        data['published'] = [
            it.to_dict() for it in deck_repo.get_my_published_cards(user=user)
        ]

    return data


@auth_api.route('/edit_user', methods=['POST'])
@auth_token_required
@dict_to_response
def add_basic_info():
    params = request.json

    account_manager = current_app.managers.account_manager
    user = account_manager.edit_user(
        user=current_user,
        first_name=params.get('first_name', ''),
        last_name=params.get('last_name', ''),
        username=params.get('username', ''),
        bio=params.get('bio', ''),
    )

    return get_base_user_info(user)


# @auth_api.route('/add_basic_info', methods=['POST'])
# @auth_token_required
# def add_basic_info():
#     params = request.json

#     try:
#         account_manager = current_app.managers.account_manager
#         first_name = params.get('first_name', '')
#         last_name = params.get('last_name', '')

#         account_manager.update_info(current_user, first_name, last_name)
#         return jsonify({
#             'result': 'success',
#             'auth_token': current_user.get_auth_token()
#         })

#     except Exception as e:
#         # TODO
#         # report to sentry
#         _logger.exception(e)
#         return jsonify({'error': 'unknown_error'}), 400


def get_base_user_info(user):
    return {
        'id': user.id,
        'email': user.email,
        'stripped_email': user.stripped_email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'bio': user.bio,

        'thumbnail_url': user.thumbnail_url,
        'linkedin_profile': user.linkedin_profile,
        'linkedin_headline': user.linkedin_headline,

        'active': user.active,
        'confirmed_at': user.confirmed_at,
        'source': user.source,
        'total_silver_points': user.silver_points,
        'tier': user.tier,

        'is_admin': False
    }


def get_signin_user_info(user):
    return {
        'user': get_base_user_info(user),
        'auth_token': user.get_auth_token()
    }


@auth_api.route('/linkedin_signin', methods=['POST'])
def linkedin_signin():
    params = request.json
    access_token = params.get('access_token')
    account_manager = current_app.managers.account_manager

    try:
        user = account_manager.login_with_linkedin(access_token)
        return jsonify(get_signin_user_info(user))
    except (
        exceptions.MissingAccessToken,
        exceptions.AuthenticationFailed
    ) as e:
        return jsonify({'error': e.message}), 400
    except Exception as e:
        # TODO
        # report to sentry
        _logger.exception(e)
        return jsonify({'error': 'unknown_error'}), 400


# @auth_api.route('/get_my_profile', methods=['GET'])
# @auth_token_required
# def get_my_profile():
#     try:
#         return jsonify({
#             'profile_data': current_user.get_basic_data(),
#             'skills_data': [
#                 user_skill.to_dict() for user_skill in current_user.skills
#             ]
#         })

#     except Exception as e:
#         # TODO
#         # report to sentry
#         _logger.exception(e)
#         return jsonify({'error': 'unknown_error'}), 400


# @auth_api.route('/add_skill', methods=['POST'])
# @auth_token_required
# def add_skill():
#     params = request.json

#     try:
#         account_manager = current_app.managers.account_manager
#         skill = params.get('skill', '').lower().strip()
#         level = params['level']
#         price = params['price'] * 100
#         details = params.get('details', '')

#         account_manager.add_skill(
#             current_user, skill, level, price, details
#         )
#         return jsonify({
#             'result': 'success'
#         })

#     except Exception as e:
#         # TODO
#         # report to sentry
#         _logger.exception(e)
#         return jsonify({'error': 'unknown_error'}), 400


# @auth_api.route('/edit_skill', methods=['POST'])
# @auth_token_required
# def edit_skill():
#     params = request.json

#     try:
#         account_manager = current_app.managers.account_manager
#         skill_id = params.get('skill_id', -1)
#         level = params['level']
#         price = params['price'] * 100
#         details = params.get('details', '')

#         account_manager.edit_skill(
#             current_user, skill_id, level, price, details
#         )
#         return jsonify({
#             'result': 'success'
#         })

#     except Exception as e:
#         # TODO
#         # report to sentry
#         _logger.exception(e)
#         return jsonify({'error': 'unknown_error'}), 400


# @auth_api.route('/delete_skill', methods=['POST'])
# @auth_token_required
# def delete_skill():
#     params = request.json

#     try:
#         account_manager = current_app.managers.account_manager
#         skill_id = params.get('skill_id', -1)

#         account_manager.delete_user_skill(current_user, skill_id)
#         return jsonify({'result': 'success'})

#     except Exception as e:
#         # TODO
#         # report to sentry
#         _logger.exception(e)
#         return jsonify({'error': 'unknown_error'}), 400


@auth_api.route('/report_device', methods=['POST'])
@auth_token_required
def report_device():
    params = request.json
    device_token = params.get("device_token")
    device_type = params.get("device_type")

    try:
        account_manager = current_app.managers.account_manager
        account_manager.register_device(
            current_user, device_token, device_type)
        return jsonify({'result': 'success'})

    except Exception as e:
        # TODO
        # report to sentry
        _logger.exception(e)
        return jsonify({'error': 'unknown_error'}), 400


@auth_api.route('/fb_signin', methods=['POST'])
@dict_to_response
def fb_signin():
    params = request.json
    access_token = params.get('fb_access_token')
    account_manager = current_app.managers.account_manager

    user = account_manager.login_with_facebook(access_token)
    return jsonify(get_signin_user_info(user))


@auth_api.route('/google_signin', methods=['POST'])
def google_signin():
    params = request.json
    access_token = params.get('google_access_token')
    account_manager = current_app.managers.account_manager

    try:
        user = account_manager.login_with_google(access_token)
        return jsonify(get_signin_user_info(user))
    except (
        exceptions.MissingAccessToken,
        exceptions.AuthenticationFailed,
        exceptions.NotVerified,
    ) as e:
        return jsonify({'error': e.message}), 400
    except Exception as e:
        # TODO
        # report to sentry
        _logger.exception(e)
        return jsonify({'error': 'unknown_error'}), 400


@auth_api.route('/edit_profile', methods=['POST'])
@auth_token_required
def edit_profile():
    params = request.json

    try:
        account_manager = current_app.managers.account_manager
        first_name = params.get('first_name')
        last_name = params.get('last_name')
        username = params.get('username', '')

        if not (first_name and last_name and username):
            raise exceptions.InvalidName

        bio = params.get('bio', '')
        if len(bio) > 10000:
            raise exceptions.BioTooLong

        user = account_manager.edit_profile(
            current_user, first_name, last_name, username, bio
        )
        return jsonify({
            'result': 'success',
            'name': user.name,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': user.bio
        })
    except (
        exceptions.InvalidName,
        exceptions.UsernameAlreadyExists,
        exceptions.BioTooLong
    ) as e:
        return jsonify({'error': e.message}), 400

    except Exception as e:
        # TODO
        # report to sentry
        _logger.exception(e)
        return jsonify({'error': 'unknown_error'}), 400


# V2 signup method starts here
@auth_api.route('/send_confirmation_email', methods=['POST'])
@dict_to_response
def send_confirmation_email():
    params = request.json
    email = params.get('email')
    username = params.get('username')
    year = int(params.get('year'))
    account_manager = current_app.managers.account_manager

    account_manager.send_confirmation_email(email, username, year)
    return {'result': 'success'}


@auth_api.route('/resend_confirmation_email', methods=['POST'])
@dict_to_response
def ressend_confirmation_email():
    params = request.json
    email = params.get('email')
    account_manager = current_app.managers.account_manager

    account_manager.resend_confirmation_email(email)
    return {'result': 'success'}


@auth_api.route('/check_confirmation_code', methods=['POST'])
@dict_to_response
def check_confirmation_code():
    params = request.json
    email = params.get('email')
    confirmation_code = params.get('confirmation_code')
    account_manager = current_app.managers.account_manager

    account_manager.check_confirmation_code(email, confirmation_code)
    return {'result': 'success'}


@auth_api.route('/fb_signin_v2', methods=['POST'])
@dict_to_response
def fb_signin_v2():
    params = request.json
    email = params.get('email')
    confirmation_code = params.get('confirmation_code')
    access_token = params.get('fb_access_token')
    account_manager = current_app.managers.account_manager

    user = account_manager.login_with_facebook_v2(
        email, confirmation_code, access_token
    )
    return jsonify(get_signin_user_info(user))
