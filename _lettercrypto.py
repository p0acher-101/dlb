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
import ast


KEY_LENGTH = 2048



#-------------------------------------------------------------------------------------------------------------------------------------
#
#
#                                              Helper fucntions
#
#
#-------------------------------------------------------------------------------------------------------------------------------------


        

# Creates an RSA Key pair.  Uses the pyCrypto random function.  Saves the key to a pemfile.  This function takes a while to run
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
    #We now have to base64 encode the signature to avoid problems
    signature_enc = str(base64.b64encode(signature))
    return (name, pkey_out, signature_enc)


#Confusion here as to adding public keys, need distinct functions for adding ones own public key as opposed to adding an entry. This is avoided if this function 
#can do both.  As it stands, we can call this fucntion with it being passed the output of share_pubkey or a tuple of three elements. 
#Adds a public key to the nicks table, only adds if the signature matches and _ledger.add_nick() function checks for duplicates.
def add_pubkey_ledger(name):
    if verify_nick(name):
        _ledger.add_nick(name)
    else:
        return
    
    
# Takes as input a tuple of a nickname entry (nick, publickey, signature) and returns true if the signature is verified.

def verify_nick(nick):
    #Convert the signature back from base 64 first.
    signature_dec = str(base64.b64decode (nick[2]))
    key = RSA.importKey(str(nick[1]))
    h = SHA256.new(str(nick[0]))
    verifier = PKCS1_v1_5.new(key)
    return verifier.verify(h, str(signature_dec))
    
    
# Function to encrypt a message using a specified public key from the nicks table. Outputs a tuple of the to nick and encrypted message.  
def encrypt(to, message_text):
    entry = _ledger.get_nick(to)
    key = RSA.importKey(str(entry[1]))
    enc_message = key.encrypt(message_text,32)
    #Base64 encode the message for output
    double_enc = base64.b64encode(str(enc_message))
    return (to,double_enc,)


# Decrypts a message taking a tuple as input of "to" and encrypted message.
def decrypt(message):
    try:
        key = get_key(message[0])
    except:
        print "No corresponing private key"
        return
    enc_message = base64.b64decode(str(message[1]))
    decoded_message = key.decrypt(ast.literal_eval(str(enc_message)))
    return decoded_message
    
    
    
    
    
        
    