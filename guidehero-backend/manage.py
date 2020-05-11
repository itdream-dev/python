import os
import sys
import arrow

from app.ivysaur_app import create_app
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from lib.registry import get_registry

ivysaur_env = os.environ.get('IVYSAUR_ENV')
if not ivysaur_env:
    print "please set IVYSAUR_ENV environment var"
    sys.exit(1)

app = create_app(ivysaur_env)
db = get_registry()['DB']

from lib.models.role import Role  # NOQA
from lib.models.user import User  # NOQA
from lib.models.device import Device  # NOQA
from lib.models.base_folder import BaseFolder  # NOQA
from lib.models.base_deck import BaseDeck  # NOQA
from lib.models.base_set import BaseSet  # NOQA
from lib.models.base_card import BaseCard  # NOQA
from lib.models.base_card_content import BaseCardContent  # NOQA
from lib.models.card import Card  # NOQA
from lib.models.card_likes import CardLikes  # NOQA
from lib.models.card_comments import CardComments  # NOQA
from lib.models.notification import Notification # NOQA
from lib.models.confirmation_email import ConfirmationEmail  # NOQA


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def create_roles():
    """Creates the roles."""
    user_datastore = get_registry()['USER_DATASTORE']
    user_datastore.find_or_create_role(name='admin', description='Admin')
    user_datastore.find_or_create_role(name='user', description='User')
    db.session.commit()
    print "successfully created roles: " + arrow.utcnow().format(
        'YYYY-MM-DD HH:mm:ss ZZ'
    )


@manager.command
def create_test_user():
    """Creates the roles."""
    user_datastore = get_registry()['USER_DATASTORE']
    email = 'john.smith@veles-soft.com'
    user_data = {
        'email': email,
        'password': '12345',
        'silver_points': 30000
    }
    user = user_datastore.create_user(**user_data)
    db.session.commit()
    user_datastore.add_role_to_user(email, 'user')
    db.session.commit()


@manager.command
def create_test_cards():
    """Creates the roles."""
    from lib.models.card import Card
    from lib.models.user import User
    u = User.query.filter(User.email == 'john.smith@veles-soft.com').first()
    deck = Card(type=Card.DECK, creator=u)
    card1 = Card(type=Card.TEXT, creator=u, parent=deck)
    card2 = Card(type=Card.TEXT, creator=u, parent=deck)

    db.session.add(card1)
    db.session.add(card2)
    db.session.commit()
    print(card1.id)
    print(card2.id)


@manager.command
def update_cards():
    """Creates the roles."""
    from lib.models.card import Card
    import arrow
    now = arrow.utcnow().timestamp
    for c in Card.query.all():
        c.created_at = now
    db.session.commit()
    print('Done')


if __name__ == "__main__":
    manager.run()
