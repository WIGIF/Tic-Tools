#!/usr/bin/python3

from Crypto.PublicKey import RSA
from argparse import ArgumentParser
from urllib.request import urlopen
from json import loads
from sys import argv

def factordb(n):
    with urlopen(f"http://factordb.com/api?query={n}") as req :
        if req.code == 200 :
            data = loads(req.read())["factors"]
            print(f"Factors of {n} : {', '.join([i[0] for i in data])}")
        else: print(f"FactorDB : Error {req.code}") 

def generate_coef(p,q,e):
    n = p * q
    phi =(p-1) * (q-1)
    d = pow(e,-1,phi)
    return (n, phi, d)

def printPEM(pvkey, pubkey):
    print('Public key:\n', pubkey)
    print('Private key:\n', pvkey)

def printKey(e,n,d):
    publicKey = (n, e)
    privateKey = (n, d)
    print('Public key:\n', publicKey)
    print('Private key:\n', privateKey)

def createPEM(e,n,d):
    privateKey = RSA.construct((n, e, d))
    privateKeyPem = privateKey.exportKey(pkcs=8).decode()
    publicKey = RSA.construct((n, e))
    publicKeyPem = publicKey.exportKey().decode()
    return (privateKeyPem,publicKeyPem)

def writeKey(pvkey, pubkey, name):
    with open(f"pv_{name}.pem","w") as file:
        file.write(pvkey)
    with open(f"pub_{name}.pem","w") as file:
        file.write(pubkey)


if __name__ == "__main__" :
    parser = ArgumentParser()
    parser.add_argument("-p", help="value of p", type=int, required=('-f' not in argv))
    parser.add_argument("-q", help="value of q", type=int, required=('-f' not in argv))
    parser.add_argument("-e", help="value of exponant", type=int, default=65537)
    parser.add_argument("-f", help="FactorDB request for n", type=int)
    parser.add_argument("-v","--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("--hex", help="use hex value for (p, q, e) or n", action="store_true")
    parser.add_argument("--export", help="export key named with value", type=str)
    args = parser.parse_args()
    
    if not args.f :
        p, q, e = (args.p, args.q, args.e)
        if args.hex : p, q, e = (int(p,16), int(q,16), int(e,16))
        n, phi, d = generate_coef(p,q,e)
        if args.verbose : printKey(e,n,d)
        pvkey, pubkey = createPEM(e,n,d)
        if args.verbose : printPEM(pvkey, pubkey)
        if args.export : writeKey(pvkey, pubkey, args.export)
    else :
        n = args.f 
        if args.hex : n = int(n,16)
        factordb(n)
