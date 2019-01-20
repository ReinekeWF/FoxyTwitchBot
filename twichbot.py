import time
import socket
import requests
import config

HOST = "irc.chat.twitch.tv"
PORT = 6667
NICK = "kleinerfuchsbot"
PASS = config.oauth()

CHANNEL = input('Channel name eingeben: ')

listCommands = ['!loben','!commands']

r = requests.get('http://tmi.twitch.tv/group/user/' + CHANNEL + '/chatters')
r.encoding
test = r.json()
banned = {'bots':['freast',
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
                    'moobot']}

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


s = socket.socket()
def send_message(message):
    s.send(bytes("PRIVMSG #" + CHANNEL + " :" + message + "\r\n", "UTF-8"))
    print(NICK + ': ' +message)

try:
    s.connect((HOST, PORT))
    s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
    s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
    s.send(bytes("JOIN #" + CHANNEL + " \r\n", "UTF-8"))
    print("Erfolgreiche Verbindung zu Channel " + CHANNEL)

except:
    print('fehler beim login')


print('send')
#send_message('hallo  =^.^=')
print('spieler anzahl' + str(len(listViewer)))
for viewer in listViewer:
    print(viewer)
print('es sind ' + str(len(listViewer)) + ' Viewer im Chat')

startTime = time.time()
while True:
    #if (time.time() - startTime) >= 10:
    #    send_message('TimerTest')
    #    startTimet = time.time()

    #chat = str(s.recv(1024)).split('\\r\\n')
    for line in str(s.recv(1024)).split('\\r\\n'):
        parts = line.split(':')
        if len(parts) < 3:
            continue

        if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
            message = parts[2][:len(parts[2])]


        usernamesplit = parts[1].split("!")
        username = usernamesplit[0]

        print(username + ": " + message)

        if 'test' in message:
            send_message("hallo")
            print(parts[2])
        if message == '17':
            send_message('was 17? 17 Apfel?')
        if 'meister' in message:
            send_message("Mein Meister ist ReinekeWF!")
            print(parts[2])

# hier sind die Commands zuhause
        if '!commands' in message:
            command = ' | '.join(listCommands)
            send_message(command)
        if '!loben' in message:
            send_message('Fuchsi fühlt sich gelobt! =^.^=')

        if '!exit' in message:
            send_message('Tschüss')
            s.shutdown(1)
            exit()
