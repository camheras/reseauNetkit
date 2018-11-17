#!/usr/bin/python
##
# TCP chat server
# port 1664
##
from socket import *
from select import *
from sys import argv
from sys import stdin
import time
 

name = ""
socks = [] #Pourquoi ?
myaddr = []
nvSockets = []
s = None
ban = [] #Les bannis, on verifie ici avant de recevoir 
users = []#Liste des users connus
serv = socket(AF_INET, SOCK_STREAM)

def estBanni(c):
    for x in ban:
        if x == c:
            return 1
    return 0


def ban(ip):#fini
	if(ip in ban):
		print("deja blackliste")
	else:
		ban.append(ip)
		print ("l'ip "+ip+" a bien ete blackliste" )

def unban(ip):#fini
	if(user in ban):
		ban.remove(user)
		print ("l'ip "+ip+" est debloque")
	else:
		print("n'est pas bloque")

def afficher():
    print()

def generateSocketClient(ip):#return un socket qui pointe vers l'ip
	s = socket(AF_INET, SOCK_STREAM)
	s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	s.connect((ip, 1664))
	return s

def handle( msg, ip):  # Traite et gere les string qui sont recus
	print(msg)
	s1,s2 = msg.split("\\001")
	print(s1)
	#s2 = s2[1:]
	#s1=s1[1:]
	s1=int(s1)
	print("msg : " +msg)
	if s1 > 1000 and s1 < 2000: #START
		print("recoit START")
		sc = generateSocketClient(ip)
		sendMsg( sc, s2, 2)
		time.sleep(5)
		sendMsg( sc, s2, 2)
		users.append((ip,s2))
		sendMsg( sc, " ", 3)		

	elif s1 > 2000 and s1 < 3000: #HELLO
		print("recoit HELLO")

	elif s1 > 3000 and s1 < 4000: #IPS
		
		print("recoit IPS")#peut etre l'inverse, probabilite d'erreur
		ips= s2.split(";")
		for user in ips :
			name,ip=user.split(",")
			if user not in users :
				users.append((ip,name))
			

	elif s1 > 4000 and s1 < 5000: #PM
		print("recoit PM")
		if estBanni(ip) == 0:
			print("pm recu : "+s2)

	elif s1 > 5000 and s1 < 6000: #BM
		if estBanni(ip) == 0:
			print("bm recu : " + s2)
	else:
		print("erreur")

# todo
# check ban

def sendMsg(socket, msg, type):  # Le 1229 c'est pas des erreurs destress
    # Je ne suis pas sur de la syntaxe du send
    if type == 1:
        message = ""
        message = "1229\\001" + name  # SEND START
        print("send message :" + message)
        buf = message.encode('utf-8')
        socket.send(buf)

    if type == 2:  # send nickname de l'interlocuteur, il faurait avoir mis dans le msg le nickname du receptioniste
        message = ""
        message = "2229\\001" + msg
        print("send message :" + message)
        buf = message.encode('utf-8')
        socket.send(buf)

    if type == 3:  
		ips = ""
		for i in users:
			ips= ips+i[0]+","+i[1]+";"
		message = "3229\\001" + ips
		message = message + myaddr[0] +","+ name #La on se rajoute. 
		print("send message :" + message)
		buf = message.encode('utf-8')
		socket.send(str(message))

    if type == 4:  # Send PM
        message = ""
        message = "4229\\001" + msg
        print("send message :" + message)
        buf = message.encode('utf-8')
        socket.send(buf)

    if type == 5:  # TODO ca ne marcheras pas
		message = "5229\\001" + msg
		buf = message.encode('utf-8')
		for x in socks:
			x.send(buf)

def createProfile():
	print("what's your name ?")
	return raw_input() 
	

def isCorrectIp(ip):
    print(ip)
    ip = int(ip)
    if ip <= 255 and ip >= 0:
        return True
    else:
        quit()
        return False
		

def createServ():#fini
	serv.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	serv.bind(('0.0.0.0',1664))
	serv.listen(5)
	socks.append(serv)


def quit():#fini
	exit()


def sendMsgBroadcast(msg):
	for s in socks:
		sendMsg(s,msg)
	print("ok")


def init():
	#creer socket qui ecoute
	createServ()
	if len(argv) == 2:
		print("ip : "+argv[1])
		#create socket pour client on l'appelle s
		s = socket(AF_INET, SOCK_STREAM)
		s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		s.connect((argv[1], 1664))
		print("j'ai trouve mon adrresse : " + s.getsockname()[0])
		myaddr.append(s.getsockname()[0])
		socks.append(s)
		users.append((myaddr[0],name))
		sendMsg(s,"",1)

	elif len(argv) == 1:
		print ("Pas d'ip!")
	else:
		print("Nombres d'arguments incorects")
		quit();

def isCorrectIp(ip):
    print(ip)
    ip = int(ip)
    if ip <= 255 and ip >= 0:
        return True
    else:
        quit()
        return False

def msg(data):
	if data == "quit":
		quit()
	elif data == "pm":
		sendMsgBroadcast()
	elif	data == "bm":
		sendMsg()
	elif	data == "ban":
		print("ban")
	elif	data == "unban":
		print("unban")
	else:
		print("la commande n'est pas reconnue")

name = createProfile()
print("djfbjebzf"+name)
init()
data = ""
socks.append(stdin)
while 1:
	if data == "exit":
		break
	
	lin, lout, lex =select(socks,[],[],0.5)
	
	for k in lin:
		#if k in nvSockets :
			
		if k==stdin:
			data = stdin.readline().strip("\n")
			print ("entree clavier : %s" % data)
			msg(data)
		if k==serv:
			sc, addr = serv.accept()
			print(sc.getpeername())
			
			d = sc.recv(1024).decode("utf-8")
			handle(d,sc.getpeername()[0])
			print(d)




