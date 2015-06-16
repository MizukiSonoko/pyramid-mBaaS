# -*- coding: utf-8 -*-

import unittest
import transaction

from Crypto.Cipher import AES
from pyramid import testing

from .models import (
    DBSession,
    User,
)
from .endpoint import (
    VERSION,
)

from .key import secret_key
from .security import (
    decrypt,
    encrypt,
)

import json, os

class TestFunctionSuccessCondition(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from .models import (
            Base,
        )
        from .security import (
            signup,
        )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)

        with transaction.manager:
            seed = os.urandom(16).encode('hex')
            signup(seed)
        engine = create_engine('sqlite://')
        Base.metadata.create_all(engine)

        from pyramid_mbaas import main
        from webtest import TestApp
        a = main({}, **{'sqlalchemy.url': 'sqlite://'})
        self.app = TestApp(a)
        
        self.user_id = ''
        self.seed = ''
        self.vector = ''


    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_signup(self):
        import os
        seed = os.urandom(16).encode('hex')
        res = self.app.post('/'+ VERSION +'/sign_up',{
            'hash':seed,
        }, status = 200)
        obj = json.loads(res.body)

        self.user_id = obj['user_id']
        self.seed    = obj['seed']
        self.vector  = obj['vector']

        res = self.app.post('/'+ VERSION +'/user_status',{
            'user_id': self.user_id,
        }, status = 200)
        obj = json.loads(res.body)
        print(decrypt(self.user_id, obj['data'].decode('hex')))

        data = encrypt(self.user_id, '{"name":"Mizuki"}')
        data = data.encode('hex')
        res = self.app.post('/'+ VERSION +'/update',{
            'user_id': self.user_id,
            'data':data,
        }, status = 200)
        
        obj = json.loads(res.body)

        res = self.app.post('/'+ VERSION +'/user_status',{
            'user_id': self.user_id,
        }, status = 200)
        obj = json.loads(res.body)
        print("UserName:"+decrypt(self.user_id, obj['data'].decode('hex')))

