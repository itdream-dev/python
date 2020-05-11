#!/usr/bin/env python
import os
import sys

from app.ivysaur_app import create_app


ivysaur_env = os.environ.get('IVYSAUR_ENV')
if not ivysaur_env:
    print "please set IVYSAUR_ENV environment var"
    sys.exit(1)

application = create_app(ivysaur_env)

if __name__ == '__main__':
    if ivysaur_env == 'development':
    	application.run(host='0.0.0.0', threaded=True)
        # application.run(threaded=True)
    else:
        application.run()
