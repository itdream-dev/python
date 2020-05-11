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


with open('app/static/data/questions_data.json') as data_file:
    data = json.load(data_file)


from lib.models.question import Question
from lib.models.tag import Tag
from lib.registry import get_registry

if __name__ == '__main__':
    db = get_registry()['DB']

    for question_data in data.itervalues():

        question = Question(
            question_1=question_data['question_1'],
            question_2=question_data['question_2'],
            question_3=question_data['question_3'],
            question_4=question_data['question_4'],
            choice_1=question_data['choice_1'],
            choice_2=question_data['choice_2'],
            choice_3=question_data['choice_3'],
            choice_4=question_data['choice_4']
        )

        for tag_data in question_data['tags']:
            tag = Tag.query.filter(
                Tag.name == tag_data
            ).first()

            if not tag:
                tag = Tag(name=tag_data)
                db.session.add(tag)

            question.tags.append(tag)

        db.session.add(question)

    db.session.commit()
