# -*- coding: utf-8 -*-

from twilio.rest import TwilioRestClient

from datetime import datetime

from flask.views import View

from flask import flash, redirect, url_for, render_template, request, session

from google.appengine.ext import ndb

from forms import GiftForm
from models import GiftModel
from models import UserModel

from decorators import registration_required

from settings import TWILIO_SID
from settings import TWILIO_TOKEN


class EditGift(View):

    @registration_required
    def dispatch_request(self, gift_id):
        users = UserModel.query().order(UserModel.user_last_name)
        households = list(set([x.user_household for x in users]))

        gift = GiftModel.get_by_id(gift_id)
        gift.purchased = True if gift.purchaser else False
        form = GiftForm(obj=gift)
        if request.method == "POST":
            if form.validate_on_submit():
                if session['user']['uid'] == gift.added_by.id():
                    if gift.purchaser:
                        purchaser = None
                        owner = None
                        adder = None
                        for user in users:
                            purchaser = user if user.key.id() == gift.purchaser.id() else purchaser
                            owner = user if user.key.id() == gift.owner.id() else owner
                            adder = user if user.key.id() == gift.added_by.id() else adder

                        client = TwilioRestClient(TWILIO_SID, TWILIO_TOKEN)
                        message = client.messages.create(
                            body="An item you purchased (%s) for %s %s was updated by %s %s. %s" % (
                                gift.summary,
                                owner.user_first_name,
                                owner.user_last_name,
                                adder.user_first_name,
                                adder.user_last_name,
                                url_for('edit_gift', gift_id=gift.key.id())
                            ),
                            to=purchaser.user_phone,
                            from_='+15153052239'
                        )

                    gift.summary = form.data.get('summary')
                    gift.description = form.data.get('description')
                if session['user']['uid'] != gift.owner.id():
                    gift.notes = form.data.get('notes')
                    if form.data.get('purchased'):
                        gift.purchaser = ndb.Key(UserModel, session['user']['uid'])
                        gift.purchase_date = datetime.now()
                    elif gift.purchaser:
                        if session['user']['id'] == gift.purchaser.id():
                            gift.purchaser = None
                            gift.purchase_date = None
                        else:
                            flash(u"You can't unclaim a gift you didn't mark as purchased.", 'warning')

                    gift.put()

                    flash(u'Gift %s successfully saved.' % gift_id, 'success')
                else:
                    flash(u"You can't edit a gift you didn't add.", 'warning')
                return redirect(url_for('gift_list', user_id=gift.owner.id()))
        return render_template(
            'edit_gift.html',
            gift=gift,
            form=form,
            auth=session.get('user', {}),
            households=households
        )
