# -*- coding: utf-8 -*-
# def __init__(self, dateTime, status, total, capital=False, population=0,


class Order(object):
    def __init__(self, id, userId, dateTime, total, items_quantity, coupon_id, notes, payment_method, payback_for,
                 delivery=False, products_id=[]):
        self.id = id
        self.userId = userId
        self.dateTime = dateTime
        self.total = total
        self.items_quantity = items_quantity
        self.coupon_id = coupon_id
        self.notes = notes
        self.payment_method = payment_method
        self.payback_for = payback_for
        self.delivery = delivery
        self.products_id = products_id

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE]
        order = Order(source[u'id'], source[u'userId'], source[u'dateTime'], source[u'total'])

        if u'items_quantity' in source:
            order.items_quantity = source[u'items_quantity']

        if u'coupon_id' in source:
            order.coupon_id = source[u'coupon_id']

        if u'notes' in source:
            order.notes = source[u'notes']

        if u'payment_method' in source:
            order.payment_method = source[u'payment_method']

        if u'payback_for' in source:
            order.payback_for = source[u'payback_for']

        if u'delivery' in source:
            order.delivery = source[u'delivery']

        if u'products_id' in source:
            order.products_id = source[u'products_id']

        return order
        # [END_EXCLUDE]

    def to_dict(self):
        # [START_EXCLUDE]
        dest = {
            u'id': self.id,
            u'userId': self.userId,
            u'dateTime': self.dateTime,
            u'total': self.total
        }

        if self.items_quantity:
            dest[u'items_quantity'] = self.items_quantity

        if self.coupon_id:
            dest[u'coupon_id'] = self.coupon_id

        if self.notes:
            dest[u'notes'] = self.notes

        if self.payment_method:
            dest[u'payment_method'] = self.payment_method

        if self.payback_for:
            dest[u'payback_for'] = self.payback_for

        if self.delivery:
            dest[u'delivery'] = self.delivery

        if self.products_id:
            dest[u'products_id'] = self.products_id

        return dest
        # [END_EXCLUDE]

    def __repr__(self):
        return(
            u'order(id={}, user_id={}, dateTime={}, total={}, items_quantity={}, coupon_id={}, notes={}, payment_method={}, '
                u'payback_for={}, delivery={})'
            .format(self.id, self.userId, self.dateTime, self.total, self.coupon_id, self.items_quantity, self.notes, self.payment_method,
                    self.payback_for, self.delivery, self.products_id))