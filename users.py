# -*- coding: utf-8 -*-
# def __init__(self, name, phone, email, capital=False, population=0,


class User(object):
    def __init__(self, uid, register_date, name, phone, email, main_address_id, image, orders_id=[]):
        self.uid = uid
        self.register_date = register_date
        self.name = name
        self.phone = phone
        self.email = email
        self.image = image
        self.main_address_id = main_address_id
        self.orders_id = orders_id

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE]
        user = User(source[u'uid'], source[u'name'], source[u'phone'], source[u'email'])

        if u'register_date' in source:
            user.register_date = source[u'register_date']

        if u'main_address_id' in source:
            user.main_address_id = source[u'main_address_id']

        if u'image' in source:
            user.image = source[u'image']

        if u'orders_id' in source:
            user.orders_id = source[u'orders_id']

        return user
        # [END_EXCLUDE]

    def to_dict(self):
        # [START_EXCLUDE]
        dest = {
            u'uid': self.uid,
            u'name': self.name,
            u'phone': self.phone,
            u'email': self.email
        }

        if self.main_address_id:
            dest[u'main_address_id'] = self.main_address_id

        if self.register_date:
            dest[u'register_date'] = self.register_date

        if self.image:
            dest[u'image'] = self.image

        if self.orders_id:
            dest[u'orders_id'] = self.orders_id

        return dest
        # [END_EXCLUDE]

    def __repr__(self):
        return(
            u'user(uid={}, register_date={}, name={}, phone={}, email={}, image={}, main_address_id={})'
            .format(self.uid, self.register_date, self.name, self.email, self.image, self.main_address_id,
                    self.orders_id))