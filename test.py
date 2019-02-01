
import config
import socket
import time
s = socket.socket()

HOST = config.host
PORT = config.port
NICK = config.nick
PASS = config.oauth
CHANNEL = 'artimus83'
username = 'Twitch'
message = ''
meta = ''


s.connect((HOST, PORT))
s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))

s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
s.send(bytes("JOIN #" + CHANNEL + " \r\n", "UTF-8"))
print("Erfolgreiche Verbindung zu Channel " + CHANNEL)

s.send(bytes("CAP REQ :twitch.tv/membership" + "\r\n", "UTF-8"))
s.send(bytes("CAP REQ :twitch.tv/tags" + "\r\n", "UTF-8"))
s.send(bytes("CAP REQ :twitch.tv/commands" + "\r\n", "UTF-8"))
log = open ('log.txt','a')
while True:

    chat = str(s.recv(1024)).split('\\r\\n')
    for line in chat:
        parts = line.split('PRIVMSG #' + CHANNEL + ' :')
        if len(parts) >= 2:
            meta = parts[0]
            message = parts[1]
            print(parts[1])
        else:
            print(parts)
        '''
        if len(parts) <3:
            continue

        #usernamesplit = parts[1].split("!")
        #username = usernamesplit[0]
        zaeler = 0
        for object in parts[0].split(';'):
            print(object)
            if 'display-name' in object:
                print('gefunden')
                username = object.split('=')[1]
            zaeler += 1
        print(username)
        '''
