from uuid import uuid4

from flask.views import View

from flask import render_template
from flask import session

from google.appengine.ext import ndb

from forms import RequestTokenForm
from models import UserModel


class PublicLogin(View):
    def dispatch_request(self):
        form = RequestTokenForm()
        if form.validate_on_submit():
            token = uuid4().hex[:6]
            phone = form.user_phone.data
            registered_users = UserModel.query(user_phone=user_phone)
            for registered_user in registered_user:
                registered_user.token = token
            ndb.put_multi(registered_users)
            return render_template('404.html')

        return render_template('validate_token.html')


class PublicValidateToken(View):
    def dispatch_request(self, user_token):
        registered_users = UserModel.query()
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
            return redirect(url_for('login'))