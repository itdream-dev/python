# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request, current_app
from flask_security.core import current_user
from flask_security.decorators import auth_token_required
import logging
_logger = logging.getLogger(__name__)

tutor_api = Blueprint('tutor', __name__)


@tutor_api.route('/search_tutors', methods=['POST'])
@auth_token_required
def search_tutors():
    params = request.json

    try:
        tutor_manager = current_app.managers.tutor_manager
        search_key = params.get('search', '')

        tutors = tutor_manager.search_tutors(current_user, search_key)

        return jsonify({
            'tutors': [
                '%s %s' % (tutor.first_name, tutor.last_name)
                for tutor in tutors
            ]
        })

    except Exception as e:
        # TODO
        # report to sentry
        _logger.exception(e)
        return jsonify({'error': 'unknown_error'}), 400
