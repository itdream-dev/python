# -*- coding: utf-8 -*-
import arrow
from config import Ivysaur
from flask_mail import Message
from registry import get_registry


class EmailHelper(object):

    def __init__(self):
        self.mail = get_registry()['MAIL']

    def send_email(self, user, expert, user_skill, now):
        msg = Message(
            u'[Expert Request] User:%s Expert:%s' % (user.email, expert.email),
            sender=Ivysaur.Config.MAIL_USERNAME,
            recipients=[Ivysaur.Config.MAIL_USERNAME])
        msg.html = u"""
        Expert Request<br><br>
        requested at: %s<br>

        User Info:<br>
        Name: %s %s<br>
        Email: %s<br><br>

        Expert Info:<br>
        Name: %s %s<br>
        Email: %s<br><br>
        Skill: %s<br>
        Price: $%0.2f / min<br>
        """ % (
            now, user.first_name, user.last_name, user.email,
            expert.first_name, expert.last_name, expert.email,
            user_skill.skill.name, user_skill.price / 100.00
        )
        self.mail.send(msg)

    def send_cancel_email(self, user, expert, user_skill):
        msg = Message(
            u'[Expert Request CANCELLED] User:%s Expert:%s' % (
                user.email, expert.email
            ),
            sender=Ivysaur.Config.MAIL_USERNAME,
            recipients=[Ivysaur.Config.MAIL_USERNAME])
        msg.html = u"""
        Expert Request <br>
        <font color="red" size="8">Cancelled</font><br><br>
        cancelled at: %s<br>

        User Info:<br>
        Name: %s %s<br>
        Email: %s<br><br>

        Expert Info:<br>
        Name: %s %s<br>
        Email: %s<br><br>
        Skill: %s<br>
        Price: $%0.2f / min<br>
        """ % (
            arrow.utcnow(), user.first_name, user.last_name, user.email,
            expert.first_name, expert.last_name, expert.email,
            user_skill.skill.name, user_skill.price / 100.00
        )
        self.mail.send(msg)

    def send_venmo_transfer_email(self, user, username, email):
        msg = Message(
            u'[Venmo Request] User:%s' % (
                user.email
            ),
            sender=Ivysaur.Config.MAIL_USERNAME,
            recipients=["chrisryuichi@gmail.com"])
        msg.html = u"""
        Venmo Request from:<br><br>

        User Info:<br>
        Name: %s %s<br>
        Email: %s<br><br>

        Venmo Info:<br>
        Username: %s<br>
        Email: %s<br><br>
        """ % (
            user.first_name, user.last_name, user.email,
            username, email
        )
        self.mail.send(msg)

    def send_card_transfer_email(self, user, payment_type, email):
        msg = Message(
            u'[%s Request] User:%s' % (
                payment_type, user.email
            ),
            sender=Ivysaur.Config.MAIL_USERNAME,
            recipients=["chrisryuichi@gmail.com"])
        msg.html = u"""
        %s Request from:<br><br>

        User Info:<br>
        Name: %s %s<br>
        Email: %s<br><br>

        %s Info:<br>
        Email: %s<br><br>
        """ % (
            payment_type, user.first_name, user.last_name, user.email,
            payment_type, email
        )
        self.mail.send(msg)

    def send_get_point_email(self, user, username, email, amount, silver_point):
        msg = Message(
            u'[Get Point Request] User:%s' % (
                user.email
            ),
            sender=Ivysaur.Config.MAIL_USERNAME,
            recipients=["chrisryuichi@gmail.com"])
        msg.html = u"""
        Get Point Request from:<br><br>

        User Info:<br>
        Name: %s %s<br>
        Email: %s<br><br>

        Venmo Info:<br>
        Username: %s<br>
        Email: %s<br><br>
        Amount: $%.2f<br>
        Points: %d<br><br>
        """ % (
            user.first_name, user.last_name, user.email,
            username, email, amount, silver_point
        )
        self.mail.send(msg)

    def send_confirmation_email(self, confirmation_email):
        msg = Message(
            u'[GuideHero] Confirmation Email',
            sender=Ivysaur.Config.MAIL_USERNAME,
            recipients=[confirmation_email.id])
        msg.html = u"""
        Thank you for registering.<br><br>

        Your confirmation code is: %s
        """ % confirmation_email.confirmation_code
        self.mail.send(msg)
