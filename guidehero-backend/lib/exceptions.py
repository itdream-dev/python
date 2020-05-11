# -*- coding: utf-8 -*-


class MissingEmailOrPassword(Exception):
    def __init__(self, message='missing_email_or_password'):
        Exception.__init__(self, message)


class LoginFailed(Exception):
    def __init__(self, message='login_failed'):
        Exception.__init__(self, message)


class AccountExists(Exception):
    def __init__(self, message='account_exists'):
        Exception.__init__(self, message)


class NotAuthroized(Exception):
    def __init__(self, message='not_authorized'):
        Exception.__init__(self, message)


class UserDoesntExist(Exception):
    def __init__(self, message='user_doesnt_exist'):
        Exception.__init__(self, message)


class UserSkillDoesntExist(Exception):
    def __init__(self, message='user_skill_doesnt_exist'):
        Exception.__init__(self, message)


class RegistrationNotComplete(Exception):
    def __init__(self, message='registration_not_complete', auth_token=''):
        Exception.__init__(self, message)
        self.auth_token = auth_token


class MissingAccessToken(Exception):
    def __init__(self, message='missing_access_token'):
        Exception.__init__(self, message)


class AuthenticationFailed(Exception):
    def __init__(self, message='authentication_failed'):
        Exception.__init__(self, message)


class InvalidArguments(Exception):
    def __init__(self, message='invalid_arguments'):
        Exception.__init__(self, message)


class NotVerified(Exception):
    def __init__(self, message='not_verified'):
        Exception.__init__(self, message)


class NoEmailAccount(Exception):
    def __init__(self, message='no_email_account'):
        Exception.__init__(self, message)


class InvalidName(Exception):
    def __init__(self, message='invalid_name'):
        Exception.__init__(self, message)


class UsernameAlreadyExists(Exception):
    def __init__(self, message='username_already_exists'):
        Exception.__init__(self, message)


class BioTooLong(Exception):
    def __init__(self, message='bio_too_long'):
        Exception.__init__(self, message)


class AddCommentFailed(Exception):
    def __init__(self, message='add_comment_failed'):
        Exception.__init__(self, message)


class AlreadySubmitted(Exception):
    def __init__(self, message='already_submitted'):
        Exception.__init__(self, message)


class EmailAlreadyRegistered(Exception):
    def __init__(self, message='email_already_registered'):
        Exception.__init__(self, message)


class EmailNotRegistered(Exception):
    def __init__(self, message='email_not_registered'):
        Exception.__init__(self, message)


class InvalidConfirmationCode(Exception):
    def __init__(self, message='invalid_confirmation_code'):
        Exception.__init__(self, message)
