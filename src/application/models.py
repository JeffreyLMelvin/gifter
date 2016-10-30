"""
models.py

App Engine datastore models

"""

from google.appengine.ext import ndb


class UserModel(ndb.Model):
    user_email = ndb.StringProperty(default=None)
    user_first_name = ndb.StringProperty(required=True, default='')
    user_last_name = ndb.StringProperty(required=True, default='')
    # version 2
    user_phone = ndb.StringProperty(default=None)
    user_token = ndb.StringProperty(default=None)
    # version 3
    user_household = ndb.StringProperty(default='Other')
    user_house_manager = ndb.BooleanProperty(default=False)
    user_is_adult = ndb.BooleanProperty(default=False)



class GiftModel(ndb.Model):
    owner = ndb.KeyProperty(required=True, kind=UserModel)
    added_by = ndb.KeyProperty(required=True, kind=UserModel)
    summary = ndb.StringProperty(required=True)
    description = ndb.StringProperty(default='')
    notes = ndb.StringProperty(default='')
    purchaser = ndb.KeyProperty(default=None, kind=UserModel)
