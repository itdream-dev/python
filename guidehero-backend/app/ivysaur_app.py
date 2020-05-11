# -*- coding: utf-8 -*-
from opentok import OpenTok
from lib.registry import get_registry
from config import Ivysaur
from config.app_config import init_config
from flask import Flask, render_template
from flask.ext.security import SQLAlchemyUserDatastore, Security
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mail import Mail
from app.app_json_coder import AppJSONEncoder
from app.request_logger_middleware import RequestLoggerMiddleware
import logging


def _initialize_flask_app():
    return Flask(__name__, static_url_path=None, template_folder='')


def _register_version_and_log(app):
    from version import version
    from log import log
    app.add_url_rule('/version.txt', 'version', version)
    app.add_url_rule('/log.txt', 'log', log)
    return app


def _register_blueprints(app):
    from home import home
    app.register_blueprint(home)

    from api.auth_api import auth_api
    from api.deck_api import deck_api
    from api.notification_api import notification_api
    from api.account_api import account_api
    from api.ask_api import ask_api
    from api.points_api import points_api

    app.register_blueprint(auth_api, url_prefix='/api/v1/auth')
    app.register_blueprint(deck_api, url_prefix='/api/v1/deck')
    app.register_blueprint(notification_api, url_prefix='/api/v1/notification')
    app.register_blueprint(account_api, url_prefix='/api/v1/account')
    app.register_blueprint(ask_api, url_prefix='/api/v1/deck')
    app.register_blueprint(points_api, url_prefix='/api/v1/points')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('static/404.html'), 404

    return app


def _initialize_managers(app):
    from app.managers.account_manager import AccountManager
    from app.managers.deck_manager import DeckManager
    from app.managers.notification_manager import NotificationManager
    from app.managers.ask_manager import AskManager
    from app.managers.points_manager import PointsManager

    class __ManagerContainer:
        pass
    app.managers = __ManagerContainer()
    app.managers.account_manager = AccountManager()
    app.managers.deck_manager = DeckManager()
    app.managers.notification_manager = NotificationManager()
    app.managers.ask_manager = AskManager()
    app.managers.points_manager = PointsManager()
    return app


def _configure_logging(app):
    app.logger.addHandler(logging.getLogger('ivysaur'))
    app.logger_name = 'ivysaur'
    return app


def _initialize_models():
    '''
    Some models are not loaded during app initialization and not detected by
    alembic because of this.
    This is temporary solution to load missed model.
    Normal solution is to create repo for each goup of  models and initialize
    the ropes in create_app method
    '''
    from lib.models.card_role_permission import CardRolePermission
    from lib.models.card_permission import CardPermission
    from lib.models.search import Search
    from lib.models.call import Call
    from lib.models.expert_request import ExpertRequest
    from lib.models.transfer import Transfer
    return [
        CardRolePermission, CardPermission, Search, Call, ExpertRequest,
        Transfer
    ]


def create_app(env):
    init_config(env)
    app = _initialize_flask_app()
    app.wsgi_app = RequestLoggerMiddleware(app.wsgi_app)
    app = _configure_logging(app)
    app.config.from_object(Ivysaur.Config)
    app = _register_blueprints(app)
    app = _register_version_and_log(app)

    db = SQLAlchemy(app, session_options={"autoflush": False})
    reg = get_registry()
    reg['DB'] = db

    mail = Mail(app)
    reg['MAIL'] = mail

    reg['TOKBOX'] = OpenTok(
        Ivysaur.Config.TOKBOX_API_KEY, Ivysaur.Config.TOKBOX_API_SECRET
    )

    from lib.models.user import User
    from lib.models.role import Role

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    Security(app, user_datastore)

    from lib.repo.user_repo import UserRepo
    from lib.repo.device_repo import DeviceRepo
    from lib.repo.deck_repo import DeckRepo
    from lib.repo.notification_repo import NotificationRepo
    from lib.repo.ask_repo import AskRepo

    # see comment for this method
    _initialize_models()

    reg['USER_DATASTORE'] = user_datastore
    reg['USER_REPO'] = UserRepo()
    reg['DEVICE_REPO'] = DeviceRepo()
    reg['DECK_REPO'] = DeckRepo()
    reg['NOTIFICATION_REPO'] = NotificationRepo()
    reg['ASK_REPO'] = AskRepo()

    app = _initialize_managers(app)
    app.json_encoder = AppJSONEncoder
    return app
