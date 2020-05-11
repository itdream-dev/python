# -*- coding: utf-8 -*-
import os
import subprocess
from flask import Response


def get_git_revision_hash():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'])


def version():
    version_data = ""
    try:
        with open('version.txt', 'r') as f:
            version_data += 'commit: %s\n' % f.read()
    except Exception as e:
        version_data += '%s: %s' % (e.__class__.__name__, e.message)
    try:
        version_data += "env: %s\n" % os.environ.get('IVYSAUR_ENV')
    except Exception as e:
        version_data += '%s: %s' % (e.__class__.__name__, e.message)
    return Response(version_data, mimetype='text/plain')
