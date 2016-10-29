"""
models.py

App Engine datastore models

"""

from google.appengine.ext import ndb


class UserModel(ndb.Model):
    user_email = ndb.StringProperty(default=None)
    user_first_name = ndb.StringProperty(required=True)
    user_last_name = ndb.StringProperty(required=True)
    # version 2
    user_phone = ndb.StringProperty(default=None)
    user_token = ndb.StringProperty(default=None)


class GiftModel(ndb.Model):
    summary = ndb.StringProperty(required=True)
    description = ndb.StringProperty(default='')
    purchaser = ndb.KeyProperty(default=None)
