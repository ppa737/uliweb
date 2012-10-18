from uliweb import settings
from uliweb.utils.common import import_attr
from hashlib import md5

def get_cipher(key=None):
    """
    Get cipher object, and then you can invoke:
        des = get_cipher()
        d = des.encrpy('Hello')
        print des.descrpy(d)
    """
    des_func = import_attr(settings.SECRETKEY.CIPHER_CLS)
    kwargs = settings.SECRETKEY.CIPHER_ARGS
    
    if not key:
        key = get_cipher_key()
    cipher = des_func(key, **kwargs)
    return cipher

def get_key():
    """
    Read the key content from secret_file
    """
    with file(settings.SECRETKEY.SECRET_FILE, 'rb') as f:
        return f.read()
    
def get_cipher_key():
    """
    Create key which will be used in des, because des need 8bytes chars
    """
    _key = get_key()
    _k = md5(_key).hexdigest()
    key = xor(_k[:8], _k[8:16], _k[16:24], _k[24:])
    return key
    
def xor(*args):
    arg1 = args[0]
    for arg in args[1:]:
        s = []
        for i, ch in enumerate(arg):
            s.append(chr(ord(arg1[i]) ^ ord(ch)))
        arg1 = ''.join(s)
    return arg1