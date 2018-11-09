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
ban = [] #Les bannis, on verifie ici avant de 
user = []
serv = socket()

class User: #associe une ip a un nickname
	def __init__(self,addr,name):
		self.nickname = name
		self.addr = addr[0]

	def __str__(self):
		return("(" +self.name + "@" + self.addr + ")")	

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

def sendMsg(dest,msg):
        for i in socks:
                if i == argv[1]: #il y a une socket qui pointe vers l'ip destination
                        print("")
                else:
                        print("")
        print("ok")

def sendMsgBroadcast(msg):
	for s in socks:
		sendMsg(s,msg)
	print("ok")

def init():
	#creer socket qui ecoute
	createServ()
	if len(argv) == 2:
		print("ip")
		createServ()

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
			d = s.recv(1024).decode("ascii")
			print(d)

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


