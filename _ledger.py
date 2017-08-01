#------------------------------------------------------------------------------------------------------------------------------------
#
#
#                                        This module contains the functions and classes to operate the ledger
#                                        which is a database of messages, public keys/nickname pairs and 
#                                        known nodes, this module will handle all the local side data shuffling.
#
#
#
#-------------------------------------------------------------------------------------------------------------------------------------



import ntplib  #Need network time
import time
import sqlite3
import sys




#--------------------------------------------------------------------------------------------------------------------------------------
#
#                                               Helper functions for the ledger.
#
#--------------------------------------------------------------------------------------------------------------------------------------

def get_time(): # Gets network time for timestamping messages as this fails during testing (probably due to a query limit I'll let this revert to machine time for now)
    try:
        c = ntplib.NTPClient()
        response = c.request('pool.ntp.org')
        return response.tx_time
    except:
        print "unable to obtain network time. Using system time."  #just to warn me ntp is being a bitch.
        return time.time()
        
# Returns a unix time 24 hours prior to calling.  To be used for deleting old messages from the ledger.
def twentyFour():
    seconds_in_day = 86400
    return get_time() - seconds_in_day
        

#----------------------------------------------------------------------------------------------------------------------------------------
#
#                                               The SQLite Database
#
#-----------------------------------------------------------------------------------------------------------------------------------------


# This will open the ledger or create it if it doesn't and then add a table for messages.

# This currently needs to be called for any other database functions as it is the only one to create the database.  May separate this out from the table creation later to make
# it a run once function, then the tables can be created in any order.
def create_database():
    try:
        ledger = sqlite3.connect('ledger.db')
        print "Database Opened"
        myCursor = ledger.cursor()
        myCursor.execute('CREATE TABLE IF NOT EXISTS Messages(Timestamp FLOAT PRIMARY KEY, Recipient TEXT NOT NULL, Sender TEXT NOT NULL, Subject TEXT, Message TEXT)')
        print "Table Created"    
    except sqlite3.Error, e:
        print "Database error %s" % e.args[0]
        if ledger:
            ledger.rollback()
            sys.exit(1)
            
    finally:
        if ledger:
            ledger.close()
            
# Adds a message to the database, takes a list as input with (currently) 5 items. 
#Now checks for a duplicate Timestamp.  However need to check the floating point handling as it looks like it may round the figures
#to two decimal places.  This may not be a bad thing.  No human would be writing messages in millisecons.......
def add_entry(message):
    try:
        ledger = sqlite3.connect('ledger.db')
        print "Database Opened"        
        myCursor = ledger.cursor()
        #print message[0]  Test code
        myCursor.execute("SELECT Timestamp FROM Messages WHERE Timestamp = ?",(message[0],)) #Checking for existence of that timestamp.
        temp = myCursor.fetchall()
        #print temp[0][0]  More test code
        if message[0] == temp[0][0]:
            print "Duplicate Entry."
            return
        else:
            myCursor.execute("INSERT INTO Messages(Timestamp,Recipient,Sender,Subject,Message) VALUES(?,?,?,?,?)", (message[0],message[1],message[2],message[3],message[4]))
            ledger.commit()
            print "Message added"
    except sqlite3.Error, e:
        print "Database error %s" % e.args[0]
        if ledger:
            ledger.rollback()
            sys.exit(1)
                    
    finally:
        if ledger:
            ledger.close() 
            
            
            
            
# Finds all messages to a passed in string.  Returns list of tuples or a string if no records are found.           
def find_for(who):
    try:
        ledger = sqlite3.connect('ledger.db')
        myCursor = ledger.cursor()
        myCursor.execute("SELECT * FROM Messages WHERE Recipient =? ORDER BY Timestamp",(who,))
        result = myCursor.fetchall()
        if not result:
            return "No Records match"
        else:
            return result
              
    except sqlite3.Error, e:
        print "Database error %s" % e.args[0]
        if ledger:
            ledger.rollback()
            sys.exit(1)
                            
    finally:
        if ledger:
            ledger.close()         


# Finds all messages from a passed in string.  Returns a list of tuples or a string if no records are found.            
def find_from(who):
    try:
        ledger = sqlite3.connect('ledger.db')
        myCursor = ledger.cursor()
        myCursor.execute("SELECT * FROM Messages WHERE Sender =? ORDER BY Timestamp",(who,))
        result = myCursor.fetchall()
        if not result:
            return "No Records match"
        else:
            return result        
              
    except sqlite3.Error, e:
        print "Database error %s" % e.args[0]
        if ledger:
            ledger.rollback()
            sys.exit(1)
                            
    finally:
        if ledger:
            ledger.close()        
            
# Finds all messages from a sender to a recipient as a list of tuples, or returns a string if not found.
def find_from_to(fromWho, toWho):
    try:
        ledger = sqlite3.connect('ledger.db')
        myCursor = ledger.cursor()
        myCursor.execute("SELECT * FROM Messages WHERE Sender =? AND Recipient =? ORDER BY Timestamp",(fromWho,toWho,))
        result = myCursor.fetchall()
        if not result:
            return "No Records match"
        else:
            return result        
              
    except sqlite3.Error, e:
        print "Database error %s" % e.args[0]
        if ledger:
            ledger.rollback()
            sys.exit(1)
                            
    finally:
        if ledger:
            ledger.close()        
            
            
            
# Deletes all messages that are over 24 hours old.  

def weed():
    time_limit = twentyFour()
    try:
        ledger = sqlite3.connect('ledger.db')
        myCursor = ledger.cursor()
        myCursor.execute("DELETE FROM Messages WHERE Timestamp < ?",(time_limit,))
        ledger.commit()     
    except sqlite3.Error, e:
        print "Database error %s" % e.args[0]
        if ledger:
            ledger.rollback()
            sys.exit(1)   
       
    finally:
        if ledger:
            ledger.close()


# Function to De-duplicate the database keyed on Timestamp.

#  Shouldn't need this as insert is now self checking.  


#----------------------------------------------------------------------------------------------
#
#                                    A test function to check what's in the db
#                                   
#-----------------------------------------------------------------------------------------------
def display_records():
    try:
        ledger = sqlite3.connect('ledger.db')
        myCursor = ledger.cursor()
        myCursor.execute("SELECT * FROM Messages")
        print myCursor.fetchall()
          
    except sqlite3.Error, e:
        print "Database error %s" % e.args[0]
        if ledger:
            ledger.rollback()
            sys.exit(1)
                        
    finally:
        if ledger:
            ledger.close()        
            
            
#-------------------------------------------------------------------------------------------------
#
#                More sqlite3 stuff to add another table for peer details.
#
#--------------------------------------------------------------------------------------------------


#This function add the Peers table to the existing ledger.db, n.b. the ledger create function needs to be called before this.
def create_peers():
    try:
        ledger = sqlite3.connect('ledger.db')
        print "Database Opened"
        myCursor = ledger.cursor()
        myCursor.execute('CREATE TABLE IF NOT EXISTS Peers(IP_address TEXT PRIMARY KEY, Lastseen FLOAT, Port INT)')
        print "Peers Table Created"    
    except sqlite3.Error, e:
        print "Database error %s" % e.args[0]
        if ledger:
            ledger.rollback()
            sys.exit(1)
            
    finally:
        if ledger:
            ledger.close()


# Function to add a peer record in the database.  If it already exists then it will update the existing.

def add_peer(peer):
    try:
        ledger = sqlite3.connect('ledger.db')
        myCursor = ledger.cursor()
        myCursor.execute("SELECT IP_address FROM Peers WHERE IP_address = ?",(peer[0],)) #Checking for existence of that ip.
        temp = myCursor.fetchone()
        #print temp[0][0]
        if temp and temp[0] == peer[0]:     #if ip exists as a record we update that one.
            myCursor.execute('UPDATE Peers SET Lastseen = ?, Port = ? WHERE IP_address = ?',(peer[1],peer[2],peer[0],))
            ledger.commit()
            print "Peer Record Updated"
        else:
            myCursor.execute('INSERT INTO Peers(IP_address,Lastseen,Port) VALUES(?,?,?)',(peer[0],peer[1],peer[2]))
            ledger.commit()
            print "Peer Record added."
    except sqlite3.Error, e:
        print "Database error %s" % e.args[0]
        if ledger:
            ledger.rollback()
            sys.exit(1)
                        
    finally:
        if ledger:
            ledger.close()          


#Deletes a Peer record based on ip address.
def delete_peer(ip):
    try:
        ledger = sqlite3.connect('ledger.db')
        myCursor = ledger.cursor()
        myCursor.execute('DELETE FROM Peers WHERE IP_address = ?',(ip,))
        ledger.commit()
        print 'Record(s) Deleted.'
    except sqlite3.Error, e:
        print "Database error %s" % e.args[0]
        if ledger:
            ledger.rollback()
            sys.exit(1)
                    
    finally:
        if ledger:
            ledger.close()   
            
# Return Peer function passes out data from a record keyed from the IP address will return a tuple of, ip, lastseen, port

def return_peer(ip):
    try:
        ledger = sqlite3.connect('ledger.db')
        myCursor = ledger.cursor()
        myCursor.execute('SELECT * FROM Peers WHERE IP_address = ?',(ip,))
        temp = myCursor.fetchone()
        return temp
    except sqlite3.Error, e:
        print "Database error %s" % e.args[0]
        if ledger:
            ledger.rollback()
            sys.exit(1)
                    
    finally:
        if ledger:
            ledger.close()       
    
            
# Display Peer table

def display_peers():
    try:
        ledger = sqlite3.connect('ledger.db')
        myCursor = ledger.cursor()
        myCursor.execute("SELECT * FROM Peers")
        print myCursor.fetchall()
          
    except sqlite3.Error, e:
        print "Database error %s" % e.args[0]
        if ledger:
            ledger.rollback()
            sys.exit(1)
                        
    finally:
        if ledger:
            ledger.close()        
            
            
#----------------------------------------------------------------------------------------------------------------------------------------
#
#
#                        Another table for the ledger.db this one will hold the nickname database
#                        that holds the records for nicknames and public keys and a signature which is
#                        the nickname encrypted with the private key to allow for verification.
#
#
#-----------------------------------------------------------------------------------------------------------------------------------------

#This function adds the Peers table to the existing ledger.db, n.b. the ledger create function needs to be called before this.
def create_nicks():
    try:
        ledger = sqlite3.connect('ledger.db')
        print "Database Opened"
        myCursor = ledger.cursor()
        myCursor.execute('CREATE TABLE IF NOT EXISTS Nicks(Nickname TEXT PRIMARY KEY, Pubkey LONG, Signature TEXT, Timestamp LONG)')
        print "Nicks Table Created"    
    except sqlite3.Error, e:
        print "Database error %s" % e.args[0]
        if ledger:
            ledger.rollback()
            sys.exit(1)
            
    finally:
        if ledger:
            ledger.close()
            
            
            
#Function to add an entry to the Nicks table, checks to see if the Nickname exists and if so exits without adding.

def add_nick(nick):
    try:
        ledger = sqlite3.connect('ledger.db')
        myCursor = ledger.cursor()
        myCursor.execute("SELECT Nickname FROM Nicks WHERE Nickname = ?",(nick[0],)) #Checking for existence of that ip.
        temp = myCursor.fetchone()
        if temp == None:
            temp = (0,0,)
        if str(temp[0]) == nick[0]:
            print "Record already exists."
            return
        else:
            myCursor.execute('INSERT INTO Nicks(Nickname, Pubkey, Signature, Timestamp) VALUES(?,?,?,?)',(nick[0],nick[1],str(nick[2]),get_time()))
            ledger.commit()
            print "Nickname added."
    except sqlite3.Error, e:
        print "Database Error %s" % e.args[0]
        if ledger:
            ledger.rollback()
            sys.exit(1)
    finally:
        if ledger:
            ledger.close()
            
            
# Function returns the entry for nickname.

def get_nick(nick):
    try:
        ledger = sqlite3.connect('ledger.db')
        myCursor = ledger.cursor()
        myCursor.execute("SELECT * FROM Nicks WHERE Nickname = ?",(nick,)) #Checking for existence of that ip.
        return myCursor.fetchone()
        
    except sqlite3.Error, e:
        print "Database Error %s" % e.args[0]
        if ledger:
            ledger.rollback()
            sys.exit(1)
    finally:
        if ledger:
            ledger.close()
            
            
            
            
            
            
            
            
            
            
            
            
#---------------------------------------------------------------------------------------------------------------------------------------------
#
#
#                                        For functionality will add address book
#                                        This will be purely local storage of the Nicks database
#                                        for received and sent "addresses"
#                                        Will be used to warn if pub key changes to prevent
#                                        MITM attacks
#
#----------------------------------------------------------------------------------------------------------------------------------------------
























#-------------------------------------------------------------------------------------------------------------------------------------------------
#
#
#                                     WIll add a saved messages table
#                                     in this received messages will be saved
#                                     encrypted by users pub key as well copies of
#                                     sent messages.
#
#
#---------------------------------------------------------------------------------------------------------------------------------------------------