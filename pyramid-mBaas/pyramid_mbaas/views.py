
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
    signup,
    decrypt,
    encrypt,
)
from .manager import (
    get_user,
)

@view_config(route_name='sign_up', request_method='POST', renderer='json')
def sign_up(request):
    seed = None
    if 'hash' in request.params:
        seed =  request.params['hash']
        result = signup(seed)
        if result:
            return Response( body=json.dumps(
                {'code':'200',
                 'message':'login successfull',
                 'user_id':result['user_id'],
                 'seed'   :result['seed'],
                 'vector' :result['vector']
                 }
            ),
            status = '200 OK',
            content_type='application/json')

    return Response(
        body=json.dumps(
            {'code':'403',
             'message':'Invalied request'
            }
        ),
        status = '403 forbidden',
        content_type='application/json')

@view_config(route_name='user_status', request_method='POST', renderer='json')
def user_status(request):
    user_id = None
    if 'user_id' in request.params:
        user_id =  request.params['user_id']
        user = get_user(user_id)
        if user:
            data = user.name
            print('#'*30)
            print(data)
            print('#'*30)
            data = encrypt(user_id, data)
            print('#'*30)
            print(data)
            print('#'*30)
            return Response( 
                body=json.dumps(
                    {
                    'code':'200',
                    'message':'valied',
                    'data'   : data,
                    }
                ),
                status = '200 OK',
                content_type='application/json'
            )

    return Response(
        body=json.dumps(
            {'code':'403',
             'message':'invalied'
            }
        ),
        status = '403 forbidden',
        content_type='application/json'
    )

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

