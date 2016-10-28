# -*- coding: utf-8 -*-

from flask.views import View

from flask import redirect, url_for

from decorators import admin_required


class AdminSecret(View):

    @admin_required
    def dispatch_request(self):

        return redirect(url_for('list_users'))
