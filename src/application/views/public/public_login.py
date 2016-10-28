from uuid import uuid4

from flask.views import View

from flask import flash
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for

from google.appengine.ext import ndb

from forms import TokenForm
from models import UserModel


class PublicLogin(View):
    def dispatch_request(self):
        form = TokenForm()
        if form.validate_on_submit():
            token = uuid4().hex[:6]
            phone = form.user_phone.data
            registered_users = UserModel.query(UserModel.user_phone == phone)
            for registered_user in registered_users:
                registered_user.token = token
            ndb.put_multi(registered_users)
            flash(u"Token sent to %s. Follow link or type in token above." % phone, 'success')

        return render_template('validate_token.html', form=form)


class PublicValidateToken(View):
    def dispatch_request(self, user_token):
        form = TokenForm()
        if form.validate_on_submit():
            user_token = form.user_token.data
        registered_users = UserModel.query(UserModel.user_token == user_token)
        updated_users = []
        for registered_user in registered_users:
            if registered_user.user_token and registered_user.user_token == user_token:
                session['user'] = phone
                registered_user.user_token = None
                updated_users.append(registered_user)
        ndb.put_multi(updated_users)

        if session.get('user', None):
            return redirect(url_for('list_users'))
        else:
            flash(u"Invalid token, please request a new one.", 'warning')
            return redirect(url_for('login'))