#!/usr/bin/python
##
# TCP chat server
# port 1664
##
from socket import *
from select import *
from sys import argv
from sys import stdin

socks = [] #Pourquoi ?
name = ""
s = None
serv = socket()

class User: #associe une ip a un nickname
	def __init__(self,addr,name):
		self.nickname = name
		self.addr = addr[0]
		self.users = []#Liste des User connus
		self.ban = [] #Les bannis, on verifie ici avant de recevoir 


	def __str__(self):
		return("(" +self.name + "@" + self.addr + ")")	


	def estBanni(c)
		for x in self.ban :
			if x == c :
				return 1
		return 0


	def afficher() :


	def generateSocketClient():


	def handle(mdg,sc):#Traite et gere les string qui sont recus
		str = x.split("\001")
		if str[0] < 1000 and str[0] < 2000 :#todo peut mieux faire start
			sc = generateSocketClient()
			sendMsg(self,sc, str[1] ,2)
			sendMsg(self,sc," ",3)

		if str[0] < 2000 and str[0] < 3000 :#hello
		#bah cool

		if str[0] < 3000 and str[0] < 4000 :# ips
		for ip in x[1].split(","):
			users.append(ip) #On rajoute les ip 
		if str[0] < 4000 and str[0] < 5000 :# pm
			if estBanni(sc.getsockeName()) == 0 :
				afficher(str[1])
		#check ban
		if str[0] < 5000 and str[0] < 6000 :# bm
			#todo
		#check ban

	def sendMsg(self,socket,msg,type):#Le 1229 c'est pas des erreurs destress
		#Je ne suis pas sur de la syntaxe du send
		if type == 1 :
			message = ""
			message =1229+"\001"+self.nickname#SEND START
			buf = message.encode('utf-8')
			socket.send(buf)

		if type == 2 :#send nickname de l'interlocuteur, il faurait avoir mis dans le msg le nickname du receptioniste
			message = ""
			message = 2229+"\001"+msg
			buf = message.encode('utf-8')
			socket.send(buf)			

		if type == 3 :#TODO
			ips =""
			for x in this.users
				ips = x.addr  +" ," + ips 
				
			message=(3229+"\001"+ ips)
			buf = message.encode('utf-8')
			socket.send(buf)

		if type == 4 :#Send PM
			message =""
	 		message = 4229+"\001"+msg
			buf = message.encode('utf-8')
			socket.send(buf)

	 	if type == 5 :#TODO ca ne marcheras pas
	 		sendMsgBroadcast(msg.encode('utf-8'))



def createProfile():
	print("what's your name ?")
	name = raw_input()
	print("hello "+name)


def isCorrectIp(ip):
	print(ip)
	ip = int(ip)
	if ip<=255 and ip>=0:
		return True
	else:
		quit()
		return False


def ban(user,ban):
	if(user in ban):
		print("deja blackliste")
	else:
		ban.append(user)
		print (user.nickname +" avec l'ip "+user.addr+" a bien ete blackliste" )


def unban(user,ban):
	if(user in ban):
		ban.remove(user)
		print (user.nickname +" avec l'ip "+user.addr+" est debloque" )
	else:
		print("n'est pas bloque")
		

def createServ():
	serv.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	serv.bind(('0.0.0.0',1664))
	serv.listen(5)

	
def quit():
	#quitte le serveur
	exit()


def sendMsgBroadcast(msg):
	for s in socks:
		sendMsg(s,msg)
	print("ok")


def init():
	#creer socket qui ecoute
	createServ()
	if len(argv) == 2:
		print("ip"+argv[0])
		createServ()#pour l'ecoute
		#create socket pour client on l'appelle s
		s.connect((argv[0], 1664))
		s.send("HELLO")

	if len(argv) == 1:
		print ("Pas d'ip!")
	else:
		print("Nombres d'arguments incorects")
		quit();


def start():
	createProfile()
	init()
	data = ""
	while 1:
		if data == "exit":
			break
		
		sc,addr = serv.accept()
		lin, lout, lex =select([serv],[],[],0.1)
		print("aaa")
		for s in lin:
			if s==stdin :
				data = stdin.readline().strip("\n")
				print ("entree clavier : %s" % data)
		for s in lout:
			print("test")
			d = s.recv(1024).decode(utf-8)
			print(d)
			handle(d,s)

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


start()
