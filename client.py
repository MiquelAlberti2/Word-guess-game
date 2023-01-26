#!/usr/bin/env python3

import json
import socket
import sys
import ssl


class Client:
    
    def __init__(self, name):
        self.id = None
        self.username = name
        self.bye= False
        self.error = False

        with open('project1-words.txt', 'r') as f:
            self.words = f.read().splitlines()
        
        self.index = 0  #index of the list of words
        self.word_guess = [None, None, None, None, None]
        self.wrong_letters=set()
        self.right_letters=set()


    def hello_message(self):
        msg = {
            "type" : "hello",
            "northeastern_username" : self.username
        }

        notif = '{ "type": "hello",' + ' "northeastern_username": "' + self.username +'"}\\n'
        #print('C -> S: ' + notif)

        return json.dumps(msg)

    def guess_message(self, word):
        msg = {
            "type": "guess",
            "id": self.id , 
            "word": word
        }

        notif = '{ "type": "guess",' + ' "id": "' + str(self.id) + '", "word": "' + word + '"}\\n'
        #print('C -> S: ' + notif)

        return json.dumps(msg)

    def read_and_respond_message(self, message):
        msg = json.loads(message) #msg now is a python dictionary


        if msg["type"] == "start":
            self.id = msg["id"]
            #the first guess is the first word of the list
            return self.guess_message(self.words[0])
            
        elif msg["type"] == "retry":
            self.index += 1

            #update the information I know about the guessed word
            self.update_guess(msg["guesses"][-1]["word"], msg["guesses"][-1]["marks"])

            #look for the next word candidate
            while not self.word_candidate(self.words[self.index]):
                self.index += 1

            return self.guess_message(self.words[self.index])
            
        elif msg["type"] == "bye":
            self.bye = True
            return msg["flag"]

        else: #error
            self.error = True
            return msg["message"]


    def update_guess(self, word, mark):
        
        for i in range(5):
            if mark[i] == 0 and word[i] not in self.right_letters:
                self.wrong_letters.add(word[i])
            elif mark[i] == 1:
                self.right_letters.add(word[i])
                if word[i] in self.wrong_letters:
                    self.wrong_letters.remove(word[i])
            elif mark[i] == 2:
                self.word_guess[i] = word[i]
                self.right_letters.add(word[i])
                if word[i] in self.wrong_letters:
                    self.wrong_letters.remove(word[i])



    def word_candidate(self, word):

        #check if the word has no wrong letters
        for letter in word:
            if letter in self.wrong_letters:
                return False

    
        #check if the word has all the right letter
        for letter in self.right_letters:
            if letter not in word:
                return False


        #check the positions of the letters we know
        for i in range(5):
            if self.word_guess[i]: #different from None
                if self.word_guess[i] != word[i]:
                    return False 


        return True



###############################################################
#"main"
###############################################################
def mysend(sock, msg_str):
    msg_str = msg_str + '\n'
    msg = bytes(msg_str, 'utf-8')
    length = len(msg)
    totalsent = 0
    while totalsent < length:
        sent = sock.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent


hostname = sys.argv[-2]
northeastern_username = sys.argv[-1]
port = 27993 #default value
tls = False

#Check optional parameters
if sys.argv[1] == "-s" or (len(sys.argv) > 3 and sys.argv[3] == "-s"):
    tls = True
    port = 27994 #default value if TLS

if sys.argv[1] == "-p":
    port = int(sys.argv[2])


if tls:
    context = ssl.create_default_context()
    so = socket.create_connection((hostname, port))
    s = context.wrap_socket(so, server_hostname=hostname)
else:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))



client = Client(northeastern_username)
exit = False

mysend(s, client.hello_message())


while not exit:

    r=''
    r = s.recv(1024).decode('UTF-8')
    while not r.endswith('\n'):
        r += s.recv(1024).decode('UTF-8')

    #print('S -> C: ' + r)
    respond = client.read_and_respond_message(r)

    if client.bye or client.error:
        print(respond)
        exit = True
    else:
        mysend(s, respond)

if tls:
    so.close()
s.close()


