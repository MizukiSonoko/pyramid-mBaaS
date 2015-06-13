
import json
import os
import hashlib

from pyramid.response import Response
from pyramid.view import (
    view_config,
    notfound_view_config
    )

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    )

from .endpoint import (
    VERSION,
    )
from .security import (
    decrypt,
    )


@view_config(route_name='login', request_method='POST', renderer='json')
def login(request):
    account = None
    data = None
    if 'account' in request.params:
        account = request.params['account']
    if 'seed' in request.params:
        seed = request.params['seed']
    if 'vector' in request.params:
        vec  = request.params['vector']

    if account and seed and vec:
        account = account + (16-(len(account)%16))*"$"
        user = authenticate( account, os.urandom(16), os.urandom(16))
        if user:
            headers = {
                'auth-token': hashlib.md5( os.urandom(16)).digest(),
            } 
            return Response( headers = headers, body=json.dumps(
                {'code':'200',
                 'message':'login successfull'
                 }
            ),

            status = '200 OK',
            content_type='application/json')

    return Response(
        body=json.dumps(
            {'code':'403',
             'message':'Invalied request'}
        ),
        status = '403 forbidden',
        content_type='application/json')

@view_config(route_name='user_status', request_method='POST', renderer='json')
def user_status(request):
    account = None
    data = None
    if 'account' in request.params:
        account =  request.params['account']
    if 'data' in request.params:
        data = request.params['data']
    if account and data:
        data = decript(account, data)
    print(data)
    # TODO execute to update.
    return {}

@notfound_view_config()
def not_found(request):
    return Response(
        body=json.dumps(
            {'code':'404',
             'message':'Endpoint not found'
            }
        ),
        status='404 Not Found',
        content_type='application/json')

