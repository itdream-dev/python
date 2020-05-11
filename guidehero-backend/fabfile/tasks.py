import gspread
import os
import sys

_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(_root)

from fabric.api import task
from oauth2client.service_account import ServiceAccountCredentials
from lib.registry import get_registry


CRED_FILE_PATH = (
    './fabfile/GuideHero-418dcdd7bfc2.json'
)
SPREADSHEET_ID = '1pXq_Bu-1UWFOlKsJeq5q9f7yYfgLbFUm0lrK09RZoh8'
CHRIS = 'Chris Yamamoto'

JP = 'ja-JP'
EN = 'en-US'


@task
def add_from_gspreadsheet():
    _init_app()
    sh = _get_worksheet()
    db = get_registry()['DB']
    deck_repo = get_registry()['DECK_REPO']

    deck_repo.truncate_tables()

    folder1 = None
    folder2 = None
    deck = None
    for row in sh.get_all_values()[1:]:
        if not any(row):
            continue

        # root folder
        if row[0]:
            folder1 = deck_repo.add_folder(
                row[0],
                CHRIS,
                row[1],
                root_level=True
            )
            continue

        # next layer of folders
        if row[1]:
            folder2 = deck_repo.add_folder(
                row[1],
                CHRIS,
                row[2],
                root_level=False
            )
            folder1.folders.append(folder2)
            continue

        # deck
        if row[2]:
            deck = deck_repo.add_deck(
                row[2],
                CHRIS,
                row[3]
            )
            folder2.decks.append(deck)
            continue

        new_set = deck_repo.add_set(row[3], CHRIS)
        deck.content.append(new_set)

        # card 1
        card1 = deck_repo.add_card(row[3])
        new_set.content.append(card1)
        card_content1_1 = deck_repo.add_card_content(
            'text', row[3], JP
        )
        card1.content.append(card_content1_1)
        card_content1_2 = deck_repo.add_card_content(
            'text', row[4], EN
        )
        card1.content.append(card_content1_2)
        card_content1_3 = deck_repo.add_card_content(
            'audio', row[3], JP
        )
        card1.content.append(card_content1_3)

        # card 2
        card2 = deck_repo.add_card(row[5])
        new_set.content.append(card2)
        card_content2 = deck_repo.add_card_content(
            'text', row[5], EN
        )
        card2.content.append(card_content2)

        if row[6]:
            # card 3
            card3 = deck_repo.add_card('image')
            new_set.content.append(card3)
            card_content3 = deck_repo.add_card_content(
                'image', row[6], EN
            )
            card3.content.append(card_content3)

        if row[7]:
            # card 4
            card4 = deck_repo.add_card('video')
            new_set.content.append(card4)
            card_content4 = deck_repo.add_card_content(
                'video', row[7], EN
            )
            card4.content.append(card_content4)

        if row[8]:
            # card 5
            card5 = deck_repo.add_card('example')
            new_set.content.append(card5)
            card_content5 = deck_repo.add_card_content(
                'web', row[8], EN
            )
            card5.content.append(card_content5)

    db.session.commit()


def _init_app():
    from app.ivysaur_app import create_app
    ivysaur_env = os.environ.get('IVYSAUR_ENV')
    if not ivysaur_env:
        print "please set IVYSAUR_ENV environment var"
        sys.exit(1)

    create_app(ivysaur_env)


def _get_worksheet():
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CRED_FILE_PATH, scope
    )
    gc = gspread.authorize(credentials)
    sh = gc.open_by_key(SPREADSHEET_ID)
    automated_worksheet = sh.worksheet("Sheet1")
    return automated_worksheet
