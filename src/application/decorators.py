"""
decorators.py

Decorators for URL handlers

"""

from functools import wraps
from google.appengine.api import users
from flask import redirect, request, abort, session, url_for

from models import UserModel


def login_required(func):
    """Requires standard login credentials"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not users.get_current_user():
            return redirect(users.create_login_url(request.url))
        return func(*args, **kwargs)
    return decorated_view


def registration_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        is_admin = users.is_current_user_admin()
        if flask.session.get('user', None) or is_admin:
            return func(*args, **kwargs)
        return redirect(url_for('login'))
        # if current_user:
        #     is_registered = current_user.email() in [x.user_email for x in UserModel.query()]
        #     if is_registered or users.is_current_user_admin():
        #         return func(*args, **kwargs)
        #     abort(401)
        # return redirect(users.create_login_url(request.url))
    return decorated_view


def admin_required(func):
    """Requires App Engine admin credentials"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if users.get_current_user():
            if not users.is_current_user_admin():
                abort(401)  # Unauthorized
            return func(*args, **kwargs)
        return redirect(users.create_login_url(request.url))
    return decorated_view


def superadmin_required(func):
    """Requires App Engine admin credentials"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if users.get_current_user():
            if not users.is_current_user_admin():
                abort(401)  # Unauthorized
            return func(*args, **kwargs)
        return redirect(users.create_login_url(request.url))
    return decorated_view