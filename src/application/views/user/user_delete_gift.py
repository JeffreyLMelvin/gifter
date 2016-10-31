# -*- coding: utf-8 -*-

from twilio.rest import TwilioRestClient

from flask.views import View

from flask import flash, redirect, url_for, request, session

from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from models import GiftModel
from models import UserModel

from decorators import registration_required

from settings import TWILIO_SID
from settings import TWILIO_TOKEN


class DeleteGift(View):

    @registration_required
    def dispatch_request(self, gift_id):
        gift = GiftModel.get_by_id(gift_id)
        if request.method == "POST":
            if gift.added_by.id() == session['user']['uid']:
                try:
                    if gift.purchaser:
                        users = UserModel.query()
                        purchaser = None
                        owner = None
                        adder = None
                        for user in users:
                            purchaser = user if user.key.id() == gift.purchaser.id() else purchaser
                            owner = user if user.key.id() == gift.owner.id() else owner
                            adder = user if user.key.id() == gift.added_by.id() else adder

                        client = TwilioRestClient(TWILIO_SID, TWILIO_TOKEN)
                        message = client.messages.create(
                            body="An item you purchased (%s) for %s %s was removed by %s %s." % (
                                    gift.summary,
                                    owner.user_first_name,
                                    owner.user_last_name,
                                    adder.user_first_name,
                                    adder.user_last_name
                                ),
                            to=purchaser.user_phone,
                            from_='+15153052239'
                        )

                    gift.key.delete()
                    flash(u'Gift %s successfully deleted.' % gift_id, 'success')
                    return redirect(url_for('gift_list', user_id=gift.owner.id()))
                except CapabilityDisabledError:
                    flash(u'App Engine Datastore is currently in read-only mode.', 'info')
                    return redirect(url_for('gift_list', user_id=gift.owner.id()))
            else:
                flash(u"You can't delete a gift idea that you didn't add.", 'warning')
