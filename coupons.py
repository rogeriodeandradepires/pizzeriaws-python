# -*- coding: utf-8 -*-
# def __init__(self, code, description, email, capital=False, population=0,


class Coupon(object):
    def __init__(self, id, code, description,  discount):
        self.id = id
        self.code = code
        self.description = description
        self.discount = discount

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE]
        coupon = Coupon(source[u'id'], source[u'code'], source[u'discount'])

        if u'description' in source:
            coupon.description = source[u'description']

        return coupon
        # [END_EXCLUDE]

    def to_dict(self):
        # [START_EXCLUDE]
        dest = {
            u'id': self.id,
            u'code': self.code,
            u'discount': self.discount,
        }

        if self.description:
            dest[u'description'] = self.description

        return dest
        # [END_EXCLUDE]

    def __repr__(self):
        return(
            u'coupon(id={}, code={}, description={}, discount={})'
            .format(self.id, self.code, self.description, self.discount))