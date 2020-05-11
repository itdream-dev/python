# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, current_app, request
from flask_security.core import current_user
from flask_security.decorators import auth_token_required
import logging
from app.api.utils import dict_to_response

_logger = logging.getLogger(__name__)

deck_api = Blueprint('deck', __name__)


@deck_api.route('/get_all_decks', methods=['GET'])
@auth_token_required
def get_all_decks():
    deck_manager = current_app.managers.deck_manager
    return jsonify({
        'all_decks': deck_manager.get_decks()
    })


@deck_api.route('/get_all_public_decks', methods=['GET'])
@auth_token_required
@dict_to_response
def get_all_public_decks():
    deck_manager = current_app.managers.deck_manager
    decks = deck_manager.get_public_decks()
    return {
        'all_decks': [
            deck.to_dict(user=current_user) for deck in decks
        ]
    }


@deck_api.route('/search_cards', methods=['GET'])
@auth_token_required
def seach_cards():
    params = request.json
    try:
        keywords = params.get('keywords', None)
        deck_manager = current_app.managers.deck_manager
        cards = deck_manager.search_cards(keywords=keywords)
        return jsonify({
            'cards': [
                card.to_dict(user=current_user) for card in cards
            ]
        })
    except Exception as e:
        # TODO
        # report to sentry
        _logger.exception(e)
        return jsonify({'error': 'unknown_error'}), 400


@deck_api.route('/get_my_published_decks', methods=['GET'])
@auth_token_required
def get_my_published_decks():
    try:
        deck_manager = current_app.managers.deck_manager
        decks = deck_manager.get_my_published_decks(current_user)
        return jsonify({
            'all_decks': [deck.to_dict(user=current_user) for deck in decks],
            'name': current_user.name,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'bio': current_user.bio,
            'thumbnail': current_user.thumbnail_url
        })
    except Exception as e:
        # TODO
        # report to sentry
        _logger.exception(e)
        return jsonify({'error': 'unknown_error'}), 400


@deck_api.route('/create_text_card', methods=['POST'])
@auth_token_required
@dict_to_response
def create_text_card():
    deck_manager = current_app.managers.deck_manager
    params = request.json

    card_title = params.get('card_title')
    pronunciation_language = params.get('language')
    card_content = params.get('card_content')
    description = params.get('card_description', '')
    deck_manager.create_text_card(
        current_user, card_title, card_content, pronunciation_language,
        description,
        tag_names=params.get('tags')
    )
    return jsonify({'result': 'success'})


@deck_api.route('/create_image_card', methods=['POST'])
@auth_token_required
@dict_to_response
def create_image_card():
    deck_manager = current_app.managers.deck_manager
    params = request.json

    card_title = params.get('card_title')
    description = params.get('card_description', '')
    s3_file_name = params.get('s3_file_name')
    image_x = params.get('image_x')
    image_y = params.get('image_y')
    image_width = params.get('image_width')
    image_height = params.get('image_height')

    card = deck_manager.create_image_card(
        current_user, card_title, s3_file_name, description,
        image_x, image_y, image_width, image_height,
        tag_names=params.get('tags'),
        image_scale=params.get('image_scale'),
    )
    return jsonify({
        'result': 'success',
        'created_card_id': card.id
    })


@deck_api.route('/edit_image_card', methods=['POST'])
@auth_token_required
@dict_to_response
def edit_image_card():
    deck_manager = current_app.managers.deck_manager
    params = request.json

    card = deck_manager.edit_image_card(
        user=current_user,
        card_id=params.get('card_id'),
        s3_file_name=params.get('s3_file_name'),
        name=params.get('card_title'),
        description=params.get('card_description', ''),
        x_position=params.get('image_x'),
        y_position=params.get('image_y'),
        width=params.get('image_width'),
        height=params.get('image_height'),
        tag_names=params.get('tags'),
        scale=params.get('image_scale')
    )
    return card.to_dict()


@deck_api.route('/create_video_card', methods=['POST'])
@auth_token_required
@dict_to_response
def create_video_card():
    deck_manager = current_app.managers.deck_manager
    params = request.json

    card_title = params.get('card_title')
    description = params.get('card_description', '')
    s3_file_name = params.get('s3_file_name')
    thumbnail_url = params.get('thumbnail_url')

    card = deck_manager.create_video_card(
        current_user, card_title, s3_file_name, thumbnail_url, description,
        tag_names=params.get('tags'),
        scale=params.get('scale'),
        video_length=params.get('video_length')
    )
    return jsonify({
        'result': 'success',
        'created_card_id': card.id
    })


@deck_api.route('/edit_video_card', methods=['POST'])
@auth_token_required
@dict_to_response
def edit_video_card():
    deck_manager = current_app.managers.deck_manager
    params = request.json
    card = deck_manager.edit_video_card(
        user=current_user,
        card_id=params.get('card_id'),
        name=params.get('card_title'),
        description=params.get('card_description', ''),
        s3_file_name=params.get('s3_file_name'),
        thumbnail_url=params.get('thumbnail_url'),
        tag_names=params.get('tags'),
        scale=params.get('scale'),
        video_length=params.get('video_length')
    )
    return card.to_dict()


@deck_api.route('/generate_image_upload_params', methods=['POST'])
@auth_token_required
def generate_image_upload_params():
    deck_manager = current_app.managers.deck_manager
    params = request.json
    file_name = params.get('file_name')

    try:
        return jsonify({
            'result': deck_manager.generate_image_upload_params(file_name)
        })
    except Exception as e:
        # TODO
        # report to sentry
        print '%s: %s' % (e.__class__.__name__, e.message)
        return jsonify({'error': 'unknown_error'}), 400


@deck_api.route('/generate_video_upload_params', methods=['POST'])
@auth_token_required
def generate_video_upload_params():
    deck_manager = current_app.managers.deck_manager
    params = request.json
    file_name = params.get('file_name')

    try:
        return jsonify({
            'result': deck_manager.generate_video_upload_params(file_name)
        })
    except Exception as e:
        # TODO
        # report to sentry
        print '%s: %s' % (e.__class__.__name__, e.message)
        return jsonify({'error': 'unknown_error'}), 400


@deck_api.route('/get_created_cards', methods=['GET'])
@auth_token_required
def get_created_cards():
    deck_manager = current_app.managers.deck_manager
    try:
        darft_cards = deck_manager.get_cards_for_drafts(current_user)
        return jsonify({
            'created': [
                card.to_dict(user=current_user) for card in darft_cards
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

        # TODO
        # report to sentry
        print '%s: %s' % (e.__class__.__name__, e.message)
        return jsonify({'error': 'unknown_error'}), 400


@deck_api.route('/create_deck', methods=['POST'])
@auth_token_required
@dict_to_response
def create_deck():
    deck_manager = current_app.managers.deck_manager
    params = request.json

    deck_title = params.get('deck_title')
    card_ids = params.get('card_ids')
    is_ask_mode_enabled = params.get('is_ask_mode_enabled', False)
    deck_format = params.get('format', '')
    tag_names = params.get('tags', [])
    deck_manager.create_deck(
        current_user,
        deck_title,
        card_ids,
        False,
        is_ask_mode_enabled=is_ask_mode_enabled,
        deck_format=deck_format,
        tag_names=tag_names,
    )
    return jsonify({'result': 'success'})


@deck_api.route('/delete_cards', methods=['POST'])
@auth_token_required
def delete_cards():
    deck_manager = current_app.managers.deck_manager
    params = request.json
    try:
        card_ids = params.get('card_ids')
        deck_manager.delete_cards(current_user, card_ids)
        return jsonify({'result': 'success'})
    except Exception as e:
        # TODO
        # report to sentry
        print '%s: %s' % (e.__class__.__name__, e.message)
        return jsonify({'error': 'unknown_error'}), 400


@deck_api.route('/copy_cards', methods=['POST'])
@auth_token_required
@dict_to_response
def copy_cards():
    deck_manager = current_app.managers.deck_manager
    params = request.json
    try:
        card_ids = params.get('card_ids')
        deck_manager.copy_cards(current_user, card_ids)
        return jsonify({'result': 'success'})
    except Exception as e:
        # TODO
        # report to sentry
        print '%s: %s' % (e.__class__.__name__, e.message)
        return jsonify({'error': 'unknown_error'}), 400


@deck_api.route('/copy_card', methods=['POST'])
@auth_token_required
@dict_to_response
def copy_card():
    deck_manager = current_app.managers.deck_manager
    params = request.json
    new_card = deck_manager.copy_card(
        user=current_user,
        card_id=params['card_id']
    )
    return new_card.to_dict()


@deck_api.route('/publish_decks', methods=['POST'])
@auth_token_required
def publish_decks():
    deck_manager = current_app.managers.deck_manager
    params = request.json
    try:
        card_ids = params.get('card_ids')
        publish = params.get('publish')
        deck_manager.publish_decks(current_user, card_ids, publish)
        return jsonify({'result': 'success'})
    except Exception as e:
        # TODO
        # report to sentry
        print '%s: %s' % (e.__class__.__name__, e.message)
        return jsonify({'error': 'unknown_error'}), 400


@deck_api.route('/edit_deck', methods=['POST'])
@auth_token_required
@dict_to_response
def edit_deck():
    deck_manager = current_app.managers.deck_manager
    params = request.json

    deck_id = params.get('deck_id')
    card_ids = params.get('card_ids')
    deck_manager.edit_deck(
        current_user,
        deck_id,
        card_ids,
        tag_names=params.get('tags')
    )
    return jsonify({'result': 'success'})


@deck_api.route('/get_image_search_urls', methods=['POST'])
def get_image_search_urls():
    deck_manager = current_app.managers.deck_manager
    params = request.json
    try:
        search_key = params.get('search_key')
        return jsonify({
            'search_key': search_key,
            'urls': deck_manager.get_image_search_urls(search_key)
        })
    except Exception as e:
        # TODO
        # report to sentry
        print '%s: %s' % (e.__class__.__name__, e.message)
        return jsonify({'error': 'unknown_error'}), 400


@deck_api.route('/like_card', methods=['POST'])
@auth_token_required
def like_card():
    deck_manager = current_app.managers.deck_manager
    params = request.json
    try:
        card_id = params.get('card_id')
        deck_manager.like_card(current_user, card_id)
        return jsonify({'result': 'success'})
    except Exception as e:
        # TODO
        # report to sentry
        print '%s: %s' % (e.__class__.__name__, e.message)
        return jsonify({'error': 'unknown_error'}), 400


@deck_api.route('/like_comment', methods=['POST'])
@auth_token_required
@dict_to_response
def like_comment():
    deck_manager = current_app.managers.deck_manager
    params = request.json
    deck_manager.like_comment(
        user=current_user,
        comment_id=params['comment_id']
    )
    return {}


@deck_api.route('/convert_card_to_deck', methods=['POST'])
@auth_token_required
@dict_to_response
def convert_card_to_deck():
    deck_manager = current_app.managers.deck_manager
    params = request.json
    deck = deck_manager.convert_card_to_deck(
        user=current_user,
        card_id=params['card_id']
    )
    return deck.to_dict()


@deck_api.route('/unlike_comment', methods=['POST'])
@auth_token_required
@dict_to_response
def unlike_comment():
    deck_manager = current_app.managers.deck_manager
    params = request.json
    deck_manager.unlike_comment(
        user=current_user,
        comment_id=params['comment_id']
    )
    return {}


@deck_api.route('/unlike_card', methods=['POST'])
@auth_token_required
def unlike_card():
    deck_manager = current_app.managers.deck_manager
    params = request.json
    try:
        card_id = params.get('card_id')
        deck_manager.unlike_card(current_user, card_id)
        return jsonify({'result': 'success'})
    except Exception as e:
        # TODO
        # report to sentry
        print '%s: %s' % (e.__class__.__name__, e.message)
        return jsonify({'error': 'unknown_error'}), 400


@deck_api.route('/move_card', methods=['POST'])
@auth_token_required
@dict_to_response
def move_card():
    deck_manager = current_app.managers.deck_manager
    params = request.json
    card_ids = params.get('card_ids')
    move_to = params.get('move_to')
    deck_manager.move_card(current_user, card_ids, move_to)
    return {'result': 'success'}


@deck_api.route('/add_comment', methods=['POST'])
@auth_token_required
@dict_to_response
def add_comment():
    deck_manager = current_app.managers.deck_manager
    params = request.json
    comment = deck_manager.add_comment(
        user=current_user,
        content=params.get('comment_content'),
        card_id=params.get('card_id'),
        comment_id=params.get('comment_id'),
    )
    return jsonify({
        'result': 'success',
        'comment': comment.to_dict()
    })


@deck_api.route('/change_order', methods=['POST'])
@auth_token_required
@dict_to_response
def change_order():
    deck_manager = current_app.managers.deck_manager
    params = request.json
    try:
        deck_manager.change_order(
            user=current_user,
            card_id=params.get('card_id'),
            position=params.get('position'),
        )
    except Exception as ex:
        return jsonify({'result': 'error', 'message': str(ex)})
    return {'result': 'success'}


@deck_api.route('/get_card', methods=['POST'])
@auth_token_required
def get_card():
    deck_manager = current_app.managers.deck_manager
    params = request.json
    try:
        card_id = params.get('card_id')
        return jsonify({
            'card': deck_manager.get_card(card_id).to_dict(current_user)
        })
    except Exception as e:
        # TODO
        # report to sentry
        print '%s: %s' % (e.__class__.__name__, e.message)
        return jsonify({'error': 'unknown_error'}), 400


@deck_api.route('/view_card', methods=['POST'])
@auth_token_required
@dict_to_response
def view_card():
    deck_manager = current_app.managers.deck_manager
    params = request.json
    deck_manager.view_card(
        user=current_user,
        card_id=params['card_id']
    )
    return {}


@deck_api.route('/test_error_handling', methods=['GET'])
@dict_to_response
def test_error_handling():
    return test_error_handling_process()


def test_error_handling_process():
    return {}
