
from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    User,
)
from .key import ( 
    secret_key,
)
import hashlib

from Crypto.Cipher import AES

GROUPS = {
    'user':['group:users'],
    'admin':['group:admins'],
}

secret_key = hashlib.sha256('This is secret passphrase.').digest()


def authenticate(crypt_data, seed):

    try:
        aes = AES.new(secret_key(), AES.MODE_CBC, iv)
        name, passwd = aes.decrypt( crypt_data).split(":")
        user = DBSession.query(User).filter(User.name == name).first()
    except DBAPIError:
        return False

    if not user:
        return False
    
    if user.passwd == hashlib.md5(passwd).hexdigest():
        return True
    return False

def groupfinder(name, request):
    try:
        user = DBSession.query(User).filter(User.name == name).one()
    except DBAPIError:
        return []   
 
    if user:
        return GROUPS.get(user.group, [])


