# -*- coding: utf-8 -*-

import phonenumbers

from flask.views import View

from flask import flash, redirect, url_for, render_template, session

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
        households = list(set(x.user_household for x in registered_users))
        form = UserForm()
        if form.validate_on_submit():
            self.save_entry()
        return render_template(
            'list_users.html',
            users=registered_users,
            form=form,
            auth=session.get('user', {}),
            is_admin=users.is_current_user_admin(),
            households=households
        )

    @admin_required
    def save_entry(self):
        form = UserForm()
        user = UserModel(
            user_email=form.user_email.data,
            user_first_name=form.user_first_name.data,
            user_last_name=form.user_last_name.data,
            user_phone=phonenumbers.format_number(
                phonenumbers.parse(form.user_phone.data, region='US'),
                phonenumbers.PhoneNumberFormat.E164
            ),
            user_token=form.user_token.data,
            user_household=form.user_household.data.title(),
            user_house_manager=form.user_house_manager.data,
            user_is_adult=form.user_is_adult.data,
            user_is_managed=form.user_is_managed.data
        )
        try:
            user.put()
            user_id = user.key.id()
            flash(u'User %s successfully saved.' % user_id, 'success')
            return redirect(url_for('list_users'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_users'))


class AdminFilterUsers(View):
    @registration_required
    def dispatch_request(self, filters):
        filters = filters.split(',')
        registered_users = UserModel.query().order(UserModel.user_last_name)
        households = list(set([x.user_household for x in registered_users]))

        if 'children' in filters:
            filters.remove('children')
            registered_users = filter(lambda x: x.user_is_adult == False, registered_users)
        elif 'adults' in filters:
            filters.remove('adults')
            registered_users = filter(lambda x: x.user_is_adult == True, registered_users)

        filtered_users = []
        if not filters:
            filtered_users = registered_users
        else:
            for user in registered_users:
                if user.user_household in filters:
                    filtered_users.append(user)

        form = UserForm()

        return render_template(
            'list_users.html',
            users=filtered_users,
            form=form,
            auth=session.get('user', {}),
            is_admin=users.is_current_user_admin(),
            households=households
        )