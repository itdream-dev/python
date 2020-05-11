# -*- coding: utf-8 -*-
from lib.registry import get_registry
from lib.models.skill import Skill


class SkillRepo(object):

    def __init__(self):
        self.db = get_registry()['DB']

    def get_skill(self, skill_id):
        return Skill.query.filter(Skill.id == skill_id).first()
