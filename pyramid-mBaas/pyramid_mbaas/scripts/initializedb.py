# -*- coding: utf-8 -*-

import os
import sys
import transaction

from .info import email

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    User,
    Item,
    Box,
    Base,
    )
from ..security import (
    signup
    )

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    engine.connect().connection.connection.text_factory = str 
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        signup(email)
        item1 = Item(name = u'勧誘チケット', kind='ticket', power = 1)
        item2 = Item(name = u'ミラクルストーン', kind='ticket', power = 1)
        
        
        DBSession.add(item1)
        DBSession.add(item2)

