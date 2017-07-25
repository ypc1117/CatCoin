import os
import ecdsa
import ecdsa.ecdsa
import hashlib
from ecdsa.ecdsa import curve_secp256k1, generator_secp256k1
from ecdsa.curves import SECP256k1
from ecdsa.ellipticcurve import Point
from ecdsa.util import string_to_number, number_to_string

ADDRTYPE_P2PKH = 28
ADDRTYPE_P2SH = 5
ADDRTYPE_P2WPKH = 6

__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
assert len(__b58chars) == 58


def Hash(x):
    if type(x) is unicode: x=x.encode('utf-8')
    return sha256(sha256(x))

def base_encode(v, base):
    """ encode v, which is a string of bytes, to base58."""
    if base == 58:
        chars = __b58chars
    elif base == 43:
        chars = __b43chars
    long_value = 0L
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

def sha256(x):
    return hashlib.sha256(x).digest()

def hash_160(public_key):
    md = hashlib.new('ripemd')
    md.update(sha256(public_key))
    return md.digest()

def point_to_ser(P, comp=True ):
        if comp:
            return ( ('%02x'%(2+(P.y()&1)))+('%064x'%P.x()) ).decode('hex')
        return ( '04'+('%064x'%P.x())+('%064x'%P.y()) ).decode('hex')

def public_key_to_p2pkh(public_key):
    return hash160_to_p2pkh(hash_160(public_key))

def hash160_to_p2pkh(h160):
    return hash_160_to_bc_address(h160, ADDRTYPE_P2PKH)

def hash_160_to_bc_address(h160, addrtype, witness_program_version=1):
    s = chr(addrtype)
    if addrtype == ADDRTYPE_P2WPKH:
        s += chr(witness_program_version) + chr(0)
    s += h160
    return base_encode(s+Hash(s)[0:4], base=58)

G = generator_secp256k1
_r = G.order()
pvk = ecdsa.util.randrange( pow(2,256) ) %_r
Pub = pvk*G
pubkey_c = point_to_ser(Pub,True)
addr_c = public_key_to_p2pkh(pubkey_c)[:]
print addr_c 
