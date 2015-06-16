
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
from .response import (
    ForbiddenResponse,
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
    update_user,
)

import json

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

    return ForbiddenResponse

@view_config(route_name='update', request_method='POST', renderer='json')
def update(request):
    user_id = None
    data    = None
    if 'user_id' in request.params and 'data' in request.params:
        user_id = request.params['user_id']
        data    = request.params['data']

        data    = decrypt(user_id, data.decode('hex'))
        data    = data.strip()
        try:
            data = json.loads(data)
        except(ValueError):
            return ForbiddenResponse
        name = None
        rank = None
        HP   = None
        if 'name' in data:
            name = data['name']
        if 'rank' in data:
            rank = data['rank']
        if 'HP' in data:
            HP   = data['HP']
        if name or rank or HP:
            result = update_user(user_id=user_id, name=name, rank=rank, HP=HP)
            if result:
                return Response( 
                    body=json.dumps(
                        {
                        'code':'200',
                        'message':'update successful',
                        }
                    ),
                    status = '200 OK',
                    content_type='application/json'
                )
    return ForbiddenResponse


@view_config(route_name='user_status', request_method='POST', renderer='json')
def user_status(request):
    user_id = None
    if 'user_id' in request.params:
        user_id =  request.params['user_id']
        user = get_user(user_id)
        if user:
            data = user.name
            data = encrypt(user_id, data).encode('hex')
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

    return ForbiddenResponse

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

