# -*- coding: utf-8 -*-
# def __init__(self, street, number, email, capital=False, population=0,


class Address(object):
    def __init__(self, id, user_id, zip_code_cep, street, number, neighborhood, reference, state='São Paulo', city='Araçatuba'):
        self.id = id
        self.user_id = user_id
        self.zip_code_cep = zip_code_cep
        self.street = street
        self.number = number
        self.neighborhood = neighborhood
        self.reference = reference
        self.state = state
        self.city = city

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE]
        address = Address(source[u'id'], source[u'user_id'], source[u'zip_code_cep'], source[u'street'], source[u'neighborhood'])

        if u'number' in source:
            address.number = source[u'number']

        if u'state' in source:
            address.state = source[u'state']

        if u'city' in source:
            address.city = source[u'city']

        if u'reference' in source:
            address.reference = source[u'reference']

        return address
        # [END_EXCLUDE]

    def to_dict(self):
        # [START_EXCLUDE]
        dest = {
            u'id': self.id,
            u'user_id': self.user_id,
            u'zip_code_cep': self.zip_code_cep,
            u'street': self.street,
            u'neighborhood': self.neighborhood,
        }

        if self.number:
            dest[u'number'] = self.number

        if self.state:
            dest[u'state'] = self.state

        if self.city:
            dest[u'city'] = self.city

        if self.reference:
            dest[u'reference'] = self.reference

        return dest
        # [END_EXCLUDE]

    def __repr__(self):
        return(
            u'address(id={}, user_id={}, street={}, zip_code_cep={}, number={}, neighborhood={}, state={}, city={}, reference={})'
            .format(self.id, self.user_id, self.zip_code_cep, self.street, self.number, self.neighborhood, self.state, self.city,
                    self.reference))