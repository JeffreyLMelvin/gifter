# -*- coding: utf-8 -*-

from flask.views import View

from flask import flash, redirect, url_for, request, session

from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from models import GiftModel

from decorators import registration_required


class DeleteGift(View):

    @registration_required
    def dispatch_request(self, gift_id):
        gift = GiftModel.get_by_id(gift_id)
        if request.method == "POST":
            if gift.added_by.id() == session.user.id():
                try:
                    gift.key.delete()
                    flash(u'Gift %s successfully deleted.' % gift_id, 'success')
                    return redirect(url_for('gift_list', user_id=gift.owner.id()))
                except CapabilityDisabledError:
                    flash(u'App Engine Datastore is currently in read-only mode.', 'info')
                    return redirect(url_for('gift_list', user_id=gift.owner.id()))
            else:
                flash(u"You can't delete a gift idea that you didn't add.", 'warning')
