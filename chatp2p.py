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
socks = [] #liste des sockets
sockscl = [] #liste des sockets clients
myaddr = [] #adresse ip
s = None
listban = []  # Les bannis, on verifie ici avant de recevoir
users = []  # Liste des users connus
serv = socket(AF_INET, SOCK_STREAM) #socket serveur


def estBanni(c):
    for x in listban:
        if x == c:
            return True
    return False


def ban(ip):
    if (ip in listban):
        print("deja blackliste")
    else:
        listban.append(ip)
        print("l'ip " + ip + " a bien ete blackliste")

def generateSocketClient(ip):  # return un socket qui pointe vers l'ip
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.connect((ip, 1664))
    return s


def handle(msg, ip, socket):  # Traite et gere les string qui sont recus
    print("Jai recu : " + msg)
    k1 = msg.split("\001")
    s1 = int(k1[0])
    if s1 > 1000 and s1 < 2000:  # START
        print("J'ai recu un START")
        sendMsg(socket, k1[1], 2)
        if (ip,  k1[1]) not in users:
            users.append((ip, k1[1]))
            sockscl.append(socket)
        sendMsg(socket, " ", 3)

    elif s1 > 2000 and s1 < 3000:  # HELLO
        print("J'ai recu un HELLO")

    elif s1 > 3000 and s1 < 4000:  # IPS;
        print("J'ai recu un IPS")
        for x in k1 :
            if x != k1[0] :
                lesips=str(x)
                ips = lesips.split(";")
                for i in ips:
                    print(i)
                    if i != "":
                        ip,name = i.split(",")
                        if (ip, name) not in users:
                            if ip != myaddr[0]:
                                users.append((ip, name))
                                print("utilisateur ajoute")

    elif s1 > 4000 and s1 < 5000:  # PM
        print("recoit PM")
        if estBanni(ip) == 0:
            print("pm recu : " + k1[1])


    elif s1 > 5000 and s1 < 6000:  # BM
        print("recoit bm : ")
        if estBanni(ip) == 0:
            print("bm recu : " + k1[1])
    else:
        print("erreur")


def sendMsg(socket, msg, type):
    if type == 1: #START
        message = "1229\001" + name +"\001"
        print("send message :" + message)
        buf = message.encode('utf-8')
        socket.send(buf)

    if type == 2: #HELLO
        message = "2229\001" + msg +"\001"
        print("send message :" + message)
        buf = message.encode('utf-8')
        socket.send(buf)

    if type == 3: #IPS
        ips = ""
        for i in users:
            ips = ips + i[0] + "," + i[1] + ";"
        message = "3229\001" + ips +"\001"
        message = message + socket.getsockname()[0] + "," + name  # TODO
        print("send message :" + message)
        buf = message.encode('utf-8')
        for sock in sockscl:
            sock.send(buf)

    if type == 4:  # Send PM
        print(users)
        tab = msg.split(" ")
        message = "4229\001"+tab[1] + "#" + tab[2] + "\001"
        print("send message :" + message)
        sendtoSockFromName(tab[1],message)


    if type == 5:
        message = "5229\001" + msg + "\001"
        buf = message.encode('utf-8')
        for x in sockscl:
            x.send(buf)

def sendtoSockFromName(name,msg):
    print("je recherche la socket qui est a associe a :" +name)
    for i in users:
        if i[1]==name:
            print ("J'ai trouve son ip : " + i[0])
            sa=generateSocketClient(i[0])
            sa.send(msg)
            sa.close()
            for j in socks:
                if j != stdin and j != serv:
                    if i[0]== j.getpeername()[0] and i[0] not in listban:
                        print("J'ai trouve sa socket, et il n'est pas banni")
                        j.send(msg.encode('utf-8'))

    return "pas d'adresse associe a ce nom"

def createProfile():
    print("what's your name ?")
    return raw_input()


def createServ():
    serv.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serv.bind(('0.0.0.0', 1664))
    serv.listen(5)
    socks.append(serv)


def quit():
    exit()


def sendMsgBroadcast(msg):
    for s in users[0]:
        print(s)
        sc = generateSocketClient(s)
        sc.send(msg)
    print("broadcast send")


def init():
    createServ()
    if len(argv) == 2:
        print("ip : " + argv[1])
        s = socket(AF_INET, SOCK_STREAM)
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.connect((argv[1], 1664))
        myaddr.append(s.getsockname()[0])
        socks.append(s)
        sendMsg(s, "", 1)
    elif len(argv) == 1:
        print("Pas d'ip!")
    else:
        print("Nombres d'arguments incorects")
        quit();

def msg(data):
    if data == "quit":
        quit()
    elif data.split(" ")[0] == "pm":
        sendMsg("",data,4)
    elif data.split(" ")[0] == "bm":
        sendMsgBroadcast(data)
    elif data.split(" ")[0] == "ban":
        ban(data.split(" ")[1])
    elif data == "users":
        print(str(users))
    elif data.split(" ")[0] == "unban":
        ban(data.split(" ")[1])
    else:
        print("la commande n'est pas reconnue")


name = createProfile()
init()
data = ""
socks.append(stdin)
while 1:
    if data == "exit":
        break

    lin, lout, lex = select(socks, [], [],0.5)

    for k in lin:
        if k == stdin:
            data = stdin.readline().strip("\n")
            print("entree clavier : %s" % data)
            msg(data)
        elif k == serv:
            sc, addr = serv.accept()
            data = sc.recv(1024).decode("utf-8")
            handle(data, sc.getpeername()[0], sc)
            if not any(sc.getpeername()[0] in x.getpeername() for x in sockscl):
                sockscl.append(sc)
                socks.append(sc)
            print(data)
        else:
            data = k.recv(1024).decode("utf-8")
            if data:
                handle(data, k.getpeername()[0], k)
