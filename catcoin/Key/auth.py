import os,json,time
import logging

logging.basicConfig(level=logging.INFO)

from datetime import datetime
from aiohttp import web
import hashlib
import ecdsa
from ecdsa.ecdsa import *
from ecdsa.ecdsa import curve_secp256k1, generator_secp256k1
from ecdsa.curves import SECP256k1
from ecdsa.ellipticcurve import Point
from ecdsa.util import string_to_number, number_to_string
from random import SystemRandom

__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
assert len(__b58chars) == 58

url = "http://10.10.0.99:9000/"

def sha256(x):
    return hashlib.sha256(x).digest()

def Hash(x):
    if type(x) is unicode: x=x.encode('utf-8')
    return sha256(sha256(x))


def base_encode(v, base):
    """ encode v, which is a string of bytes, to base58."""
    if base == 58:
        chars = __b58chars
    elif base == 43:
        chars = __b43chars
    long_value = 0
    for (i, c) in enumerate(v[::-1]):
        long_value += (256**i) * ord(c)
    result = ''
    while long_value >= base:
        div, mod = divmod(long_value, base)
        result = chars[mod] + result
        long_value = div
    result = chars[long_value] + result
    # Bitcoin does a little leading-zero-compression:
    # leading 0-bytes in the input become leading-1s
    nPad = 0
    for c in v:
        if c == '\0': nPad += 1
        else: break
    return (chars[0]*nPad) + result

def EncodeBase58Check(vchIn):
    hash = Hash(vchIn)
    return base_encode(vchIn + hash[0:4], base=58)

def point_to_ser(P, comp=True ):
    if comp:
        return ( ('%02x'%(2+(P.y()&1)))+('%064x'%P.x()) ).decode('hex')
    return ( '04'+('%064x'%P.x())+('%064x'%P.y()) ).decode('hex')

def ECC_YfromX(x,curved=curve_secp256k1, odd=True):
    _p = curved.p()
    _a = curved.a()
    _b = curved.b()
    for offset in range(128):
        Mx = x + offset
        My2 = pow(Mx, 3, _p) + _a * pow(Mx, 2, _p) + _b % _p
        My = pow(My2, (_p+1)/4, _p )

        if curved.contains_point(Mx,My):
            if odd == bool(My&1):
                return [My,offset]
            return [_p-My,offset]
    raise Exception('ECC_YfromX: No Y found')

def ser_to_point(Aser):
    curve = curve_secp256k1
    generator = generator_secp256k1
    _r  = generator.order()
    assert Aser[0] in ['\x02','\x03','\x04']
    if Aser[0] == '\x04':
        return Point( curve, string_to_number(Aser[1:33]), string_to_number(Aser[33:]), _r )
    Mx = string_to_number(Aser[1:])
    return Point( curve, Mx, ECC_YfromX(Mx, curve, Aser[0]=='\x03')[0], _r )   

def generate_keypairs():    
    randrange = SystemRandom().randrange
    g = generator_secp256k1
    n = g.order()
    secret = randrange(1,n)
    pubkey = Public_key(g,g*secret)
    privkey = Private_key(pubkey,secret)
    xpub = point_to_ser(pubkey.point,True).encode('hex')
    return privkey,xpub

def generate_sin(xpub):    
    h = hashlib.new('ripemd160')
    h.update(hashlib.sha256(xpub).hexdigest())
    h1 =  "0f02"+h.hexdigest()
    print(h1)
    checksumTotal =  hashlib.sha256(hashlib.sha256(h1).hexdigest()).hexdigest()
    checksum = checksumTotal[0:4]
    sin =  base_encode(h1+checksum,base=58)
    return sin

    
def generate_signature(privkey,url):
    randrange = SystemRandom().randrange
    g = generator_secp256k1
    n = g.order()
    secret = randrange(1,n)
    signature = privkey.sign(int(url.encode("hex"),16),n/10) 

    return signature

def generate_verfication(xpub,url,signature):

    g = generator_secp256k1
    pubkey = Public_key(g,ser_to_point(xpub.decode('hex')))
    return pubkey.verifies(int(url.encode('hex'),16),signature)

def login(xpub):
    sin = generate_sin(xpub)
    try:
        if sin in database:
            logger.info("Login Successfully")
        else:
            logger.info("Error")
    except Exception as ex:
        logger.error(traceback.print_exc())
                     



def handle_login(request):
    try:
        params = await request.json()
        xpub = params['xpub']
        return web.Response(text=json.dumps(await login(xpub)))

    except Exception as ex:
        logger.error(traceback.print_exc())
        return web.Response(text=json.dumps({
            'status': 'failture',
            'errmsg': '服务器未知错误'
        }))

def register(username):
    privkey,xpub = generate_keypairs()

    x_signature = generate_signature(privkey,url)
    signature = Signature(x_signature.r,x_signature.s)  
    if generate_verfication(xpub,url,signature):
        sin = generate_sin(xpub)
            ##insert into database
    else:
        print("INVAILD SIGNATURE")                 



def handle_register(request):
    try:
        params = await request.json()
        username = params['username']
        return web.Response(text=json.dumps(await register(username)))

    except Exception as ex:
        logger.error(traceback.print_exc())
        return web.Response(text=json.dumps({
            'status': 'failture',
            'errmsg': '服务器未知错误'
        }))



def index(request):
    return web.Response(body=open("login.html","rb").read(),content_type='text/html',charset='UTF-8')

def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET','/',index)
    app.router.add_route('POST','/register/',handle_register)
    app.router.add_route('POST','/login/',handle_login)
    srv = await loop.create_server(app.make_handler(),'127.0.0.1',9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()    
