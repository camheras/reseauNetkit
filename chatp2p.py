#!/usr/bin/python
##
# TCP chat server
# port 1664
##
from socket import *
from select import *
from sys import argv
from sys import stdin

socks = []  # Pourquoi ?
name = ""
s = None
serv = socket()
nickname = name
addr = ""
users = []
ban = []

def estBanni(c):
    for x in ban:
        if x == c:
            return 1
    return 0

def afficher():
    print()

def generateSocketClient():
print()


def handle( msg, sc):  # Traite et gere les string qui sont recus
    str = msg.split("\001")
    if str[0] < 1000 and str[0] < 2000:  # todo peut mieux faire start
        sc = generateSocketClient()
        sendMsg( sc, str[1], 2)
        sendMsg( sc, " ", 3)

    if str[0] < 2000 and str[0] < 3000:  # hello
        print ()# bah cool

    if str[0] < 3000 and str[0] < 4000:  # ips
        for ip in msg[1].split(","):
            users.append(ip)  # On rajoute les ip
    if str[0] < 4000 and str[0] < 5000:  # pm
        if estBanni(sc.getsockeName()) == 0:
            print(str[1])
    # check ban
    if str[0] < 5000 and str[0] < 6000:  # bm
        print("Un message est arrive en broadcast")

# todo
# check ban

def sendMsg(socket, msg, type):  # Le 1229 c'est pas des erreurs destress
    # Je ne suis pas sur de la syntaxe du send
    if type == 1:
        message = ""
        message = 1229 + "\001" + nickname  # SEND START
        print("send message :" + message)
        buf = message.encode('utf-8')
        socket.send(buf)

    if type == 2:  # send nickname de l'interlocuteur, il faurait avoir mis dans le msg le nickname du receptioniste
        message = ""
        message = 2229 + "\001" + msg
        print("send message :" + message)
        buf = message.encode('utf-8')
        socket.send(buf)

    if type == 3:  # TODO
        ips = ""
        for x in users :
            ips = x.addr + " ," + ips

        message = (3229 + "\001" + ips)
        print("send message :" + message)
        buf = message.encode('utf-8')
        socket.send(buf)

    if type == 4:  # Send PM
        message = ""
        message = 4229 + "\001" + msg
        print("send message :" + message)
        buf = message.encode('utf-8')
        socket.send(buf)

    if type == 5:  # TODO ca ne marcheras pas
        sendMsgBroadcast(msg.encode('utf-8'))


def createProfile():
    print("what's your name ?")
    name = raw_input()
    print("hello " + name)


def isCorrectIp(ip):
    print(ip)
    ip = int(ip)
    if ip <= 255 and ip >= 0:
        return True
    else:
        quit()
        return False


def ban(user, ban):
    if (user in ban):
        print("deja blackliste")
    else:
        ban.append(user)
        print (user.nickname + " avec l'ip " + user.addr + " a bien ete blackliste")


def unban(user, ban):
    if (user in ban):
        ban.remove(user)
        print (user.nickname + " avec l'ip " + user.addr + " est debloque")
    else:
        print("n'est pas bloque")


def createServ():
    serv.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serv.bind(('0.0.0.0', 1664))
    serv.listen(5)


def quit():
    # quitte le serveur
    exit()


def sendMsgBroadcast(msg):
    for s in socks:
        print("Hey")
        #sendMsg(s, msg)
    print("ok")


def init():
	#creer socket qui ecoute
    createServ()
    if len(argv) == 2:
		print("ip "+argv[1])
		#create socket pour client on l'appelle s
		s = socket(AF_INET, SOCK_STREAM)
		s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		s.connect((argv[1], 1664))
		print(s.getsockname())
		socks.append(s)
		s.send("START")


def msg(data):
	if data == "quit":
		quit()
	elif data == "pm":
		sendMsgBroadcast(arg[1],arg[2])
	elif	data == "bm":
		sendMsg()
	elif	data == "ban":
		print("ban")
	elif	data == "unban":
		print("unban")
	else:
		print("la commande n'est pas reconnue")


def start():
    createProfile()
    init()
    data = ""

    socks.append(stdin)

    while 1:
        if data == "exit":
            break

        lin, lout, lex = select(socks, [], [])

        for s in lin:
            if s == stdin:
                data = stdin.readline().strip("\n")
                print ("entree clavier : %s" % data)
                msg(data)
            if s == serv:
                print("test")
                sc, addr = s.accept()
                d = sc.recv(1024).decode("ascii")
                print(d)


start()
