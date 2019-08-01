
import config
import socket
import time
import  twitchio

import time
s = socket.socket()

HOST = config.host
PORT = config.port
NICK = config.nick
PASS = config.oauth
CHANNEL = 'sparkofphoenixtv'
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
log = open ('test_' + CHANNEL + '_log.txt','a')
strat =  time.time()

def get_message():
    return s.recv(1024).decode("utf-8")
user = []

while (time.time() - strat) < 60 * 5:
    '''
    message = get_message()
    print(message)
    #log.writelines(str(message))
    log.write(str(message)+'\r\n')
    '''

    #chat = str(s.recv(1024)).split('\\r\\n')#.index()
    chat = str(s.recv(1024).decode("utf-8")).split('\\r\\n')#.remove("b'")
    print(chat)

    for line in chat:
        if "JOIN" in line or "PART" in line or "QUIT" in line or "NOTICE" in line or "USERSTATE" in line or 'PRIVMSG #' in line:
            if 'PRIVMSG' in line:
                parts = line.split('PRIVMSG #' + CHANNEL + ' :')

                userdata = parts[0].split(';')
                newUser = dict()
                for data in userdata:
                    dataParts = data.split('=')
                    key = dataParts[0]
                    valve = dataParts[1]
                    newUser.update({str(key) : valve})
                u = True
                for x in user:
                    if x.get('display-name') in newUser.get('display-name'):
                        u = False
                if u == True:
                    user.append(newUser)
                    aktuser = newUser

                print(aktuseruser)
    streamer = False
    mod = False
    for x in user:
        if x == 'bagdes':
            test = x.get('badges')
            if test == 'broadcaster/1':
                streamer = True
        if x == 'mod':
            test = x.get('mod')
            if test == '1':
                mod = True
        print(x.get('display-name') + '> Stramer :' + str(streamer) + '> Moderator :' + str(mod))



'''
for er in user:
    print(type(er))
    items = []
    for item in er.items() :
#        items
    log.write(str(items) +'\n')
log.close()


    for line in chat:
        parts = line.split('PRIVMSG #' + CHANNEL + ' :')
        if len(parts) >= 2:
            meta = parts[0]
            message = parts[1]
            print(parts[1])
        else:
            print(parts)
        
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
