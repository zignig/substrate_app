#!/usr/bin/python -i 

import M2Crypto , os

import readline,rlcompleter
readline.parse_and_bind('tab:complete')

def fake_callback():
	return 

M2Crypto.Rand.rand_seed (os.urandom (1024))
def key(name='test.pem'):
	try:
		os.stat('test.pem')
		key = M2Crypto.RSA.load_key('test.pem',fake_callback)
		return key
	except:
		test_key = M2Crypto.RSA.gen_key(1024,65537)
		test_key.save_pem('test.pem',None)
		return test_key

k = key()
