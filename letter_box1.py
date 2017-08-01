
import _ledger
import _lettercrypto










class Message():
    time = _ledger.get_time()  #for testing duplicate entries
    SENDER = '[SENDER]'
    SUBJECT = '[SUBJECT]'
    BODY = '[BODY]'
    def set_data(self, recipient, sender, subject, body):
        self.recipient = recipient
        self.sender = sender
        self.subject = subject
        self.body = body
    
    def message_out(self):
        return [self.time, self.recipient, self.sender, self.subject, self.body]
    def display_message(self):
        print self.recipient, self.sender, self.subject, self.body, self.time
    def message_out_4_encryption(self):
        body = '[SENDER]' + str(self.sender) + '[SUBJECT]' + str(self.subject + '[BODY]' + self.body)
        return (self.recipient, body)

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
    #print x.message_out_4_encryption()
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
    #_lettercrypto.create_key('Alice')
    _lettercrypto.add_pubkey_ledger(_lettercrypto.share_pubkey('Bob'))
    _lettercrypto.add_pubkey_ledger(_lettercrypto.share_pubkey('Alice'))
    #test =  _lettercrypto.share_pubkey('Bob')
   # print _lettercrypto.verify_nick(test)
    #_lettercrypto.encrypt('Bob', 'This is a test message.')
    #_lettercrypto.add_pubkey_ledger(('Bob', '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApx4iD2bNKTOw5q0sXhxv\ngZajM9tNCGx/qfEPT0AXihS+TdEms0x/M5uCdJ2WJcMaP15RWHXROnftZUz14G9Z\nmN+wPgb/ANKM4NBhZ4bY9+jXYkMkkrkuP1OHSXd7mK7iimkBI0J8FzISVqzPe1M4\n7ujVj5FYeJU2843HA7Q90AmhfpiQyQxO1jzygl68BSYcgTGxHLKR4camrmiPvAqe\n3OSKimhCmnfuqABe1ulF7BXQ6x03wAldm7OvZX3ahe2r5Qm3yCZHrt0j7v7OHd0s\nb+p1vuJfRm9Jl+QJ0xhPGwYyXKROkBTw8XxFq7QwWtCykO8kCLUKKAznYc3TXvga\nswIDAQAB\n-----END PUBLIC KEY-----', 'GrGZSN9Z1QffIJUyZ6Wfqj63uEoUeH9utm7OvyWjyyNks7ZAxJaotAeQGZ5FA505/WdZCZHuVqeInSu/ITZUjacF3yzkcEhAHfOszO+DHAoyxa/muEXVwKnf/dj7jQyVcpLwQvKx8QDMDu4Z5duTsIhtM+elDg+ISs8uWcDr1HmjfZM8ETeyywD3TpIE3utlVc7rlvvhCrqxUCUgibv9hXjIkyacnbqcEl21klnF4c/g9X+q1WfdmYxjmSxWJEhKoIuKm4qavSB24a42Ubwh1bciatKtYnaXN2hJWR3UF13gLQS1xAzwJP8DS6EFjkOgWOtCW89LiQWL2Y3TuzrYGQ=='))
    #print _ledger.get_nick('Bob')
    #_lettercrypto.encrypt('Bob','This is a test')
    #x = _lettercrypto.share_pubkey('Bob')
    #print x 
    #print _lettercrypto.baseencode(x)
    x = _lettercrypto.encrypt('Bob', 'This is a test. If you are reading this then encryption and decryption work!')
    print _lettercrypto.decrypt(x)
     
    
    
    
    


    