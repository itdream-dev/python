# -*- coding: utf-8 -*-
import os
import sys
import pprint

_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(_root)


from app.ivysaur_app import create_app
ivysaur_env = os.environ.get('IVYSAUR_ENV')
if not ivysaur_env:
    print "please set IVYSAUR_ENV environment var"
    sys.exit(1)

create_app(ivysaur_env)


if __name__ == '__main__':
    from lib.registry import get_registry
    card_id = raw_input('Card or Deck ID: ')
    deck_repo = get_registry()['DECK_REPO']
    card = deck_repo.get_card(card_id)
    if not card:
        print "Card or Deck Doesn't Exist"
        sys.exit()

    pprint.pprint(card.to_dict())
