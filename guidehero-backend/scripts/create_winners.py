# -*- coding: utf-8 -*-
import os
import sys
import json

_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(_root)


from app.ivysaur_app import create_app
ivysaur_env = os.environ.get('IVYSAUR_ENV')
if not ivysaur_env:
    print "please set IVYSAUR_ENV environment var"
    sys.exit(1)

create_app(ivysaur_env)


from lib.registry import get_registry
from lib.models.user import User
from lib.models.card import Card
from lib.models import card as card_module
from lib.models.user_role_card import UserRoleCard
from lib.models import card_role

if __name__ == '__main__':
    db = get_registry()['DB']

    deck = Card(evaluation_period_status=card_module.EVALUATION_PERIOD_STATUS_DONE)
    db.session.add(deck)
    user = User()
    db.session.add(user)
    ucr = UserRoleCard(user=user, card=deck, role_id=card_role.CardRole.ASKED, total_likes=10, prize=100)
    db.session.add(ucr)

    db.session.commit()
    print(deck.id)
