
import _ledger
import _lettercrypto










class Message():
    #time = _ledger.get_time()  #for testing duplicate entries
    time = 1500811295.5641012
    def set_data(self, recipient, sender, subject, body):
        self.recipient = recipient
        self.sender = sender
        self.subject = subject
        self.body = body
    
    def message_out(self):
        return [self.time, self.recipient, self.sender, self.subject, self.body]
    def display_message(self):
        print self.recipient, self.sender, self.subject, self.body, self.time


class peer():
    
    def set_data(self, ip, lastseen, port):
        self.ip = ip
        self.lastseen = lastseen
        self.port = port
        
    def peer_out(self):
        return[self.ip, self.lastseen, self.port]



#Test code below
if __name__ == '__main__':
    
    #x = Message()
    #x.set_data('Bob', 'Alice', 'Pizza','Do you like pizza?' )
    #_ledger.create_database()
    #_ledger.display_peers()
    #_ledger.add_entry(x.message_out())
    #_ledger.create_peers()
    #_ledger.weed()
    #_ledger.display_records()
    #_ledger.create_peers()
   # y = peer()
   # y.set_data('192.168.0.3', 15000000000, 2052)
    #_ledger.add_peer(y.peer_out())
   # _ledger.delete_peer('192.168.0.22')
    #_ledger.display_peers()
    #print _ledger.return_peer('192.168.0.3')
    #print _ledger.find_from('Alice')
    #print _ledger.find_from_to('Alice','Bob') 
    #print _ledger.twentyFour()
    #_ledger.create_nicks()
    #_ledger.add_nick(['Alice', '676789', 'ghggjjjkhjhk', 159000099999])
    #_lettercrypto.create_key('Bob')
    #test =  _lettercrypto.share_pubkey('Bob')
   # print _lettercrypto.verify_nick(test)
    #_lettercrypto.encrypt('Bob', 'This is a test message.')
    _lettercrypto.add_pubkey_ledger('Bob')
    #x = _lettercrypto.share_pubkey('Bob')
    #print x 
    #print _lettercrypto.baseencode(x)
    
    
    
    


    