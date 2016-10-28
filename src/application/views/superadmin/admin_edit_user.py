# -*- coding: utf-8 -*-

from flask.views import View

from flask import flash, redirect, url_for, render_template, request

from forms import UserForm
from models import UserModel

from decorators import superadmin_required


class SuperAdminEditUser(View):

    @superadmin_required
    def dispatch_request(self, user_id):
        user = UserModel.get_by_id(user_id)
        form = UserForm(obj=user)
        if request.method == "POST":
            if form.validate_on_submit():
                user.user_first_name = form.data.get('user_first_name')
                user.user_last_name = form.data.get('user_last_name')
                user.user_email = form.data.get('user_email')
                user.user_phone = form.data.get('user_phone')
                user.user_admin = form.data.get('user_admin')
                user.put()
                flash(u'User %s successfully saved.' % user_id, 'success')
                return redirect(url_for('list_users'))
        return render_template('edit_user.html', user=user, form=form)
