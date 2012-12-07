# Wrapper to use the Blowfish Crypto
from blowfish import Blowfish

class Crypto:
    def __init__(self, key):
        self.key = key
        self.cipher = Blowfish(self.key)
        
    def encrypt(self, data):
        return "".join([self.cipher.encrypt(pad(data[i:i + 8], 8)).encode('hex') for i in xrange(0, len(data), 8)])
    
    def decrypt(self, data):
        return "".join([self.cipher.decrypt(pad(data[i:i + 16].decode('hex'), 8)) for i in xrange(0, len(data), 16)]).rstrip('\x08')

def pad(s, l):
    return s + "\0" * (l - len(s))
