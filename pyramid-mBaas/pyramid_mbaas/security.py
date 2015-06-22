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

import hashlib, os
from Crypto.Cipher import AES

def signup(seed):
    try:
        key = key_gen()
        seed  = key['seed']
        init_vector = key['vector']
        user_id = hashlib.sha256(seed+init_vector).hexdigest()
        
        if exist(user_id):
            return None
        
        key = Key(user_id = user_id, seed = seed, vector = init_vector)
        user = User(name = "", rank=1, HP=10, user_id = user_id)

        DBSession.add(user)
        DBSession.add(key)

        return {
            'user_id':user_id, 
            'seed':seed.encode('hex'),
            'vector':init_vector.encode('hex')
        }
    except(DBAPIError):
        return None


def key_gen(seed=None):
    if seed:
        seed = hashlib.sha256(seed).digest()
    else:
        seed = hashlib.sha256(os.urandom(16)).digest()

    init_vector = os.urandom(16)
    return {
        'seed':seed.encode('hex'),
        'vector':init_vector.encode('hex'),
    }

def decrypt(user_id ,data):
    try:
        if not exist(user_id):
            return None
        key = DBSession.query(Key).filter(Key.user_id == user_id).one()
        aes = AES.new(key.seed.decode('hex'), AES.MODE_CBC, key.vector.decode('hex'))
        data = aes.decrypt(data)
    except(DBAPIError):
        return None
    
    return data

def encrypt(user_id, data):
    try:
        if not exist(user_id):
            return None
        
        key = DBSession.query(Key).filter(Key.user_id == user_id).one()
        aes = AES.new(key.seed.decode('hex'), AES.MODE_CBC, key.vector.decode('hex'))
        data = data + (16 - (len(data) % 16))*" "
        result = aes.encrypt(data)
    except(DBAPIError):
        return None

    return result
