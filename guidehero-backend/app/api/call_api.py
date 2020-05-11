# # -*- coding: utf-8 -*-
# from flask import Blueprint, jsonify, current_app, request
# from flask_security.core import current_user
# from flask_security.decorators import auth_token_required
# from lib.registry import get_registry
# import logging
# _logger = logging.getLogger(__name__)

# call_api = Blueprint('call', __name__)


# def get_opentok():
#     return get_registry()['TOKBOX']


# @call_api.route("/initiate_call", methods=['POST'])
# @auth_token_required
# def initiate_call():
#     try:
#         params = request.json
#         user_id_2 = params.get('id_to_call')

#         call_manager = current_app.managers.call_manager
#         result = call_manager.start_session(current_user, user_id_2)
#         return jsonify(result)
#     except Exception as e:
#         # TODO
#         # report to sentry
#         _logger.exception(e)
#         return jsonify({'error': 'unknown_error'}), 400


# @call_api.route("/get_pending_call", methods=['GET'])
# @auth_token_required
# def get_pending_call():
#     try:
#         call_manager = current_app.managers.call_manager
#         pending_call = call_manager.get_pending_call(current_user)
#         if not pending_call:
#             return jsonify({})
#         return jsonify(pending_call)
#     except Exception as e:
#         # TODO
#         # report to sentry
#         _logger.exception(e)
#         return jsonify({'error': 'unknown_error'}), 400


# @call_api.route("/report_connected", methods=['POST'])
# @auth_token_required
# def report_connected():
#     try:
#         params = request.json
#         session_id = params.get('session_id')
#         call_manager = current_app.managers.call_manager
#         call_manager.report_connected(session_id)
#         return jsonify({'result': 'success'})
#     except Exception as e:
#         # TODO
#         # report to sentry
#         _logger.exception(e)
#         return jsonify({'error': 'unknown_error'}), 400


# @call_api.route("/report_ended", methods=['POST'])
# @auth_token_required
# def report_ended():
#     try:
#         params = request.json
#         session_id = params.get('session_id')
#         call_manager = current_app.managers.call_manager
#         call_manager.report_ended(session_id)
#         return jsonify({'result': 'success'})
#     except Exception as e:
#         # TODO
#         # report to sentry
#         _logger.exception(e)
#         return jsonify({'error': 'unknown_error'}), 400
