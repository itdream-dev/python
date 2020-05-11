# -*- coding: utf-8 -*-
from config import Ivysaur
from lib.registry import get_registry
from lib.models.user import User, UserSkill
from lib.models.skill import Skill
from lib.models.confirmation_email import ConfirmationEmail
from sqlalchemy import func, and_
from sqlalchemy.orm import join
from sqlalchemy.exc import IntegrityError
import lib.exceptions as exceptions
import arrow
import uuid
import random
import string


def generate_verification_code():
    return str(uuid.uuid4())


class UserRepo(object):

    def __init__(self):
        self.db = get_registry()['DB']

    def set_default_username(self, user):
        default_username = '%s%s' % (user.first_name.lower(),
                                     user.last_name.lower())
        try:
            user.username = default_username
            self.db.session.merge(user)
            self.db.session.commit()
            return user
        except:
            self.db.session.rollback()
            count = 0
            while count < 100000:
                try:
                    user.username = default_username + str(count)
                    self.db.session.merge(user)
                    self.db.session.commit()
                    return user
                except:
                    self.db.session.rollback()
                    count += 1
                    pass

    def create_inactive_user(self, username, email):
        user = User(
            username=username,
            email=email,
            active=False,
            verification_code=generate_verification_code()
        )
        self.db.session.add(user)
        return user

    def get_user(self, user_id):
        return User.query.filter(User.id == user_id).first()

    def get_user_by_email(self, email):
        return User.query.filter(User.email == email).first()

    def edit_profile(self, user):
        try:
            self.db.session.merge(user)
            self.db.session.commit()
        except IntegrityError:
            raise exceptions.UsernameAlreadyExists

    def get_user_skill(self, user_id, skill_id):
        return UserSkill.query.filter(
            UserSkill.user_id == user_id,
            UserSkill.skill_id == skill_id
        ).first()

    def get_tutors_with_skill(self, user, search_key):
        search_key = [sk.lower() for sk in search_key]
        query_filter = [
            func.lower(Skill.name).like("%" + sk + "%")
            for sk in search_key
        ]

        skill_ids = [
            skill.id for skill in Skill.query.filter(and_(*query_filter)).all()
        ]
        if not skill_ids:
            return []

        if Ivysaur.Config.RESTRICT_EXPERTS:
            userskills_users = self.db.session.query(
                UserSkill, User
            ).select_from(
                join(UserSkill, User)
            ).filter(
                UserSkill.skill_id.in_(skill_ids),
                User.email.in_(Ivysaur.Config.SEARCHABLE_EXPERTS)
                # UserSkill.user_id != user.id
            ).all()
        else:
            userskills_users = self.db.session.query(
                UserSkill, User
            ).select_from(
                join(UserSkill, User)
            ).filter(
                UserSkill.skill_id.in_(skill_ids),
                # UserSkill.user_id != user.id
            ).all()

        return [
            dict(
                userskills_user[1].get_basic_data().items() +
                userskills_user[0].to_dict().items()
            ) for userskills_user in userskills_users
        ]

    def get_usernames(self, search_key):
        return User.query.filter(
            User.username.like("%" + search_key + "%")
        ).order_by(User.username).all()

    def get_user_from_username(self, username):
        return User.query.filter(
            User.username == username
        ).first()

    def get_confirmation_email(self, email):
        return ConfirmationEmail.query.filter(
            ConfirmationEmail.id == email
        ).first()

    def _generate_confirmation_code(self):
        return ''.join(random.choice(string.digits) for i in range(6))

    def refresh_confirmation_code(self, confirmation_email):
        confirmation_code = self._generate_confirmation_code()
        confirmation_email.confirmation_code = confirmation_code
        confirmation_email.updated_at = arrow.utcnow().timestamp
        self.db.session.merge(confirmation_email)
        self.db.session.commit()
        return confirmation_email

    def create_new_confirmation_email(self, email, username, year):
        now = arrow.utcnow().timestamp
        confirmation_code = self._generate_confirmation_code()
        confirmation_email = ConfirmationEmail(
            id=email,
            confirmation_code=confirmation_code,
            created_at=now,
            updated_at=now,
            username=username,
            year=year
        )
        self.db.session.add(confirmation_email)
        self.db.session.commit()
        return confirmation_email

    def increment_verification_attempt_count(self, confirmation_email):
        confirmation_email.attempts += 1
        self.db.session.add(confirmation_email)
        self.db.session.commit()

    def get_confirmation_email_from_username(self, username):
        return ConfirmationEmail.query.filter(
            ConfirmationEmail.username == username
        ).first()
