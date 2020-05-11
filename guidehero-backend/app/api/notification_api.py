# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, current_app
from flask_security.core import current_user
from flask_security.decorators import auth_token_required
import logging
_logger = logging.getLogger(__name__)

notification_api = Blueprint('notification', __name__)


@notification_api.route('/get_notifications', methods=['GET'])
@auth_token_required
def get_notifications():
    try:
        notifications = (
            current_app.managers.notification_manager.get_notifications(
                current_user)
        )
        return jsonify({
            'notifications': [
                notification.to_dict() for notification in notifications
            ]
        })
    except Exception as e:
        # TODO
        # report to sentry
        _logger.exception(e)
        return jsonify({'error': 'unknown_error'}), 400


@notification_api.route('/opened_notification', methods=['POST'])
@auth_token_required
def opened_notification():
    try:
        current_app.managers.notification_manager.opened_notification(
            current_user
        )
        return jsonify({'result': 'success'})
    except Exception as e:
        # TODO
        # report to sentry
        _logger.exception(e)
        return jsonify({'error': 'unknown_error'}), 400
