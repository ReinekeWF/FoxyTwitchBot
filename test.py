import requests
r = requests.get('http://tmi.twitch.tv/group/user/broeki1/chatters')
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
print(len(listViewer))
for x in listViewer:
    print(x)
if "shrawg" in listViewer:
    print("ja")
else:
    print('nein')
