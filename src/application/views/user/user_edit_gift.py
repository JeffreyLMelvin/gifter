# -*- coding: utf-8 -*-

from flask.views import View

from flask import flash, redirect, url_for, render_template, request, session

from google.appengine.ext import ndb

from forms import GiftForm
from models import GiftModel
from models import UserModel

from decorators import registration_required


class EditGift(View):

    @registration_required
    def dispatch_request(self, gift_id):
        gift = GiftModel.get_by_id(gift_id)
        gift.purchased = True if gift.purchaser else False
        form = GiftForm(obj=gift)
        if request.method == "POST":
            if form.validate_on_submit():
                if session['user']['uid'] == gift.added_by.id():
                    gift.summary = form.data.get('summary')
                    gift.description = form.data.get('description')
                    if session['user']['uid'] != gift.owner.id():
                        gift.notes = form.data.get('notes')
                        if form.data.get('purchased'):
                            gift.purchaser = ndb.Key(UserModel, session['user']['uid'])
                        else:
                            gift.purchaser = None

                    gift.put()

                    flash(u'Gift %s successfully saved.' % gift_id, 'success')
                else:
                    flash(u"You can't edit a gift you didn't add.", 'warning')
                return redirect(url_for('gift_list', user_id=gift.owner.id()))
        return render_template(
            'edit_gift.html',
            gift=gift,
            form=form,
            auth=session.get('user', {})
        )
