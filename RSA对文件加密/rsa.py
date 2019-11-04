# -*- coding: utf-8 -*-
import gmpy2
import random
import binascii

# 欧几里得算法
def gcd(a,b):
	while a != 0:
		a, b = b%a, a
	return b

# 根据 p q d 求 d
def egcd(a,b):
    if a == 0:
      return (b, 0, 1)
    else:
      g, y, x = egcd(b % a, a)
      return (g, x - (b // a) * y, y)
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
      raise Exception('modular inverse does not exist')
    else:
      return x % m

# hex 字符串转化为大整数
def hex2int(s):
	dict = {'a': 10, 'c': 12, 'b': 11, 'e': 14, 'd': 13, 'f': 15, '1': 1, '0': 0, '3': 3, '2': 2, '5': 5, '4': 4, '7': 7, '6': 6, '9': 9, '8': 8}
	t = len(s)-1
	sum = 0
	for i in range(len(s)):
		sum = sum + (dict[s[t-i]]*(16**i))
	return sum

# 生成 p q [e, d]
def init():

	# 初始化
	p = 0
	q = 0

	# 随机生成素数
	while (p-1)*(q-1)<65536:
		p = gmpy2.next_prime(random.randint(9000,10000))
		q = gmpy2.next_prime(random.randint(9000,10000))

		print u'随机生成的 p={0} q={1}'.format(p,q)

	# 随机生成 10 组 [e,d]
	key = [] 
	r = (p-1)*(q-1)

	while len(key)!=10:
		t = random.randint(65537, r)
		if gcd(t,r)==1 :
			e = t
			d = modinv(e, r)
			key.append([e,d])


	print u'生成的10组密钥为: '
	print key
	return p,q,key

# 明文处理, 每 3 个字符一组
def div_m(path):
	f = open(path,'r')
	s = ''
	for line in f:
		line = line.strip()
		s = s +  line
	s = binascii.b2a_hex(s)
	r = [s[i:i+6] for i in range(0,len(s),6)]
	f.close()
	return r
	# print r

# 加密
def rsa_encrypto(path,enc_path):
	global p,q,e

	r = div_m(path)

	# 加密，将密文输出到 enc_path
	for i in range(len(r)):
		r[i] = pow(hex2int(r[i]),e,int(p*q))

	f = open(enc_path, 'w')
	for i in r:
		f.write(str(i))
		f.write('\n')
	f.close()

# 解密
def rsa_decrypto(enc_path, dec_path):
	global p,q,d
	f1 = open(enc_path, 'r')
	f2 = open(dec_path, 'w')
	m = []
	for line in f1:
		line = line.strip()
		m.append(binascii.unhexlify(hex(pow(int(line),d,p*q))[2:]))

	f2.write(''.join(m))
	f1.close()
	f2.close()

# RSA 初始化
p,q,key = init()
choice = input('Select the key, enter sequence number from 0: ')
e = key[int(choice)][0]
d = key[int(choice)][1]
print u'选择的 p={0} q={1} e={2} d={3}'.format(p,q,e,d)

# rsa_encrypto('C:\Users\peri0d\Desktop\test.txt','C:\Users\peri0d\Desktop\test2.txt')
path = str(raw_input('Please enter the file path you want to encrypto: '))
enc_path = str(raw_input('Please enter path you want to save the ciphertext: '))
try:
	rsa_encrypto(path,enc_path)
except Exception as e:
	print 'somethin error'

dec_path = str(raw_input('Please enter path you want to save the plaintext: '))

# rsa_decrypto('C:\Users\peri0d\Desktop\test2.txt','C:\Users\peri0d\Desktop\test3.txt')
try:
	rsa_decrypto(enc_path,dec_path)
except Exception as e:
	print 'somethin error'