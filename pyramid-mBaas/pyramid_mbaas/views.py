
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


@view_config(route_name='sign_up', request_method='POST', renderer='json')
def sign_up(request):
    account = None
    data = None
    if 'account' in request.params:
        account =  request.params['account']
    if 'data' in request.params:
        data = request.params['data']

    if account and data:
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
        print("AC:"+account+" data:"+data)
        data = decrypt(account, data.decode('hex'))
        print('#'*30)
        print(data)
        print('#'*30)
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

