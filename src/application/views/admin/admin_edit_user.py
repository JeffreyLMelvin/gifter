# -*- coding: utf-8 -*-

from flask.views import View

from flask import flash, redirect, url_for, render_template, request

from forms import UserForm
from models import UserForm

from decorators import admin_required


class AdminEditUser(View):

    @admin_required
    def dispatch_request(self, user_id):
        user = UserModel.get_by_id(user_id)
        form = UserForm(obj=user)
        if request.method == "POST":
            if form.validate_on_submit():
                user.first_name = form.data.get('user_first_name')
                user.last_name = form.data.get('user_last_name')
                user.email = form.data.get('user_email')
                user.put()
                flash(u'User %s successfully saved.' % user_id, 'success')
                return redirect(url_for('list_users'))
        return render_template('edit_user.html', user=user, form=form)
