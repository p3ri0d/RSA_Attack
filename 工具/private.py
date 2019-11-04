import math
import sys
from Crypto.PublicKey import RSA

keypair = RSA.generate(1024)

keypair.p = 290579950064240059571837821251441436997
keypair.q = 314436328879392457343835667929324128609
keypair.e = 65537

keypair.n = keypair.p * keypair.q
Qn = long((keypair.p-1) * (keypair.q-1))

i = 1
while (True):
    x = (Qn * i ) + 1
    if (x % keypair.e == 0):
        keypair.d = x / keypair.e
        break
    i += 1

private = open('private.pem','w')
private.write(keypair.exportKey())
private.close() 