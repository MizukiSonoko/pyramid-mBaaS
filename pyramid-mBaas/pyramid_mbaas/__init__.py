from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramidlogin.security import groupfinder

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

    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret!!', callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,
        root_factory='pyramid_mbaas.models.RootFactory')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.include('pyramid_mako')

    config.add_static_view('static', 'static', cache_max_age=3600)
    
    config.add_route('login', '/' + VERSION +'/login')
    config.add_route('user_status', '/' + VERSION +'/user_status')

    

    config.scan()
    return config.make_wsgi_app()
