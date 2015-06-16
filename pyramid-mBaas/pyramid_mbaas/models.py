from pyramid.security import (
    Allow,
    Deny,
    Everyone,
    )

from sqlalchemy import (
    Column,
    ForeignKey,
    Index,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    kind = Column(Text)
    power = Column(Integer)

    def __init__(self, name, kind, power):
        self.name = name
        self.kind = kind
        self.power = power

class Box(Base):
    __tablename__ = 'boxs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Text, ForeignKey('users.user_id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    count   = Column(Integer)

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Text, primary_key=True)
    name = Column(Text)
    rank   = Column(Integer)
    HP     = Column(Integer)

    def __init__(self, user_id, name, rank, HP):
        self.user_id = user_id
        self.name = name
        self.rank = rank
        self.HP = HP

class Key(Base):
    __tablename__ = 'keys'
    user_id = Column(Text, primary_key=True)
    seed    = Column(Text)
    vector  = Column(Text)


#Index('user_index', User.id, Box.user_id, unique=True)
#Index('item_index', Item.id, Box.item_id, unique=True)


