# -*- coding: utf-8 -*-
# def __init__(self, dateRegister, description, price, capital=False, population=0,


class Product(object):
    def __init__(self, id, dateRegister, description, price, category, size, notes, ingredients, 
                 image):
        self.id = id
        self.dateRegister = dateRegister
        self.description = description
        self.price = price
        self.category = category
        self.size = size
        self.notes = notes
        self.ingredients = ingredients
        self.image = image

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE]
        product = Product(source[u'id'], source[u'dateRegister'], source[u'description'], source[u'price'])

        if u'category' in source:
            product.category = source[u'category']

        if u'size' in source:
            product.size = source[u'size']

        if u'notes' in source:
            product.notes = source[u'notes']

        if u'ingredients' in source:
            product.ingredients = source[u'ingredients']

        if u'image' in source:
            product.image = source[u'image']

        return product
        # [END_EXCLUDE]

    def to_dict(self):
        # [START_EXCLUDE]
        dest = {
            u'id': self.id,
            u'dateRegister': self.dateRegister,
            u'description': self.description,
            u'price': self.price
        }

        if self.category:
            dest[u'category'] = self.category

        if self.size:
            dest[u'size'] = self.size

        if self.notes:
            dest[u'notes'] = self.notes

        if self.ingredients:
            dest[u'ingredients'] = self.ingredients

        if self.image:
            dest[u'image'] = self.image

        return dest
        # [END_EXCLUDE]

    def __repr__(self):
        return(
            u'product(id={}, dateRegister={}, description={}, price={}, category={}, size={}, notes={}, ingredients={}, image={})'
            .format(self.id, self.dateRegister, self.description, self.price, self.size, self.category, self.notes,
                    self.ingredients, self.image))