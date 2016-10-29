# -*- coding: utf-8 -*-

from flask.views import View

from flask import flash, redirect, url_for, render_template, request, session

from forms import GiftForm
from models import GiftModel
from models import UserModel

from decorators import registration_required


class EditGift(View):

    @registration_required
    def dispatch_request(self, gift_id):
        gift = GiftModel.get_by_id(gift_id)
        form = GiftForm(obj=gift)
        form.purchased = True if gift.purchaser else False
        if request.method == "POST":
            if form.validate_on_submit():
                gift.summary = form.data.get('summary')
                gift.description = form.data.get('description')
                if session.user.id() != gift.owner.id():
                    gift.notes = form.data.get('notes')
                    if form.data.get('purchased'):
                        gift.purchaser = session.user.key

                gift.put()

                flash(u'Gift %s successfully saved.' % gift_id, 'success')
                return redirect(url_for('gift_list', user_id=gift.owner.id()))
        return render_template(
            'edit_gift.html',
            gift=gift,
            form=form,
            auth=session.get('user', UserModel())
        )
