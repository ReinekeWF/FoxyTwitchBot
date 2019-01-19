import time
import socket
import requests
import config

HOST = "irc.chat.twitch.tv"
PORT = 6667
NICK = "kleinerfuchsbot"
PASS = config.oauth()

CHANNEL = input('Channel name eingeben: ')

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
try:
    s.connect((HOST, PORT))
    s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
    s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
    s.send(bytes("JOIN #" + CHANNEL + " \r\n", "UTF-8"))
    print("Erfolgreiche Verbindung zu Channel " + CHANNEL)

except:
    print('fehler beim login')


print('send')
#send_message('hallo ich bin ein fuchsiger bot!! =^.^=')
print('spieler anzahl' + str(len(listViewer)))
for viewer in listViewer:
    print(viewer)
print('es sind ' + str(len(listViewer)) + ' Viewer im Chat')
