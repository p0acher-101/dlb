#-------------------------------------------------------------------------------------------------------------------------------------
#
#
#                                        _lettercrypto.py module
#                                         module to handle all cryptographic functions
#                                         and character encoding for the programme.
#
#
#--------------------------------------------------------------------------------------------------------------------------------------


#Uses the pyCrypto module.
import _ledger
import Crypto
import base64
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256


KEY_LENGTH = 2048



#-------------------------------------------------------------------------------------------------------------------------------------
#
#
#                                              Helper fucntions
#
#
#-------------------------------------------------------------------------------------------------------------------------------------


def baseencode(stuff):
    output = ()
    for element in stuff:
        output += base64.b64encode(element)
    return output

        

# Vreates an RSA Key pair.  Uses the pyCrypto random function.  Saves the key to a pemfile.  This function takes a while to run
# But is not going to be run that often.  I.e. only run to create and identity.
def create_key(name):
    random_generator = Random.new().read
    key = RSA.generate(KEY_LENGTH, random_generator)
    try:
        f = open(str(name)+'.pem','w')
        f.write(key.exportKey('PEM'))
        f.close()
        print "Key Saved"
    except:
        print 'File Error.'
    finally:
        if f:
            f.close()
   
    

#Reads back into memory a pre-generated RSA key pair that has been locally saved to a pem file.
def get_key(name):
    try:
        f = open(str(name)+'.pem','r')
        key = RSA.importKey(f.read())
        f.close()
    except:
        print 'Key File read error'
    finally:
        if f:
            f.close()
    return key 



# Exports a public key along with an associated nickname and a signed version of the nickname as a tuple.  
# In a format that can be passed to the add_nick() function.
def share_pubkey(name):
    key = get_key(name)
    pubkey = key.publickey()
    pkey_out = pubkey.exportKey()
    h = SHA256.new(str(name))
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(h)
    return (name, pkey_out, signature)

def add_pubkey_ledger(name):
    x = share_pubkey(name)
    if verify_nick(x):
        _ledger.add_nick(x)
        print x
    else:
        return
    
    
# Takes as input a tuple of a nickname entry (nick, publickey, signature) and returns true if the signature is verified.

def verify_nick(nick):
    key = RSA.importKey(str(nick[1]))
    h = SHA256.new(str(nick[0]))
    verifier = PKCS1_v1_5.new(key)
    return verifier.verify(h, str(nick[2]))
    
    
    
def encrypt(to, message_text):
    key = get_key('Bob')
    entry = _ledger.get_nick(to)
    