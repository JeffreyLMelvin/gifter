# -*- coding: utf-8 -*-
from datetime import datetime

from flask.views import View

from flask import flash, redirect, url_for, render_template, request, session

from google.appengine.ext import ndb

from forms import GiftForm
from models import GiftModel
from models import UserModel

from decorators import registration_required


class PurchaseGift(View):

    @registration_required
    def dispatch_request(self, gift_id):
        gift = GiftModel.get_by_id(gift_id)
        auth_id = session.get('user', {}).get('uid')
        user = ndb.Key(UserModel, auth_id)
        if not gift.purchaser:
            gift.purchaser = user
            gift.purchase_date = datetime.now()
            gift.put()

            flash(u'Gift %s successfully saved.' % gift_id, 'success')
        elif auth_id != gift.owner.id():
            flash(u'Gift %s already purchased.' % gift_id, 'warning')
            
        return redirect(url_for('gift_list', user_id=gift.owner.id()))
