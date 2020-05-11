# -*- coding: utf-8 -*-
from flask import Blueprint
import logging
_logger = logging.getLogger(__name__)
home = Blueprint('home', __name__)


@home.route('/')
def index():
    return 'Success!'
