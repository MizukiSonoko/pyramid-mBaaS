# -*- coding: utf-8 -*-

from pyramid.response import Response
import json

from .security import key_gen


def OkResponse(data=''):
    body = {
            'code':'200',
            'message':'update successful',
            'data':data,
    }
    body.update(key_gen())
    res = Response(
        body=json.dumps(body),
        status = '200 OK',
        content_type='application/json'
    )
    return res

ForbiddenResponse = Response(
    body=json.dumps(
    {'code':'403',
        'message':'Invalied request'
    }
    ),
    status = '403 Forbidden',
    content_type = 'application/json'
)

NotFoundResponse = Response(
    body=json.dumps(
        {'code':'404',
         'message':'Endpoint not found',
        }
    ),
    status='404 Not Found',
    content_type='application/json'
)
