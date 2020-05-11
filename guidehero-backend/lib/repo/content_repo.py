# -*- coding: utf-8 -*-
from lib.registry import get_registry
from lib.models.content import Content
from lib.models.tag import Tag


class ContentRepo(object):

    def __init__(self):
        self.db = get_registry()['DB']

    def get_all_content(self):
        return Content.query.all()

    def get_content(self, content_id):
        return Content.query.filter(Content.id == content_id).first()

    def up_vote_content(self, content_id, decrement_opposite):
        content = Content.query.filter(Content.id == content_id).first()
        if not content:
            return
        content.up_vote += 1

        if decrement_opposite:
            content.down_vote = max(content.down_vote - 1, 0)
        self.db.session.merge(content)
        self.db.session.commit()

    def down_vote_content(self, content_id, decrement_opposite):
        content = Content.query.filter(Content.id == content_id).first()
        if not content:
            return
        content.down_vote += 1

        if decrement_opposite:
            content.up_vote = max(content.up_vote - 1, 0)
        self.db.session.merge(content)
        self.db.session.commit()

    def add_content(self, content_text, tags, user):
        content = Content(
            user_id=user.id,
            content=content_text
        )

        for tag_data in tags:
            tag = Tag.query.filter(
                Tag.name == tag_data
            ).first()

            if not tag:
                tag = Tag(name=tag_data)
                self.db.session.add(tag)

            content.tags.append(tag)

        self.db.session.add(content)
        self.db.session.commit()

    def edit_content(self, content_text, tags, user, content):
        content.content = content_text
        content.tags = []

        for tag_data in tags:
            tag = Tag.query.filter(
                Tag.name == tag_data
            ).first()

            if not tag:
                tag = Tag(name=tag_data)
                self.db.session.add(tag)

            content.tags.append(tag)

        self.db.session.add(content)
        self.db.session.commit()
