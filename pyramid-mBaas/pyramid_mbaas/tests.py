import unittest
import transaction

from pyramid import testing

from .models import DBSession
from .endpoint import (
    VERSION,
    )


class TestMyViewSuccessCondition(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from .models import (
            Base,
            )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            pass

        from pyramid_mbaas import main
        from webtest import TestApp
        a = main({}, **{'sqlalchemy.url': 'sqlite://'})
        self.app = TestApp(a)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_passing_view(self):
        res = self.app.post('/'+ VERSION +'/login', status = 200)

