# -*- coding: utf-8 -*-
from flask import Response, request


def log():
    if request.args.get('clear') == 'yes':
        with open('ivysaur.log', 'w') as f:
            f.write('Clear111-------------------\n')
            f.close()

    content = ''
    with open('ivysaur.log', 'r') as f:
        content = f.read()
        f.close()
    return Response(content, mimetype='text/plain')
