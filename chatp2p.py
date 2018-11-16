# -*- coding: utf-8 -*-
from socket import *
from select import select

class User:
	def __init__(self,sc,addr,name):
		self.nickname = name
		self.name = name
		self.sc = sc
		self.addr = addr[0]

	def __str__(self):
		return(self.nickname+"	(" +self.name + "@" + self.addr + ")")	

class Group:
	def __init__(self,name,mod):
		self.name = name
		self.mod = mod
		self.users = []
		self.users.append(mod)
		self.topic = "none"

	def add_user(self,user):
		self.users.append(user)

	def __str__(self):
		s = "Group : " + self.name + "\tMod : "
		if self.mod == None:
			s += "None"
		else:
			s += self.mod.name
		s += "\t"+"Topic : "+self.topic+"\n"+str(len(self.users))+" members"+"\n"
		for u in self.users:
			s += str(u)
		return(s)

def send(client,paquet):
	if len(paquet) > 255:
		paquet = chr(255)+paquet
		buf = paquet[:256].encode('utf-8')
		client.send(buf)
		send(client,paquet[256:])
	else:	
		paquet = chr(len(paquet))+paquet
		buf = paquet.encode('utf-8')
		client.send(buf)
		

def send_proto_packet(client):
	td = "j1" + chr(0)
	send(client,td)


s = socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('0.0.0.0',7326))
s.listen(5)L3 MIAGE - 2018/2019

serveurLance = True
clientsCo = []
groups = []
users = []

while serveurLance:
	coDemandees, wlist, xlist = select([s],[],[],0.05)
	for co in coDemandees:
		sc, addr = s.accept()
		clientsCo.append(sc)
		send_proto_packet(sc)
#		print("%s %s est en ligne" % ((gethostbyaddr(addr[0])[0]),(gethostbyaddr(addr[0])[2])))
		newUser = User(sc,(gethostbyaddr(addr[0])[2]),(gethostbyaddr(addr[0])[0]))
	
	clientsMsg = []

	try: 
		clientsMsg, wlist, xlist = select(clientsCo,[],[],0.05)
	except select.error:
		print("connection error")
		break
	
	else:
		for client in clientsMsg:
			for g in groups:
				for u in g.users:
					if u.sc == client:
						currentGroup = g
						currentUser = u
					
			data = client.recv(1024)
			try:
				msg = data.decode('utf-8')
#				print(msg)
			except:
				send(client,"ecan't treat packet : decode error"+chr(0))
				continue
#deconnexion d'un client
			if msg == "":
				td = "dSign-off"+chr(1)+currentUser.name+" "+currentUser.addr+" just left"+chr(0)
				for c in currentGroup.users:
					if c != currentUser:
						send(c.sc,td)
				clientsCo.remove(currentUser.sc)
				currentGroup.users.remove(currentUser)

#paquet login
			elif msg[1] == "a":
				currentUser = newUser
				send(client,"a" + chr(0))

				groupName = (msg.split(chr(1)))[2]
				groupMatch = False

				for g in groups:
					if groupName == g.name:
						groupMatch = True
						g.add_user(currentUser)
						currentGroup = g
				if groupMatch == False:
					currentGroup = Group(groupName,currentUser)
					groups.append(currentGroup)

				td = "dStatus" + chr(1) + "You are now in group "+ groupName + chr(0)
				send(client,td)

				td = "dSign-in"+ chr(1) + currentUser.name + " (" + currentUser.addr + ") entered group" + chr(0)
				for c in currentGroup.users:
					if c != currentUser:
						send(c.sc,td)
						
#paquet option
			elif msg[1] == "h":
#afficher groupes
				if msg[2] == "w":
					for g in groups:
						if g.mod == None:
							nn = "none"
						else:
							nn = g.mod.nickname
						send(client,"ico"+chr(1)+"Group : " + g.name + " | Mod : "+nn+" | Topic : "+g.topic+chr(0))
						for u in g.users:
							send(client,"ico"+chr(1)+str(u)+chr(0))
					
#messages prives
				elif msg[2] == "m":
					dest = (msg[3:].split(" "))[0]
					txt = msg[3+len(dest):-1]
					td = "c"+currentUser.nickname+chr(1)+str(txt)+chr(0)
					for c in currentGroup.users:
						if dest.find(c.name)!= -1:
							send(c.sc,td)
#changement de groupe
				elif msg[2] == "g":
					if len(msg) < 6:
						td = "dStatus"+chr(1)+"You are now in group "+currentGroup.name+chr(0)
						send(client,td)
					else:
						groupName = (msg[3:].split(" "))[0]
						groupName = groupName[1:-1]
						newGroup = None
						for g in groups:
							if groupName.find(g.name)!= -1: 
								newGroup = g
						if newGroup == None:
							newGroup = Group(str(groupName),currentUser)
							groups.append(newGroup)
						else:
							newGroup.add_user(currentUser)
						currentGroup.users.remove(currentUser)
						if currentGroup.mod == currentUser:
							currentGroup.mod = None
						td = "dStatus"+chr(1)+"You are now in group "+str(groupName)+chr(0)
						send(client,td)
						td = "dDepart"+chr(1)+currentUser.nickname+" "+currentUser.addr+" just left"+chr(0)
						for c in currentGroup.users:
							send(c.sc,td)
						
	
					
#changement de pseudo
				elif msg[2:6] == "name":
					if len(msg) < 9:
						td = "dName"+chr(1)+"Your nickname is "+currentUser.nickname+chr(0)
						send(client,td)
					else:
						newName = str(msg[7:-1])
						currentUser.nickname = newName
						td = "dName"+chr(1)+currentUser.name+" changed nickname to "+currentUser.nickname+chr(0)
						for c in currentGroup.users:
							send(c.sc,td)
										
#changement de topic
				elif msg[2:7] == "topic":
					if currentUser == currentGroup.mod:
						top = str(msg[8:-1])
						currentGroup.topic = str(top)
						
						td = "dTopic"+chr(1)+currentUser.nickname+" changed the topic to "+str(top)+chr(0)
						for c in currentGroup.users:
							send(c.sc,td)
					else:
						td = "eSetting the topic is only for moderators."+chr(0)
						send(client,td)
#passage des droits moderateur
				elif msg[2:6] == "pass":
					if currentGroup.mod == None:
						currentGroup.mod = currentUser
						td = "dNotify"+chr(1)+"server just passed you moderation of "+currentGroup.name+chr(0)
						send(client,td)
						td = "dNotify"+chr(1)+"server has passed moderation to "+currentUser.nickname+chr(0)
						for c in currentGroup.users:
							if c != currentUser:
								send(c.sc,td)
					elif currentGroup.mod == currentUser:
						currentGroup.mod = None
						td = "dNotify"+chr(1)+currentUser.nickname+" abandoned his moderator rights"+chr(0)
						for c in currentGroup.users:
							send(c.sc,td)
					else:
						td = "ethere is already a moderator"
						send(client,td)
				
#manuel
				elif msg[2] == "?":
					td = "dHelp"+chr(1)+"server supports following commands:"+chr(0)
					send(client,td)
                                        td = "dHelp"+chr(1)+"/w /m /g /name /topic /pass /q /?"+chr(0)
					send(client,td)

#commande inconnue
				else:
					send(client,"eUnknown command"+chr(0))
				
							
	
#paquet message ouvert
			elif msg[1] == "b":
				openMsg = msg[2:]
				td = "b"+currentUser.nickname+chr(1)+openMsg+chr(0)
				for c in currentGroup.users:
					if c != currentUser:
						send(c.sc,td)
#paquet inconnu
			else:
				td = "eUnknown type of packet"
				send(client,td)
				



for c in clientsCo:
	c.close()
s.close()
	
