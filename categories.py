# -*- coding: utf-8 -*-
# def __init__(self, title, description, email, capital=False, population=0,


class Category(object):
    def __init__(self, id, title, description,  image):
        self.id = id
        self.title = title
        self.description = description
        self.image = image

    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE]
        category = Category(source[u'id'], source[u'title'], source[u'image'])

        if u'description' in source:
            category.description = source[u'description']

        return category
        # [END_EXCLUDE]

    def to_dict(self):
        # [START_EXCLUDE]
        dest = {
            u'id': self.id,
            u'title': self.title,
            u'image': self.image,
        }

        if self.description:
            dest[u'description'] = self.description

        return dest
        # [END_EXCLUDE]

    def __repr__(self):
        return(
            u'category(id={}, title={}, description={}, image={})'
            .format(self.id, self.title, self.description, self.image))