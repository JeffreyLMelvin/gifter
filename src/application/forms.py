"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""

from flaskext import wtf
from flaskext.wtf import validators
from wtforms.ext.appengine.ndb import model_form

class UserForm(wtf.Form):
    user_email = wtf.TextField('Email')
    user_first_name = wtf.TextField('First Name', validators=[validators.Required()])
    user_last_name = wtf.TextField('Last Name')
    user_phone = wtf.TextField('Phone', validators=[validators.Required()])
    user_token = wtf.TextField('Token')
    user_household = wtf.TextField('Household')
    user_house_manager = wtf.BooleanField('Household Manager')
    user_is_adult = wtf.BooleanField('Adult')
    user_is_managed = wtf.BooleanField('Managed')

class TokenForm(wtf.Form):
    user_phone = wtf.TextField('Phone Number')
    user_token = wtf.TextField('Token')

class GiftForm(wtf.Form):
    summary = wtf.TextField('Summary')
    description = wtf.TextField('Description/Link')
    notes = wtf.TextAreaField("Note(s) Giftee Can't See")
    purchased = wtf.BooleanField('Purchased')

