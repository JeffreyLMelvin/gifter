# -*- coding: utf-8 -*-

from flask.views import View

from flask import flash, redirect, url_for, render_template

from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from forms import UserForm
from models import UserModel

from decorators import registration_required
from decorators import admin_required

class AdminListUsers(View):

    @registration_required
    def dispatch_request(self):
        registered_users = UserModel.query()
        form = UserForm()
        if form.validate_on_submit():
            self.save_entry()
        return render_template(
            'list_users.html',
            users=registered_users,
            form=form,
            is_admin=users.is_current_user_admin()
        )

    @admin_required
    def save_entry(self):
        form = UserForm()
        user = UserModel(
            user_email=form.user_email.data,
            user_first_name=form.user_first_name.data,
            user_last_name=form.user_last_name.data
        )
        try:
            user.put()
            user_id = user.key.id()
            flash(u'User %s successfully saved.' % user_id, 'success')
            return redirect(url_for('list_users'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_users'))
