# -*- coding: utf-8 -*-

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    User,
)
from .key import ( 
    secret_key,
    init_vec
)
import hashlib

from Crypto.Cipher import AES

def signup(name):
    try:
        seed = hashlib.sha256(os.urandom(16)).digest()
        init_vector = os.urandom(16)
        print("seed:"+seed.encode('hex')+" vector:"+init_vector.encode('hex'))
        if exist(name):
            return False

        user = User(account = name, rank=1, HP=10, seed=seed.encode('hex'), vector=init_vector.encode('hex'))
        DBSession.add(user)
    except(DBAPIError):
        return False
    return True

def exist(account):
    try:
        res = DBSession.query(User).filter(User.account == account).first()
    except(DBAPIError):
        return False
    if res:
        return True
    return False

def decrypt(name, data):

    try:
        if not exist(name):
            return None
        print("user exist")
        user = DBSession.query(User).filter(User.account == name).one()
        aes = AES.new(user.seed.decode('hex')), AES.MODE_CBC, user.vector.decode('hex'))
        data = aes.decrypt(data)

        print("data:"+  data)
    except DBAPIError:
        return None
    
    return data

def groupfinder(name, request):
    try:
        user = DBSession.query(User).filter(User.name == name).one()
    except DBAPIError:
        return []   
 
    if user:
        return ['group:users']


