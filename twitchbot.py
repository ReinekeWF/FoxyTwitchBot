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
username = 'Twich'
meta = ''
oldchat = ''
lastMessageTime = time.time()

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
aktivuser = []  # viewer()
send_message("/color SpringGreen")

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
					# print(parts[1])
					zaeler = 0
					lastMessageTime = time.time()
					for object in meta.split(';'):
						if 'display-name' in object:
							username = object.split('=')[1]
						zaeler += 1
			elif "JOIN" in line or "PART" in line or "QUIT" in line or "NOTICE" in line or "USERSTATE" in line:
				if "JOIN" in line:
					lineuser = line.split("@")
					user = lineuser[1].split(".")
					if user not in config.bots:  # or user not in aktivuser:
						print("JOIN: " + user[0])
						# send_message("Willkommen " + user[0])
						aktivuser.append(user[0])
				elif "NOTICE" in line and "too quickly" in line:
					cooldown = time.time() + 30
				elif 'NOTICE' in line:
					print(line)
				elif 'USERSTATE' in line:
					print(line)
				elif "PART" in line:
					lineuser = line.split("@")
					user = lineuser[1].split(".")
					if user in aktivuser:
						aktivuser.remove(user)
					if user not in config.bots:  # not user not in aktivuser:
						print("GO OUT: " + user[0])

				# print(line)
				# if 'JOIN' in line:
				#    print(line)
				continue

			elif 'PING' in line:
				s.send(bytes("PONG :tmi.twitch.tv  \r\n", "UTF-8"))
				print('PONG')

			# if "QUIT" not in parts[0] and "JOIN" not in parts[0] and "PART" not in parts[0]:

			if line == "'" or 'PING' in line:
				a = 0
			elif ':tmi.twitch.tv ' in line or config.nick in line:
				print(time.strftime('%H:%M:%S >>> ') + username + ": " + line)
				continue
			else:
				print(time.strftime('%H:%M:%S >>> ') + username + ": " + message)
				continue

			# Random Nachricht falls nichts im chat passiert
			if (time.time() - lastMessageTime) >= (60 * 5):
				lastMessageTime = time.time()
				send_message(randomevent())

			# Normale KeyWords ohne Benutzer interaktion
			for KeyWord in config.KeyWords:
				if KeyWord in message:
					if not len(config.KeyWords.get(KeyWord)) > 10:
						auswahlNummer = random.randint(0, len(config.KeyWords.get(KeyWord)) - 1)
						auswahlNachrichten = config.KeyWords.get(KeyWord)
						send_message(auswahlNachrichten[auswahlNummer])
						continue
					else:
						send_message(config.KeyWords.get(KeyWord))
						continue

			# Castom Keyworts mit Benutzer  interaktion
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


			# hier sind die Commands zuhause
			elif '!meister' in message:
				send_message("Mein Meister ist ReinekeWF!")

			elif '!commands' in message:
				command = ' | '.join(config.listCommands)
				send_message(command)

			elif '!loben' in message:
				send_message('/me Fuchsi fühlt sich gelobt! =^.^=')

			elif '!geschenk ' in message:
				beschenkter = message.split(' ')[1]
				send_message("@" + username + ' schenkt ' + geschenk() + ' an @' + beschenkter)

			elif message == '!git':
				send_message('https://github.com/ReinekeWF/FoxyTwitchBot')

			elif "!hype" in message:
				send_message("HYPETRAIHN incomming")

			elif "!fight" in message and username == "ReinekeWF":
				config.timerold = -1
				config.kampfModus = -1


			# Hier sind die hidden Commands zuhause
			elif '!sendepause ' in message and username == "ReinekeWF":
				zeit = (int(message.split()[1]) + round(time.time()))
				s.send(bytes(
					"PRIVMSG #" + CHANNEL + " :" + 'Ok Fuchsi ist still für ' + message.split()[
						1] + 'sekunden' + "\r\n",
					"UTF-8"))

			elif message == '!exit' and user == 'ReinekeWF':
				config.cooldown = 0
				send_message('Tschüss')
				log.close()
				s.shutdown(1)
				exit()

	else:
		a = 0
