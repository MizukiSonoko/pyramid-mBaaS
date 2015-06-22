
from pyramid.response import Response
import json

ForbiddenResponse = Response(
    body=json.dumps(
    {'code':'403',
        'message':'Invalied request'
    }
    ),
    status = '403 forbidden',
    content_type = 'application/json'
)
