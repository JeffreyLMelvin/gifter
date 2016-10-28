"""
urls.py

URL dispatch route mappings and error handlers

"""
from flask import render_template

from application import app

from application.views.public.public_warmup import PublicWarmup
from application.views.public.public_index import PublicIndex
from application.views.public.public_login import PublicLogin, PublicValidateToken

from application.views.admin.admin_list_users import AdminListUsers
from application.views.admin.admin_edit_user import AdminEditUser
from application.views.admin.admin_delete_user import AdminDeleteUser

# from application.views.superadmin.admin_list_users import SuperAdminListUsers
# from application.views.superadmin.admin_edit_user import SuperAdminEditUser
# from application.views.superadmin.admin_delete_user import SuperAdminDeleteUser


# URL dispatch rules

# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'public_warmup', view_func=PublicWarmup.as_view('public_warmup'))

app.add_url_rule('/', 'public_index', view_func=PublicIndex.as_view('public_index'))
app.add_url_rule('/login', 'login', view_func=PublicLogin.as_view('login'), methods=['GET', 'POST'])
app.add_url_rule('/login/<str:user_token>', 'validate', view_func=PublicValidateToken.as_view('validate'))

app.add_url_rule('/registry', 'list_users', view_func=AdminListUsers.as_view('list_users'), methods=['GET', 'POST'])
app.add_url_rule('/registry/<int:user_id>/edit', 'edit_user', view_func=AdminEditUser.as_view('edit_user'), methods=['GET', 'POST'])
app.add_url_rule('/registry/<int:user_id>/delete', 'delete_user', view_func=AdminDeleteUser.as_view('delete_user'), methods=['POST'])

# app.add_url_rule('/admin', 'admin_list_users', view_func=SuperAdminListUsers.as_view('admin_list_users'), methods=['GET', 'POST'])
# app.add_url_rule('/admin/<int:user_id>/edit', 'admin_edit_user', view_func=SuperAdminEditUser.as_view('admin_edit_user'), methods=['GET', 'POST'])
# app.add_url_rule('/admin/<int:user_id>/delete', 'admin_delete_user', view_func=SuperAdminDeleteUser.as_view('admin_delete_user'), methods=['POST'])



# Error handlers

# Handle 404 errors


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
