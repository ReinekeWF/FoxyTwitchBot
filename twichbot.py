import time
import socket
import requests
import config

HOST = "irc.chat.twitch.tv"
PORT = 6667
NICK = "KleinerFuchsBot"
PASS = config.oauth()

CHANNEL = 'reinekewf'


'''
r = requests.get('http://tmi.twitch.tv/group/user/gronkh/chatters')
r.encoding
'''


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
    print('fehler')

while True:
    time.sleep(3)
    print('send')
    send_message('hallo ich bin ein fuchsiger bot!! =^.^=')
