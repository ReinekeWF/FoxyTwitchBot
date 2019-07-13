# -*- coding: UTF-8 -*-
import time
import socket
import requests
import config
import random

# import threading

# import pygame
# import tkinter


listCommands = ['!loben', '!commands', '!geschenk <zu beschenknder user>', '!git']
message = ''
chat = ''
zeit = 0
username = 'Twich'
meta = ''
oldchat = ''
lastMessageTime = time.time()

HOST = config.host
PORT = config.port
NICK = config.nick
PASS = config.oauth

log = open("log.txt","a")

timer = 0
timerold = -1

def login():
    """login"""


    channelZaler = 0
    stellen = 5
    for Channel in config.ChannelList:
        if channelZaler == 10:
            stellen -= 1
        print(str(channelZaler) + ' ' * (stellen) + Channel)
        channelZaler += 1
    auswahl = input('Channel name eingeben: ')
    try:
        CHANNEL = config.ChannelList[int(auswahl)]
    except:
        CHANNEL = auswahl

    try:
        s.connect((HOST, PORT))
        s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
        s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
        s.send(bytes("JOIN #" + CHANNEL + " \r\n", "UTF-8"))
        print("Erfolgreiche Verbindung zu Channel " + CHANNEL)

    except:
        print('fehler beim login')
    return CHANNEL


def geschenk():
    """zufÃƒÂ¤lliges geschenk auswÃƒÂ¤hlen"""

    geschenke = config.geschenke
    auswahl = random.randrange(0, len(geschenke) - 1)
    return geschenke[auswahl]

def randomevent():
    auswahl = config.zufälligeNachrichten[random.randint(0,len(config.zufälligeNachrichten)-1)]
    return auswahl

def viewer():
    """listet alle zuschauer auf"""
    r = requests.get('http://tmi.twitch.tv/group/user/' + CHANNEL + '/chatters')
    # r.encoding
    test = r.json()
    banned = {'bots': config.bots}

    listBanned = banned['bots']
    listViewer = test['chatters']['viewers']

    listMods = test['chatters']['moderators']
    listVips = test['chatters']['vips']

    # loescht alle Bots und co
    for i in listBanned:
        if i in listViewer:
            listViewer.remove(i)

        if i in listMods:
            listMods.remove(i)
        if i in listVips:
            listVips.remove(i)

    zahler = 0
    for viewer in listViewer:
        # text = pygame.font.Font.render(font,viewer,True,(200,200,200))
        # fenster.blit(text,(10,zahler * 10))
        zahler += 1
        print(viewer)
    # pygame.display.flip()
    # print('es sind ' + str(len(listViewer)) + ' Viewer im Chat')

    return listViewer


def reconnect():
    """reconnect"""
    s.close()
    s.connect((HOST, PORT))
    time.sleep(0.05)
    s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
    time.sleep(0.05)
    s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
    time.sleep(0.05)
    s.send(bytes("JOIN #" + CHANNEL + " \r\n", "UTF-8"))
    print("Erfolgreiche Verbindung zu Channel " + CHANNEL)


def send_message(message):

    """
    Args:
        message:
    """
    if zeit > time.time():
        print('Fuchsi mus still bleiben')
    else:
        try:
            if config.cooldown <= time.time() and config.lastmessage != message:
                s.send(bytes("PRIVMSG #" + CHANNEL + " :" + message + "\r\n", "UTF-8"))
                print(NICK + ': ' + message)
                config.cooldown = time.time() + 2
                config.lastmessage = message
                #print(config.cooldown)
            else:
                print(message)
        except:
            reconnect()

'''
def get_message ():
    """Holt sich die Nachrichten"""
    chat = ''
    try:
        chat = str(s.recv(1024)).split('\\r\\n')

    except:
        reconnect()
    if chat != oldchat:
        oldchat = chat
        for line in oldchat:
            #log.write(line + "\n")
            if "PRIVMSG #" in line:
                parts = line.split('PRIVMSG #' + CHANNEL + ' :')
                if len(parts) >= 2:
                    meta = parts[0]
                    message = parts[1].lower()
                    #print(parts[1])
                    zaeler = 0
                    for object in meta.split(';'):
                        if 'display-name' in object:
                            username = object.split('=')[1]
                        zaeler += 1
            if "JOIN" in line or "PART" in line or "QUIT" in line or "NOTICE" in line or "USERSTATE" in line:
                if "JOIN" in line:
                    lineuser = line.split("@")
                    user = lineuser[1].split(".")
                    if user not in config.bots and user not in aktivuser:
                        #send_message("Willkommen " + user[0])
                        aktivuser.append(user[0])
                if "NOTICE" in line and "too quickly" in line:
                    cooldown = time.time() + 30
                print(line)
                #if 'JOIN' in line:
                #    print(line)
                continue

            if 'PING' in line:
                s.send(bytes("PONG :tmi.twitch.tv  \r\n", "UTF-8"))
                print('PONG')

            #if "QUIT" not in parts[0] and "JOIN" not in parts[0] and "PART" not in parts[0]:


            if line == "'" or 'PING' in line:
                continue
            elif ':tmi.twitch.tv ' in line or config.nick in line:
                print(time.strftime('%H:%M:%S >>> ') + username + ": " + line)
                continue
            else:
                print(time.strftime('%H:%M:%S >>> ') + username + ": " + message)
                continue
    return username, message

def kampffuchs():
    while True:
        time.sleep(2)
        print("test")
        if config.kampfModus == -1:
            config.startkampf = time.time()
            config.kampfModus = 1
            send_message("!fight")
            print("fight start" + str(config.timerold))
        if config.kampfModus == 1 and (time.time() - config.startkampf) >= 120:
            config.kampfModus = 0
            config.timerold = time.time()
            print("fight end" + str(timerold))
        if config.kampfModus == 1 and (time.time() - config.startkampf) < 120:
            if (config.timerold - time.time()) >= 10 or config.timerold == -1:
                config.timerold = time.time()
                time.sleep(0.5)
                send_message("!" + str(random.randrange(1,5)))
                print("fight state" + str(timerold))
            else:
                print("fight nothing" + str(timerold))
'''
# pygame.init()
# pygame.font.init()
# font = pygame.font.Font('C:/Windows/Fonts/verdana.ttf',18)
# fenster = pygame.display.set_mode((400,800))

s = socket.socket()

startTime = time.time()
# viewerlist = []
# viewerlist.append(viewer())


CHANNEL = login()
# send_message('Hallo der Bottige Fuchsi ist nun Online =^.^= ')
time.sleep(0.05)
s.send(bytes("CAP REQ :twitch.tv/membership" + "\r\n", "UTF-8"))
time.sleep(0.05)
s.send(bytes("CAP REQ :twitch.tv/tags" + "\r\n", "UTF-8"))
time.sleep(0.05)
s.send(bytes("CAP REQ :twitch.tv/commands" + "\r\n", "UTF-8"))
aktivuser = viewer()
send_message("/color SpringGreen")

#kampf = threading.Thread(target=kampffuchs())
while True:
    # if (time.time() - startTime) >= 60 * 5:
    #    viewer()
    #    #send_message('TimerTest')
    #    startTimet = time.time()

    time.sleep(1)
    ###################################
    try:
        chat = str(s.recv(1024)).split('\\r\\n')
    except:
        reconnect()

    if chat != oldchat:
        oldchat = chat
        for line in oldchat:
            log.write(line + "\n")
            bots = False
            for bot in config.bots:
                if bot in line:
                    bots = True
                    continue
            if "PRIVMSG #" in line and not bots:
                parts = line.split('PRIVMSG #' + CHANNEL + ' :')
                if len(parts) >= 2:
                    meta = parts[0]
                    message = parts[1].lower()
                    #print(parts[1])
                    zaeler = 0
                    lastMessageTime = time.time()
                    for object in meta.split(';'):
                        if 'display-name' in object:
                            username = object.split('=')[1]
                        zaeler += 1
            if "JOIN" in line or "PART" in line or "QUIT" in line or "NOTICE" in line or "USERSTATE" in line:
                if "JOIN" in line:
                    lineuser = line.split("@")
                    user = lineuser[1].split(".")
                    if user not in config.bots: # or user not in aktivuser:
                        print("JOIN: " + user[0])
                        #send_message("Willkommen " + user[0])
                        aktivuser.append(user[0])
                if "NOTICE" in line and "too quickly" in line:
                    cooldown = time.time() + 30
                if "PART" in line:
                    lineuser = line.split("@")
                    user = lineuser[1].split(".")
                    if user not in config.bots: # not user not in aktivuser:
                        print("GO OUT: " + user[0])

                #print(line)
                #if 'JOIN' in line:
                #    print(line)
                continue

            if 'PING' in line:
                s.send(bytes("PONG :tmi.twitch.tv  \r\n", "UTF-8"))
                print('PONG')

            #if "QUIT" not in parts[0] and "JOIN" not in parts[0] and "PART" not in parts[0]:


            if line == "'" or 'PING' in line:
                a = 0
            elif ':tmi.twitch.tv ' in line or config.nick in line:
                print(time.strftime('%H:%M:%S >>> ') + username + ": " + line)
                continue
            else:
                print(time.strftime('%H:%M:%S >>> ') + username + ": " + message)
                continue
############################################################
            if 'hallo ' in message or 'moin ' in message or 'hi ' in message or 'huhu ' in message:
                '''
                aktuellviewer = viewer()
                newlistviewer =[]
                for name in aktuellviewer:
                    namex = str(name).lower()
                    newlistviewer.append(namex)
                print(newlistviewer)
                if newlistviewer in message:
                    for name in newlistviewer:
                        print(name)
                        if name in message:
                            user = namex
                            break
                    send_message("Hallo " + user + ' wie gehts dir?')
                else:
                    send_message("Hallo " + username + ' wie gehts dir?')
                '''
                send_message("Hallo " + username + ' =^.^=')

            if (time.time() - lastMessageTime) >= (60*5):
                lastMessageTime = time.time()
                send_message(randomevent())

                print("langweilig")

            if 'minecraft' in message:
                send_message('Ssssssssir ' + username + ' Wassss geht? BOOOM =^.^=')

            if '17 ' in message:
                send_message('was 17? 17 Apfel?')

            if 'meister ' in message and 'kleinerfuchsbot' in message:
                send_message("Mein Meister ist ReinekeWF!")

            if 'gut und dir ' in message:
                send_message('gut und dir?')

            if 'schei\\xc3\\x9fe ' in message:
                send_message('naanana das sagt man nicht!')

            if 'python ' in message:
                send_message('was ist Python? Laufe ich etwar auf Python? ... Könnte gut sein =^.^=')

            if 'nicht antworten ' in message:
                send_message('nicht antworten finde ich unhöflich!')

            if 'edge ' in message:
                send_message('Livin On The Edge by Aerosmith ')
            if 'http' in message:
                send_message('Fuchsi mag Links Wolfform')
            # hier sind die Commands zuhause
            if '!commands ' in message:
                command = ' | '.join(listCommands)
                send_message(command)
            if '!loben' in message:
                send_message('/me Fuchsi fühlt sich gelobt! =^.^=')
            if '!geschenk ' in message:
                beschenkter = message.split(' ')[1]
                send_message("@" + username + ' schenkt ' + geschenk() + ' an @' + beschenkter)
            if message == '!git':
                send_message('https://github.com/ReinekeWF/FoxyTwitchBot')
            if "!hype" in message:
                send_message("HYPETRAIHN incomming")

            if "!fight" in message and username == "ReinekeWF":
                config.timerold = -1
                config.kampfModus = -1

            # Hier sind die hidden Commands zuhause
            if '!sendepause ' in message:
                zeit = (int(message.split()[1]) + round(time.time()))
                s.send(bytes(
                    "PRIVMSG #" + CHANNEL + " :" + 'Ok Fuchsi ist still für ' + message.split()[1] + 'sekunden' + "\r\n",
                    "UTF-8"))

            if message == '!exit':
                config.cooldown = 0
                send_message('Tschüss')
                log.close()
                s.shutdown(1)
                exit()
    else:
        a = 0
