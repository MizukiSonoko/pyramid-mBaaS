from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    )

from .endpoint import (
    VERSION,
    )


@view_config(route_name='login', request_method='POST', renderer='json')
def login(request):
    return {}

