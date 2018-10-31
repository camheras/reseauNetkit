#!/usr/bin/python
##
# TCP chat server
# port 1664
##
from socket import *
from select import *
from sys import argv
from sys import stdin

socks = []
name = ""
s = None
def createProfile():
	print("what's your name ?")
	name = input()

def isCorrectIp(ip):
	print(ip)
	ip = int(ip)
	if ip<=255 and ip>=0:
		return True
	else:
		quit()
		return False

def createServ():
	s = socket(AF_INET, SOCK_STREAM)
	print(gethostbyname(gethostname()))
	s.bind((gethostbyname(gethostname()), 1664)) #changer l'ip on a 127.0.0.1 au lieu de 10.0.0.1

def quit():
	#quitte le serveur
	print("ok")

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
	if len(argv) > 1:
		print("ip")
		createServ()
		sendMsg()
	else:
		print("pas d'ip")

def start():
	createProfile()
	init()
	data = ""
	while 1:
		if data == "exit":
			break
		lin, lout, lex =select([stdin],[],[])
		for s in lin:
			if s==stdin :
				data = stdin.readline().strip("\n")
				print ("entrée clavier : %s" % data)


		entry = raw_input()
		arg = entry.split(" ")
		nb = len(arg)
		print(name)
		if arg[0] == "quit":
			quit()
		elif arg[0] == "pm":
			sendMsgBroadcast(arg[1],arg[2])
		elif	arg[0] == "bm":
			sendMsg()
		elif	arg[0] == "ban":
			print("ban")
		elif	arg[0] == "unban":
			print("unban")



start()

