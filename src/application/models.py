"""
models.py

App Engine datastore models

"""

from google.appengine.ext import ndb


class ExampleModel(ndb.Model):
    """Example Model"""
    example_name = ndb.StringProperty(required=True)
    example_description = ndb.TextProperty(required=True)
    added_by = ndb.UserProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)


class UserModel(ndb.Model):
    user_email = ndb.StringProperty(required=False)
    user_first_name = ndb.StringProperty(required=True)
    user_last_name = ndb.StringProperty(required=True)
    user_phone = ndb.StringProperty(required=True)
    user_token = ndb.StringProperty(required=True, default=None)
    user_admin = ndb.BooleanProperty(required=True, default=False)