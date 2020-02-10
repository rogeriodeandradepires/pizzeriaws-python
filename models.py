# -*- coding: utf-8 -*-
from application import db


class User():
    id = ""
    name = ""
    email = ""
    phone = ""

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

    def __repr__(self):
        return '<Usuário %d>' % self.id

    # ['BIGINT',
    #  'BINARY',
    #  'BLOB',
    #  'BOOLEAN',
    #  'BOOLEANTYPE',
    #  'BigInteger',
    #  'Binary',
    #  'Boolean',
    #  'CHAR',
    #  'CLOB',
    #  'Comparator',
    #  'Concatenable',
    #  'DATE',
    #  'DATETIME',
    #  'DECIMAL',
    #  'Date',
    #  'DateTime',
    #  'Enum',
    #  'FLOAT',
    #  'Float',
    #  'INT',
    #  'INTEGER',
    #  'INTEGERTYPE',
    #  'Integer',
    #  'Interval',
    #  'LargeBinary',
    #  'NCHAR',
    #  'NULLTYPE',
    #  'NUMERIC',
    #  'NVARCHAR',
    #  'NullType',
    #  'Numeric',
    #  'PickleType',
    #  'REAL',
    #  'SMALLINT',
    #  'STRINGTYPE',
    #  'SchemaEventTarget',
    #  'SchemaType',
    #  'SmallInteger',
    #  'String',
    #  'TEXT',
    #  'TIME',
    #  'TIMESTAMP',
    #  'Text',
    #  'Time',
    #  'TypeDecorator',
    #  'TypeEngine',
    #  'Unicode',
    #  'UnicodeText',
    #  'VARBINARY',
    #  'VARCHAR',
    #  '_Binary',
    #  '_DateAffinity',
    #  '_DefaultColumnComparator',
    #  '__builtins__',
    #  '__doc__',
    #  '__file__',
    #  '__name__',
    #  '__package__',
    #  '_bind_or_error',
    #  '_defer_name',
    #  '_type_map',
    #  'codecs',
    #  'decimal',
    #  'dt',
    #  'event',
    #  'exc',
    #  'operators',
    #  'pickle',
    #  'processors',
    #  'quoted_name',
    #  'to_instance',
    #  'type_api',
    #  'type_coerce',
    #  'util']