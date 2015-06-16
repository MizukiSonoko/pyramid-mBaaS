# -*- coding: utf-8 -*-

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    User,
    Key,
)
from .manager import (
    exist,
)

import hashlib
from Crypto.Cipher import AES

def signup(seed):
    try:
        seed = hashlib.sha256(seed).digest()
        init_vector = os.urandom(16)
        print("seed:"+seed.encode('hex')+" vector:"+init_vector.encode('hex'))
        
        user_id = hashlib.sha256(seed.encode('hex')+init_vector.encode('hex')).hexdigest()
        
        if exist(user_id):
            return None
        
        key = Key(user_id = user_id, seed = seed.encode('hex'), vector = vector.encode('hex'))
        user = User(name = "", rank=1, HP=10, user_id = user_id)

        DBSession.add(user)
        DBSession.add(key)

        return {
            'user_id':user_id, 
            'seed':seed.encode('hex'),
            'vector':vector.encode('hex')
        }
    except(DBAPIError):
        return None

def decrypt(user_id ,data):
    try:
        if not exist(user_id):
            return None
        print("user exist")
        key = DBSession.query(Key).filter(Key.user_id == user_id).one()
        aes = AES.new(key.seed.decode('hex'), AES.MODE_CBC, key.vector.decode('hex'))
        data = aes.decrypt(data)

        print("data:"+  data)
    except(DBAPIError):
        return None
    
    return data

def encrypt(user_id, data):
    try:
        if not exist(user_id):
            return None
        
        key = DBSession.query(Key).filter(Key.user_id == user_id).one()
        aes = AES.new(key.seed.decode('hex'), AES.MODE_CBC, key.vector.decode('hex'))
        result = aes.encrypt(data)
    except(DBAPIError):
        return None

    return data
