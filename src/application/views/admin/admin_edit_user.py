# -*- coding: utf-8 -*-

import phonenumbers

from flask.views import View

from flask import flash, redirect, url_for, render_template, request, session

from forms import UserForm
from models import UserModel

from decorators import admin_required


class AdminEditUser(View):

    @admin_required
    def dispatch_request(self, user_id):
        users = UserModel.query().order(UserModel.user_last_name)
        user = filter(lambda x: x.key.id()==user_id, users)[0]
        households = list(set([x.user_household for x in users]))

        #user = UserModel.get_by_id(user_id)

        form = UserForm(obj=user)
        if request.method == "POST":
            if form.validate_on_submit():
                user.user_first_name = form.data.get('user_first_name')
                user.user_last_name = form.data.get('user_last_name')
                user.user_email = form.data.get('user_email')
                user.user_phone = phonenumbers.format_number(
                    phonenumbers.parse(form.data.get('user_phone'), region='US'),
                    phonenumbers.PhoneNumberFormat.E164
                )
                user.user_admin = form.data.get('user_admin')
                user.user_household = form.data.get('user_household')
                user.user_house_manager = form.data.get('user_house_manager')
                user.user_is_adult = form.data.get('user_is_adult')
                user.user_is_managed = form.data.get('user_is_managed')
                user.put()
                flash(u'User %s successfully saved.' % user_id, 'success')
                return redirect(url_for('list_users'))
        return render_template(
            'edit_user.html',
            user=user,
            form=form,
            auth=session.get('user', {}),
            households=households
        )
