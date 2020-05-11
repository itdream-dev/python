# -*- coding: utf-8 -*-
import arrow
from config import Ivysaur
from lib.registry import get_registry
import lib.exceptions as exceptions
from flask.ext.security.utils import encrypt_password
from sqlalchemy.exc import IntegrityError
from lib.linkedin import get_linkedin_data
from lib.facebook import get_facebook_verification_data
from lib.google import get_google_verification_data
from lib.models.skill import Skill
from lib.models.user import UserSkill
from flask_mail import Message
from lib.email import EmailHelper


class AccountManager(object):

    LINKEDIN = 'linkedin'
    FACEBOOK = 'facebook'
    GOOGLE = 'google'

    class CreateInactiveUserException(ValueError):
        pass

    def __init__(self):
        registry = get_registry()
        self.user_datastore = registry['USER_DATASTORE']
        self.db = registry['DB']
        self.device_repo = registry['DEVICE_REPO']
        self.user_repo = registry['USER_REPO']

    def _strip_email(self, email):
        at_split = email.split('@')
        username = at_split[0].split('+')[0].replace('.', '')
        return '%s@%s' % (username, at_split[-1])

    def _create_new_account(self, user_data, source=''):
        try:
            email = user_data['email']
            user_data['stripped_email'] = self._strip_email(email)
            user_data['password'] = encrypt_password(
                '%s%s%s' % (email,
                            source,
                            Ivysaur.Config.PASSWORD_PLACEHOLDER)
            )
            user_data['source'] = source
            user_data['confirmed_at'] = arrow.utcnow().timestamp
            user_data['silver_points'] = 1000

            user = self.user_datastore.create_user(**user_data)

            if email.endswith("@harvard.edu"):
                user.tier = "harvard"

            self.db.session.commit()
            self.user_datastore.add_role_to_user(email, 'user')
            self.db.session.commit()
            user = self.user_repo.set_default_username(user)
            return user
        except IntegrityError:
            raise exceptions.AccountExists()
        except:
            raise

    def verify_email(self, email, code):
        user = self.user_repo.get_user_by_email(email)
        if user is None:
            return ValueError('Can not find user with email={}'.format(email))

        if user.verification_code != code:
            return ValueError('Verification code does not match')

        user.verification_code = ''
        user.active = True
        self.db.session.commit()

    def create_inactive_account(self, username, email):
        user = self.user_repo.get_user_by_email(email)
        if user:
            raise self.CreateInactiveUserException('email_exists')

        user = self.user_repo.get_user_from_username(username)
        if user:
            raise self.CreateInactiveUserException('username_exists')

        if email.endswith("@noschool.edu"):
            raise self.CreateInactiveUserException('no_school')

        user = self.user_repo.create_inactive_user(username, email)
        self.db.session.commit()
        mail = get_registry()['MAIL']
        msg = Message(
            'Verification code for user: {} {}'.format(
                user.first_name, user.last_name
            ),
            sender=Ivysaur.Config.MAIL_USERNAME,
            recipients=[user.email])
        msg.html = u'Verification Code {}'.format(user.verification_code)
        mail.send(msg)
        return user

    def login_with_email(self, email):
        user = self.user_datastore.get_user(email)
        if not user:
            raise exceptions.UserDoesntExist()
        return user

    def login_with_linkedin(self, access_token):
        if not access_token:
            raise exceptions.MissingAccessToken()

        linkedin_data = get_linkedin_data(access_token)
        if not linkedin_data:
            raise exceptions.AuthenticationFailed()

        email = linkedin_data['email'].lower()
        user = self.user_datastore.get_user(email)

        if user:
            if (
                email.endswith("@harvard.edu") or
                email.endswith(".harvard.edu")
            ):
                user.tier = "harvard"
            for data_key, data_value in linkedin_data.iteritems():
                if data_value != getattr(user, data_key):
                    user.first_name = linkedin_data['first_name']
                    user.last_name = linkedin_data['last_name']
                    user.linkedin_profile = linkedin_data['linkedin_profile']
                    user.linkedin_headline = linkedin_data['linkedin_headline']
                    user.thumbnail_url = linkedin_data['thumbnail_url']
                    self.db.session.merge(user)
                    self.db.session.commit()
                    break

            return user

        user = self._create_new_account(linkedin_data, source=self.LINKEDIN)
        return user

    def add_skill(self, user, skill_name, level, price, details):
        skill = Skill.query.filter(
            Skill.name == skill_name
        ).first()

        if not skill:
            skill = Skill(name=skill_name)
            self.db.session.add(skill)

        user_skill = UserSkill.query.filter(
            UserSkill.user_id == user.id,
            UserSkill.skill_id == skill.id
        ).first()

        if user_skill:
            user_skill.level = level
            user_skill.price = price
            user_skill.details = details
            self.db.session.add(user_skill)

        else:
            user_skill = UserSkill(
                level=level,
                price=price,
                details=details
            )
            user_skill.skill = skill
            user.skills.append(user_skill)
            self.db.session.add(user)
        self.db.session.commit()

    def edit_skill(self, user, skill_id, level, price, details):

        user_skill = UserSkill.query.filter(
            UserSkill.user_id == user.id,
            UserSkill.skill_id == skill_id
        ).first()

        if not user_skill:
            raise exceptions.UserSkillDoesntExist()

        user_skill.level = level
        user_skill.price = price
        user_skill.details = details
        self.db.session.merge(user_skill)
        self.db.session.commit()

    def delete_user_skill(self, user, skill_id):
        UserSkill.query.filter(
            UserSkill.user_id == user.id,
            UserSkill.skill_id == skill_id
        ).delete()
        self.db.session.commit()

    def register_device(self, user, device_token, device_type):
        self.device_repo.register_device(user, device_token, device_type)

    def login_with_facebook(self, access_token):
        if not access_token:
            raise exceptions.MissingAccessToken()

        fb_data = get_facebook_verification_data(access_token)
        if not fb_data:
            raise exceptions.AuthenticationFailed()
        if not fb_data.get('verified'):
            raise exceptions.NotVerified()

        if not fb_data.get('email'):
            raise exceptions.NoEmailAccount()

        email = fb_data['email'].lower()
        user = self.user_datastore.get_user(email)
        if user:
            if fb_data.get('verified') and user.active is False:
                user.active = True
                self.db.session.commit()

        if user:
            if (
                email.endswith("@harvard.edu") or
                email.endswith(".harvard.edu")
            ):
                user.tier = "harvard"

            # updating photo
            user.thumbnail_url = fb_data['thumbnail_url']
            self.db.session.commit()

            return user

        del fb_data['verified']
        user = self._create_new_account(fb_data, source=self.FACEBOOK)
        return user

    def login_with_google(self, access_token):
        if not access_token:
            raise exceptions.MissingAccessToken()

        google_data = get_google_verification_data(access_token)
        if not google_data:
            raise exceptions.AuthenticationFailed()

        if not google_data.get('verified'):
            raise exceptions.NotVerified()

        email = google_data['email'].lower()
        user = self.user_datastore.get_user(email)

        if user:
            if (
                email.endswith("@harvard.edu") or
                email.endswith(".harvard.edu")
            ):
                user.tier = "harvard"
            return user

        del google_data['verified']
        user = self._create_new_account(google_data, source=self.GOOGLE)
        return user

    def edit_profile(self, user, first_name, last_name, username, bio):
        if user.first_name != first_name:
            user.first_name = first_name
        if user.last_name != last_name:
            user.last_name = last_name
        if user.username != username:
            user.username = username
        if user.bio != bio:
            user.bio = bio
        self.user_repo.edit_profile(user)
        return user

    def get_usernames(self, search_key):
        return self.user_repo.get_usernames(search_key)

    def get_user(self, user_id):
        return self.user_repo.get_user(user_id)

    def edit_user(self, user, **kwargs):
        for key, value in kwargs.items():
            setattr(user, key, value)
        self.db.session.commit()
        return user

    def get_user_points_summary(self, user):
        from sqlalchemy.sql import func
        from lib.models import transfer
        Transfer = transfer.Transfer

        _gv = lambda v: 0 if v is None else v
        q = self.db.session.query(
            func.sum(Transfer.silver_points).label('sum_silver_points'),
            func.sum(Transfer.gold_points).label('sum_gold_points'),
        ).filter(Transfer.user_to == user, Transfer.transaction_type != transfer.TYPES['purchase'].code)
        row = list(q)[0]
        cumulative_earnings = {'gold': _gv(row.sum_gold_points), 'silver': _gv(row.sum_silver_points)}

        q = self.db.session.query(
            func.sum(Transfer.silver_points).label('sum_silver_points'),
            func.sum(Transfer.gold_points).label('sum_gold_points'),
        ).filter(Transfer.user_to == user, Transfer.transaction_type == transfer.TYPES['purchase'].code)
        row = list(q)[0]
        points_purchased = {'gold': _gv(row.sum_gold_points), 'silver': _gv(row.sum_silver_points)}

        q = self.db.session.query(
            func.sum(Transfer.silver_points).label('sum_silver_points'),
            func.sum(Transfer.gold_points).label('sum_gold_points'),
        ).filter(Transfer.user_from == user)
        row = list(q)[0]
        points_used = {'gold': _gv(row.sum_gold_points), 'silver': _gv(row.sum_silver_points)}

        return {
            'total_points': {'silver': user.silver_points, 'gold': user.gold_points},
            'cumulative_earnings': cumulative_earnings,
            'points_purchased': points_purchased,
            'points_used': points_used
        }

    def adjust_silver_points(self, user_id, amount):
        user = self.get_user(user_id)
        user.silver_points += amount
        self.user_repo.edit_profile(user)
        return user

    def adjust_gold_points(self, user_id, amount):
        user = self.get_user(user_id)
        user.gold_points += amount
        self.user_repo.edit_profile(user)
        return user

    def follow_user(self, follower, following):
        follower.followings.append(following)
        self.db.session.commit()

    def _serialize_related_users(self, related_users, current_user):
        from lib.models.user import serialize_user_extended
        res = []
        for u in related_users:
            obj = serialize_user_extended(u)
            obj['follow_by_current_user'] = bool(
                [u1 for u1 in current_user.followings if u1.id == u.id]
            )
            obj['follow_current_user'] = bool(
                [u1 for u1 in current_user.followers if u1.id == u.id]
            )
            res.append(obj)
        return res

    def get_profile(self, user, current_user):
        from lib.models.user import serialize_user_extended

        cards = user.cards
        stats = {
            'total_likes': sum([len(c.liked_users) for c in cards]),
            'total_followers': len(user.followers),
            'total_followings': len(user.followings),
            'total_shared': 113,
            'total_points': {
                'silver': user.silver_points,
                'gold': user.gold_points
            }
        }
        user_info = serialize_user_extended(user)
        user_info.update({
            'follow_by_current_user': bool(current_user in user.followers),
            'follow_current_user': bool(current_user in user.followings),
        })
        return {
            'user_info': user_info,
            
            'stats': stats,
            'followers': self._serialize_related_users(user.followers, current_user),
            'followings': self._serialize_related_users(user.followings, current_user),
        }

    def unfollow_user(self, follower, following):
        follower.followings.remove(following)
        self.db.session.commit()

    def send_confirmation_email(self, email, username, year):
        if not email or not username or not year:
            raise exceptions.InvalidArguments
        confirmation_email = self.user_repo.get_confirmation_email(email)
        if confirmation_email and confirmation_email.verified:
            raise exceptions.EmailAlreadyRegistered
        if confirmation_email:
            confirmation_email = self.user_repo.refresh_confirmation_code(
                confirmation_email
            )
        else:
            if (
                self.user_repo.get_user_from_username(username) or
                self.user_repo.get_confirmation_email_from_username(username)
            ):
                raise exceptions.UsernameAlreadyExists
            confirmation_email = self.user_repo.create_new_confirmation_email(
                email, username, year
            )

        # send email
        EmailHelper().send_confirmation_email(confirmation_email)

    def resend_confirmation_email(self, email):
        if not email:
            raise exceptions.InvalidArguments
        confirmation_email = self.user_repo.get_confirmation_email(email)
        if confirmation_email and confirmation_email.verified:
            raise exceptions.EmailAlreadyRegistered
        if not confirmation_email:
            raise exceptions.EmailNotRegistered
        confirmation_email = self.user_repo.refresh_confirmation_code(
            confirmation_email
        )

        # send email
        EmailHelper().send_confirmation_email(confirmation_email)

    def check_confirmation_code(self, email, confirmation_code):
        if not email or not confirmation_code:
            raise exceptions.InvalidArguments
        confirmation_email = self.user_repo.get_confirmation_email(email)
        if not confirmation_email:
            raise exceptions.EmailNotRegistered
        if confirmation_email.confirmation_code != confirmation_code:
            self.user_repo.increment_verification_attempt_count(
                confirmation_email
            )
            raise exceptions.InvalidConfirmationCode
        # don't set verified to true yet

    def login_with_facebook_v2(self, email, confirmation_code, access_token):
        if not email or not confirmation_code:
            raise exceptions.InvalidArguments
        if not access_token:
            raise exceptions.MissingAccessToken()

        fb_data = get_facebook_verification_data(access_token)

        if not fb_data:
            raise exceptions.AuthenticationFailed()

        if not fb_data.get('verified'):
            raise exceptions.NotVerified()

        if not fb_data.get('email'):
            raise exceptions.NoEmailAccount()

        fb_email = fb_data['email'].lower()
        user = self.user_datastore.get_user(fb_email)
        if user:
            user.active = True

            if (
                fb_email.endswith("@harvard.edu") or
                fb_email.endswith(".harvard.edu")
            ):
                user.tier = "harvard"

            # updating photo
            user.thumbnail_url = fb_data['thumbnail_url']
            self.db.session.commit()

            return user

        # if user doesn't exist yet
        confirmation_email = self.user_repo.get_confirmation_email(email)
        if not confirmation_email:
            raise exceptions.EmailNotRegistered
        if confirmation_email.confirmation_code != confirmation_code:
            raise exceptions.InvalidConfirmationCode

        del fb_data['verified']
        user = self._create_new_account(fb_data, source=self.FACEBOOK)
        user.username = confirmation_email.username

        confirmation_email.verified = True
        confirmation_email.user_id = user.id
        self.db.session.merge(user)
        self.db.session.commit()

        return user
