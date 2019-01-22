import time
import socket
import requests
import config

# import pygame
# import tkinter

listCommands = ['!loben', '!commands']
message = ''
chat = ''
zeit = 0

HOST = "irc.chat.twitch.tv"
PORT = 6667
NICK = "kleinerfuchsbot"
PASS = config.oauth()

def login():
    ChannelList = ['artimus83','noobdevtv','reinekewf','traumfalke','tinylittlestudio','tutorexilius','propanben','gplay97','lifeoffranky','vectordex','lukascode','s0pht']
    channelZaler = 0
    stellen = 5
    for Channel in ChannelList:
        if channelZaler == 10:
            stellen -=1
        print(str(channelZaler) + ' ' * (stellen) + Channel)
        channelZaler += 1
    auswahl = input('Channel name eingeben: ')
    try:
        CHANNEL = ChannelList[int(auswahl)]
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


def viewer():
    r = requests.get('http://tmi.twitch.tv/group/user/' + CHANNEL + '/chatters')
    #r.encoding
    test = r.json()
    banned = {'bots': ['freast',
                       'nightbot',
                       'commanderroot',
                       'apricotdrupefruit',
                       'electricallongboard',
                       'host_giveaway',
                       'p0lizei_',
                       'p0sitivitybot',
                       'skinnyseahorse',
                       'slocool',
                       'activeenergy',
                       'moobot',
                       'energyzbot',
                       'kleinerfuchsbot'

                       ]}

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
    s.close()
    s.connect((HOST, PORT))
    s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
    s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
    s.send(bytes("JOIN #" + CHANNEL + " \r\n", "UTF-8"))
    print("Erfolgreiche Verbindung zu Channel " + CHANNEL)


def send_message(message):
    if zeit > time.time():
        print('Fuchsi mus still bleiben')
    else:
        try:
            s.send(bytes("PRIVMSG #" + CHANNEL + " :" + message + "\r\n", "UTF-8"))
            print(NICK + ': ' + message)
        except:
            reconnect()


# pygame.init()
# pygame.font.init()
# font = pygame.font.Font('C:/Windows/Fonts/verdana.ttf',18)
# fenster = pygame.display.set_mode((400,800))

s = socket.socket()

# send_message('Hallo der Bottige Fuchsi ist nun Online =^.^=')
startTime = time.time()
# viewerlist = []
# viewerlist.append(viewer())


CHANNEL = login()
viewer()
while True:
    # if (time.time() - startTime) >= 60 * 5:
    #    viewer()
    #    #send_message('TimerTest')
    #    startTimet = time.time()

    try:
        chat = str(s.recv(1024)).split('\\r\\n')
    except:
        reconnect()

    for line in chat:  # str(s.recv(1024)).split('\\r\\n'):
        parts = line.split(':')
        # print(line)
        if 'PING' in line:
            s.send(bytes("PONG :tmi.twitch.tv  \r\n", "UTF-8"))
            print('PONG')

        if len(parts) < 3:
            continue

        if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
            message = parts[2][:len(parts[2])]

        usernamesplit = parts[1].split("!")
        username = usernamesplit[0]

        print(username + ": " + message)

        if 'hallo' in message or 'moin' in message or 'Hallo' in message or 'Moin' in message:
            send_message("Hallo " + username + ' wie gehts dir?')

        if 'Minecraft' in message or 'minecraft' in message:
            send_message('Ssssssssir ' + username + ' Wassss geht? =^.^=')

        if '17' in message:
            send_message('was 17? 17 Apfel?')

        if 'meister' in message and 'kleinerfuchsbot' in message:
            send_message("Mein Meister ist ReinekeWF!")

        if 'gut und dir' in message:
            send_message('gut und dir?')

        if 'schei\\xc3\\x9fe' in message:
            send_message('naanana das sagt man nicht!')

        if 'python' in message:
            send_message('was ist python?')

        if 'nicht antworten' in message:
            send_message('nicht antworten finde ich unhöflich!')

        # hier sind die Commands zuhause
        if '!commands' in message:
            command = ' | '.join(listCommands)
            send_message(command)
        if '!loben' in message:
            send_message('Fuchsi fühlt sich gelobt! =^.^=')

        # Hier sind die hidden Commands zuhause
        if '!sendepause' in message:
            zeit = (int(message.split()[1]) + round(time.time()))
            s.send(bytes("PRIVMSG #" + CHANNEL + " :" + 'Ok Fuchsi ist still für ' + message.split()[1] + 'sekunden' + "\r\n", "UTF-8"))

        if message == '!exit':
            send_message('Tschüss')
            s.shutdown(1)
            exit()
