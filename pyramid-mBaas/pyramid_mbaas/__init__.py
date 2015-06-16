from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )

from endpoint import (
    VERSION,
)

def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    engine.connect().connection.connection.text_factory = str
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings)

    config.include('pyramid_mako')

    config.add_static_view('static', 'static', cache_max_age=3600)
    
    config.add_route('sign_up', '/' + VERSION +'/sign_up')
    config.add_route('update', '/' + VERSION +'/update')
    config.add_route('user_status', '/' + VERSION +'/user_status')
    
    config.scan()
    return config.make_wsgi_app()
