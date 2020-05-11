from flask import Blueprint, current_app, request
from flask_security.decorators import auth_token_required
from flask_security.core import current_user
from app.api.utils import dict_to_response
from app import app_json_coder as coder
from app import answers


ask_api = Blueprint('ask', __name__)


@ask_api.route('/add_mode', methods=['POST'])
@auth_token_required
@dict_to_response
def add_mode():
    from lib.models import card as card_module
    ask_manager = current_app.managers.ask_manager
    params = request.json
    deck_id = params['deck_id']
    deck_format = params.get('format', '')
    is_ask_mode_enabled = params.get('is_ask_mode_enabled', False)
    asked_user_ids = params.get('asked_user_ids', [])
    initial_prize = params.get('initial_prize', 0)
    prize_to_join = params.get('prize_to_join', 0)
    distribution_for = params.get('distribution_for')
    distribution_rule = params.get(
        'distribution_rule',
        card_module.DISTRIBUTION_RULE_SPLIT_PROPORTIONALLY
    )
    evaluation_start_dt = coder.decode_datetime(
        params.get('evaluation_start_dt')
    )
    evaluation_end_dt = coder.decode_datetime(params.get('evaluation_end_dt'))
    tags = params.get('tags')
    deck = ask_manager.add_mode(
        deck_id=deck_id,
        deck_format=deck_format,
        is_ask_mode_enabled=is_ask_mode_enabled,
        asked_user_ids=asked_user_ids,
        initial_prize=initial_prize,
        prize_to_join=prize_to_join,
        distribution_for=distribution_for,
        distribution_rule=distribution_rule,
        evaluation_start_dt=evaluation_start_dt,
        evaluation_end_dt=evaluation_end_dt,
        tag_names=tags
    )
    return {'result': 'success', 'deck': answers.Card(deck).to_dict()}


@ask_api.route('/give_card_to_deck', methods=['POST'])
@auth_token_required
@dict_to_response
def give_card_to_deck():
    ask_manager = current_app.managers.ask_manager
    params = request.json

    deck_id = params['deck_id']
    card_id = params['card_id']
    answer_visibility = params.get('visibility')
    viewer_ids = params.get('viewer_ids')
    deck = ask_manager.give_card_to_deck(
        deck_id, card_id, viewer_ids,
        answer_visibility=answer_visibility, tag_names=params.get('tags')
    )
    return {'result': 'success', 'deck': answers.Card(deck).to_dict()}


@ask_api.route('/give_card_to_deck_v2', methods=['POST'])
@auth_token_required
@dict_to_response
def give_card_to_deck_v2():
    ask_manager = current_app.managers.ask_manager
    params = request.json

    deck_id = params['deck_id']
    card_id = params['card_id']

    answer_visibility = params.get('visibility')
    viewer_ids = params.get('viewer_ids')

    deck = ask_manager.give_card_to_deck_v2(
        deck_id, card_id, current_user, viewer_ids=viewer_ids,
        answer_visibility=answer_visibility, tag_names=params.get('tags')
    )
    return {'result': 'success', 'deck': deck.to_dict(current_user)}


@ask_api.route('/revoke_card_from_deck', methods=['POST'])
@auth_token_required
@dict_to_response
def revoke_card_from_deck():
    ask_manager = current_app.managers.ask_manager
    params = request.json

    card_id = params['card_id']
    deck = ask_manager.revoke_card_from_deck(card_id)
    return {'deck': answers.Card(deck).to_dict()}


@ask_api.route('/revoke_card_from_deck_v2', methods=['POST'])
@auth_token_required
@dict_to_response
def revoke_card_from_deck_v2():
    ask_manager = current_app.managers.ask_manager
    params = request.json

    card_id = params['card_id']
    deck = ask_manager.revoke_card_from_ask(current_user, card_id)
    return {'deck': deck.to_dict(current_user)}


@ask_api.route('/join_ask', methods=['POST'])
@auth_token_required
@dict_to_response
def join_ask():
    ask_manager = current_app.managers.ask_manager
    params = request.json

    deck_id = params['deck_id']
    custom_join_prize = params.get('custom_join_prize', None)
    deck = ask_manager.join_ask(
        deck_id, [current_user.id], custom_join_prize=custom_join_prize
    )
    return {'result': 'success', 'deck': answers.Card(deck).to_dict()}


@ask_api.route('/unjoin_ask', methods=['POST'])
@auth_token_required
@dict_to_response
def unjoin_ask():
    ask_manager = current_app.managers.ask_manager
    params = request.json

    deck_id = params['deck_id']
    user_id = current_user.id
    deck = ask_manager.unjoin_ask(deck_id, user_id)
    return {'result': 'success', 'deck': answers.Card(deck).to_dict()}


@ask_api.route('/end_evaluation_period', methods=['POST'])
@auth_token_required
@dict_to_response
def end_evaluation_period():
    ask_manager = current_app.managers.ask_manager
    params = request.json
    deck_id = params['deck_id']
    deck = ask_manager.end_evaluation_period(deck_id)
    return {'deck': answers.Card(deck).to_dict()}


@ask_api.route('/get_sponsors', methods=['GET'])
@auth_token_required
@dict_to_response
def get_sponsors():
    ask_manager = current_app.managers.ask_manager
    params = request.json
    deck_id = params['deck_id']
    urc_s = ask_manager.get_sponsors(deck_id)
    sponsors = []
    for it in urc_s:
        res = it.user.get_extended_data()
        res['contribution'] = it.contribution
        sponsors.append(res)
    return {'sponsors': sponsors}


@ask_api.route('/get_winners', methods=['GET'])
@auth_token_required
@dict_to_response
def get_winners():
    ask_manager = current_app.managers.ask_manager
    params = request.args
    deck_id = params['deck_id']
    urc_s = ask_manager.get_winners(deck_id)
    winners = []
    for it in urc_s:
        res = it.user.get_extended_data()
        res['likes'] = it.total_likes
        res['prize'] = it.prize
        winners.append(res)
    total_likes_for_deck = sum([it.total_likes for it in urc_s])
    for it in winners:
        res['likes_relative'] = res['likes'] * 100 / total_likes_for_deck
    return {'winners': winners, 'total_likes': total_likes_for_deck}
