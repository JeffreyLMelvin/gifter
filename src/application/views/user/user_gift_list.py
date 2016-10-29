from flask.views import View

from flask import flash
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask import request

from google.appengine.ext import ndb

from models import GiftModel
from forms import GiftForm


class UserGifts(View):
    def dispatch_request(self):
        return 'here'