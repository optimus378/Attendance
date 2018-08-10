#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/venvs/kwattendance/kwattendance/")

from app import wsgi_app as application
application.secret_key = 'We-all-swim-in-the-same-river@#$^&!'
