# -*- coding: UTF-8 -*-
import time
import socket
import requests
import config
import random

# import threading

# import pygame
# import tkinter
message = ''
chat = ''
zeit = 0
meta = ''
oldchat = []
lastMessageTime = time.time()
lastChatUserTime = time.time()

HOST = config.host
PORT = config.port
NICK = config.nick
PASS = config.oauth

log = open("log.txt", "a")

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
    auswahl = config.zufälligeNachrichten[random.randint(0, len(config.zufälligeNachrichten) - 1)]
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
            # print(config.cooldown)
        except:
            reconnect()

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
aktivuser = []  # viewer()
send_message("/color SpringGreen")

thisUser = 'Twitch'
chatuser = []
newUser = dict()
aktuser = dict()

# kampf = threading.Thread(target=kampffuchs())
while True:
    runtimestart = time.time()
    # if (time.time() - startTime) >= 60 * 5:
    #    viewer()
    #    #send_message('TimerTest')
    #    startTimet = time.time()

    time.sleep(1)
    ###################################
    try:
        chat = str(s.recv(1024).decode("utf-8")).split('\\r\\n')
    except:
        reconnect()

    # Random Nachricht falls nichts im chat passiert
    if (time.time() - lastMessageTime) >= (60 * 10):
        lastMessageTime = time.time()
        send_message(randomevent())
    #live ausgabe hilfe für user
    if (time.time() - lastChatUserTime) >= (60):
        lastChatUserTime = time.time()
        print(chatuser)
        if chatuser != []:
            print('-' * 20)
            for x in chatuser:
                print(x.get('display-name'))
            print('-' * 20)

    for line in chat:
        if line not in oldchat:
            oldchat.append(line)
            log.write(line + "\n")
            if "PRIVMSG #" in line:
                bots = False
                for bot in config.bots:
                    if bot in line:
                        bots = True
                        break
                if bots:
                    continue
                else:
                    parts = line.split('PRIVMSG #' + CHANNEL + ' :')
                    if len(parts) >= 2:
                        userdata = parts[0].split(';')
                        message = parts[1].lower()
                        newUser = dict()
                        for data in userdata:
                            dataParts = data.split('=')
                            if len(dataParts) == 2:
                                key = dataParts[0]
                                valve = dataParts[1]
                                newUser.update({str(key): valve})
                        thisUser = newUser.get('display-name')
                        usermode = newUser.get('badges')
                        u = True
                        aktuser = newUser
                        if chatuser != []:
                            for x in chatuser:
                                if x.get('display-name') in newUser.get('display-name'):
                                    u = False
                                else:
                                    continue
                        if u == True:
                            chatuser.append(newUser)
                    lastMessageTime = time.time()
                aktusermeta = aktuser.keys()
                for x in aktusermeta:
                    if x == 'badges':
                        test = aktuser.get('badges')
                        try:
                            userinhalt = test.split(',')
                        except:
                            userinhalt = []
                            userinhalt.append(test)

                        for inhalt in userinhalt:

                            inhaltparts = inhalt.split('/')
                            if inhaltparts[0] == 'broadcaster':
                                streamer = True
                            else:
                                streamer = False

                            if inhaltparts[0] == 'subscriber':
                                subscriber = True
                                subscribertime = int(inhaltparts[1])
                            else:
                                subscriber = False
                                subscribertime = 0

                            if inhaltparts[0] == 'bits':
                                bits = int(inhaltparts[1])
                            else:
                                bits = 0

                    if x == 'mod':
                        test = aktuser.get('mod')
                        if test == '1':
                            mod = True
                        else:
                            mod = False
                    if x == 'turbo':
                        test = aktuser.get('turbo')
                        if test == '1':
                            turbo = True
                        else:
                            turbo = False
                print(time.strftime('%H:%M:%S >>> ') + thisUser + ": " + line)


            if "JOIN #" in line:
                lineuser = line.split("@")
                try:
                    user = lineuser[1].split(".")
                except:
                    continue
                if user not in config.bots:  # or user not in aktivuser:
                    print("JOIN: " + user[0])

                    # send_message("Willkommen " + user[0])
                    aktivuser.append(user[0])

            if 'USERNOTICE' in line or ':tmi.twitch.tv ' in line or 'NOTICE #' in line: # b'@badge-info=subscriber/0;badges=subscriber/0,premium/1;color=#5F9EA0;display-name=SanderPrGa;emotes=;flags=;id=e43959c5-5c08-4cfc-8514-81139cb11ccc;login=sanderprga;mod=0;msg-id=sub;msg-param-cumulative-months=1;msg-param-months=0;msg-param-should-share-streak=0;msg-param-sub-plan-name=Channel\\sSubscription\\s(gronkh);msg-param-sub-plan=Prime;room-id=12875057;subscriber=1;system-msg=SanderPrGa\\ssubscribed\\swith\\sTwitch\\sPrime.;tmi-sent-ts=1564179542211;user-id=52257072;user-type= :tmi.twitch.tv USERNOTICE #gronkh
                print("USERNOTICE")
                print(line)

                if 'NOTICE #' in line:
                    if "too quickly" in line:
                        cooldown = time.time() + 30
                    else:
                        print('NOTICE')
                        print(line)
                if 'USERSTATE #' in line:
                    print('USERSTATE')
                    print(line)
                print(time.strftime('%H:%M:%S >>> ') + thisUser + ": " + line)

            if "PART #" in line:
                lineuser = line.split("@")
                user = lineuser[1].split(".")
                if user in aktivuser:
                    aktivuser.remove(user)
                if user not in config.bots:  # not user not in aktivuser:
                    print("GO OUT: " + user[0])

            if 'PING' in line:
                s.send(bytes("PONG :tmi.twitch.tv  \r\n", "UTF-8"))
                print('PONG')

            # Normale KeyWords ohne Benutzer interaktion
            for KeyWord in config.KeyWords:
                if KeyWord in message:
                    if not len(config.KeyWords.get(KeyWord)) > 10:
                        auswahlNummer = random.randint(0, len(config.KeyWords.get(KeyWord)) - 1)
                        auswahlNachrichten = config.KeyWords.get(KeyWord)
                        send_message(auswahlNachrichten[auswahlNummer])
                        break
                    else:
                        send_message(config.KeyWords.get(KeyWord))
                        break

            # Castom Keyworts mit Benutzer  interaktion
            if ('hallo ' in message or 'moin ' in message or 'hi ' in message or 'huhu ' in message) and thisUser != 'ReinekeWF':
                '''
                b'@badge-info=;badges=premium/1;color=#FF0000;display-name=PropanBen;emotes=;flags=;id=8c5c406f-f6bd-4e9e-a300-9c4b7174ffe6;login=propanben;mod=0;msg-id=raid;msg-param-displayName=PropanBen;msg-param-login=propanben;msg-param-profileImageURL=https://static-cdn.jtvnw.net/jtv_user_pictures/24f1472ec4884560-profile_image-70x70.png;msg-param-viewerCount=7;room-id=78953470;subscriber=0;system-msg=7\\sraiders\\sfrom\\sPropanBen\\shave\\sjoined!;tmi-sent-ts=1564231327156;user-id=124346119;user-type= :tmi.twitch.tv USERNOTICE #reyst
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
                send_message("Hallo " + thisUser + ' =^.^=')


            # hier sind die Commands zuhause

            elif '!bits?' in message:
                send_message('@'+thisUser+ ' hat ' + str(bits) + 'Bits gespendet!' )
            elif '!sub?' in message:
                send_message('@'+thisUser+ ' ist seit ' + str(subscribertime) + ' Monaten Sub!' )

            elif '!meister' in message:
                send_message("Mein Meister ist ReinekeWF!")

            elif '!commands' in message:
                command = ' | '.join(config.listCommands)
                send_message(command)

            elif '!loben' in message:
                send_message('/me Fuchsi fühlt sich gelobt! =^.^=')

            elif '!geschenk ' in message:
                beschenkter = message.split(' ')[1]
                send_message("@" + thisUser + ' schenkt ' + geschenk() + ' an @' + beschenkter)

            elif message == '!git':
                send_message('https://github.com/ReinekeWF/FoxyTwitchBot')

            elif "!hype" in message:
                send_message("HYPETRAIHN incomming")

            elif "!fight" in message and thisUser == "ReinekeWF":
                config.timerold = -1
                config.kampfModus = -1


            # Hier sind die hidden Commands zuhause
            elif '!sendepause ' in message and (thisUser == "ReinekeWF" or streamer):
                zeit = (int(message.split()[1]) + round(time.time()))
                s.send(bytes(
                    "PRIVMSG #" + CHANNEL + " :" + 'Ok Fuchsi ist still für ' + message.split()[
                        1] + 'sekunden' + "\r\n",
                    "UTF-8"))

            elif message == '!exit' and thisUser == 'ReinekeWF':
                send_message('Tschüss')
                log.close()
                s.shutdown(1)
                exit()

        else:
            pass
