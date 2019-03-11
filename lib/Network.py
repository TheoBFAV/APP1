#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from inspect import cleandoc
import socket
import struct
import sys

BUFLEN=4096

soft_debug_mode = False
hard_debug_mode = False
# soft_debug_mode = True
# hard_debug_mode = True

do_attente_automatique = False

intro_msg = (cleandoc ("""
            ******************************
            *   Bienvenue sur AppoLab    *
            ******************************
            À tout moment, vous pouvez entrer la commande 'aide' ou 'help'
            pour afficher un message d'aide.
            Vous devez tout d'abord vous connecter en utilisant la commande 'login'
            login <identifiant> <mot-de-passe>
            """)+"\n\n")
#
# WARNING: on suppose que le message d'introduction termine toujours par un 
# double retour à la ligne (et pas d'autres lignes vides). C'est ainsi que le 
# client détermine que le message est terminé, avant de passer en mode 
# 'paquets'
#

intro_msglen = len(intro_msg.encode())

# print error
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


try:
    color = sys.stdout.shell

    # all possible colors in IDLE
    # alls = "SYNC,stdin,BUILTIN,STRING,console,COMMENT,stdout,TODO,stderr,hit,DEFINITION,KEYWORD,ERROR,sel"
    # cols = alls.split(',')
    # for c in cols:
        # color.write ("This is color " + c, c)

    # define colors for IDLE
    SEND = "STRING"
    RECV = "BUILTIN"
    WAIT = "KEYWORD"

    color_print = color.write

except AttributeError:
    # not in IDLE
    try:
        from termcolor import colored

        SEND = "green"
        RECV = "magenta"
        WAIT = "red"

        def color_print (message, color):
            print (colored (message, color), end='')
    except ImportError:
        def color_print (message, color):
            print (message, end='')



def prefix_print (prefix, message, color):
    lines = message.split('\n')
    if lines[-1] == "":
        lines.pop()
    for l in lines:
        # if l:
        color_print (prefix + l + '\n', color)






class LanguageError(Exception):
    pass

class ErrorWrite(Exception):
    pass

class PacketModeActivation(Exception):
    pass

class Common:

    def __init__(self, clientsocket, address):
        self.sock = clientsocket
        self.addr = address
        self.str_addr = address[0] + ', ' + str(address[1])

    def address(self):
        return self.str_addr

    def sendBytes (self, bts):
        self.sock.sendall (bts)

    def sendPacket (self, bts):
        size = len(bts)
        assert size < 0x80000000
        size = socket.htonl(size)
        size = struct.pack('I',size)
        self.sendBytes (size + bts)
        if hard_debug_mode:
            print ('size', size)
            print ('sent', bts)

    def sendPakString(self, msg):
        bts = msg.encode()
        self.sendPacket (bts)
        if soft_debug_mode:
            prefix_print ("<<<envoi<<< ", msg, SEND)

    def sendString(self, msg):
        bts = msg.encode()
        self.sendBytes (bts)
        if soft_debug_mode:
            prefix_print ("<<<envoi<<< ", msg, SEND)

    def recvSize (self, size):
        bts = self.sock.recv(size)
        if hard_debug_mode:
            print ('recv', bts)

        if not len(bts):
            raise ConnectionResetError

        while len(bts) < size:
            nbts = self.sock.recv (size-len(bts))
            if hard_debug_mode:
                print ('recvn', nbts)

            if not len(nbts):
                raise ConnectionResetError
            bts += nbts
        return bts


    def sendCode (self, code):
        code = socket.htonl (code)
        code = struct.pack("I", code)
        self.sendBytes (code)

    def _getCode(self, bt):
        code = struct.unpack('I',bt)[0]
        code = socket.ntohl (code)
        return code

    def recvCode (self):
        bt = self.recvSize(4)
        return self._getCode(bt)

    def recvPacket(self):
        size = self.recvCode ()
        assert not size & 0x80000000

        bts = self.recvSize (size)
        return bts

    def _decode(self,msg):
        try:
            msg = msg.decode()
            return msg
        except UnicodeDecodeError:
            # if self.pseudo is None:
            print("A client", file=sys.stderr, end=' ')
            # else:
                # print(self.pseudo, file=sys.stderr,end=' ')
            print("sent invalid characters to the server", file=sys.stderr)

            if msg == b'\xff\xf4\xff\xfd\x06':
                print("Ctrl-C was sent by client", file=sys.stderr)
                self.send("Utilisez plutôt la commande 'quit' que Ctrl-C\n")
            elif msg == b'\xff\xed\xff\xfd\x06':
                print("Ctrl-Z was sent by client", file=sys.stderr)
                self.send("Utilisez plutôt la commande 'quit' que Ctrl-Z\n")
            else:
                print("First 100 chars:", msg[:100], file=sys.stderr)
                self.send("Invalid string sent\nVerify your program compatibility with UTF-8 characters!\n")

            return None


    def recvString (self):
        msg = self.sock.recv(BUFLEN)
        msg = self._decode(msg)
        if soft_debug_mode:
            prefix_print (">>>recu >>> ", msg, RECV)
        return msg


    def recvPakString (self):
        bts = self.recvPacket()
        msg = self._decode(bts)
        if soft_debug_mode:
            prefix_print (">>>recu >>> ", msg, RECV)
        return msg

    def disconnect(self):
        self.sock.close()

    def __del__(self):
        del self.sock


def flagToLanguage(i):
    if i == 0xC8:
        return 'C++'

    if i == 0x85:
        return 'python'

    if i == 0xCC:
        return 'C'

    if i == 0xEA:
        return 'java'

    raise LanguageError


TERMBLUE = "\x1B[34m"
TERMBLUEBOLD = "\x1B[34;1m"

TERMRESET = "\x1B[0m"


class NetServer (Common):

    def __init__(self, clientsocket, address):
        Common.__init__(self, clientsocket, address)
        self.packet_mode = False
        self.sendString (intro_msg)

    def sendColorString(self, msg):
        self.sendString (TERMBLUEBOLD + msg + TERMRESET)

    def recvFirst(self):

        init = self.recvSize(4)
        code = self._getCode(init)

        if code & 0xFFFFFF00 != 0xFFFFFF00:
            # not in packet mode
            if soft_debug_mode:
                print('Normal mode activated')
                print('Init was:', init)
            self.receive = self.recvString
            self.send    = self.sendColorString
            msg = self.recvString()
            if msg:
                msg = init.decode() + msg
            else:
                msg = init.decode()
            if soft_debug_mode:
                print ('Received:',msg)
            return msg

        else:
            if soft_debug_mode:
                print('Packet mode activated')
            langage = flagToLanguage(code & 0xFF)
            self.packet_mode = True

            # send back the code to acknowledge
            self.sendCode (code)

            self.receive = self.recvPakString
            self.send    = self.sendPakString

            msg = self.receive()
            if soft_debug_mode:
                print ('Received:',msg)
            return msg

    send = Common.sendString
    receive = recvFirst



class NetClient (Common):

    def __init__(self, address = "localhost", port = 9999):

        try:
            sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
            Common.__init__(self, sock,(address, port))
            self.sock.connect ((socket.gethostbyname(address), port))
        except ConnectionError as e:
            eprint (e)
            eprint ("Erreur à la connexion, vérifiez l'adresse et le port.")
            eprint ("Peut-être que le serveur a lamentablement planté... ?")
            exit (1)

        try:
            # receive intro message
            intro = self.recvSize (intro_msglen)
            # it is also possible to check that intro ends with \n\n

            code = 0xFFFFFF85
            self.sendCode(code)

            ret = self.recvCode()
            while ret != code:
                ret = self.recvCode()
        except ConnectionResetError as e:
            eprint ("Connexion interrompue par le serveur durant l'initialisation.")
            exit (1)

        print("Vous êtes connecté·e au serveur AppoLab.")
        if soft_debug_mode:
            prefix_print('>>>recu >>> ', intro.decode(), RECV)

    def send (self, msg):
        try:
            self.sendPakString (msg)
        except (BrokenPipeError, ConnectionResetError) as e:
            eprint ("Connexion interrompue par le serveur durant envoi.")
            exit (1)

    def receive (self):
        try:
            return self.recvPakString()
        except ConnectionResetError as e:
            eprint ("Connexion interrompue par le serveur durant réception.")
            exit (1)

    def sendReceive (self, message):
        self.send (message)
        return self.receive ()


    envoyer = send
    recevoir = receive
    envoyerRecevoir = sendReceive
    input = sendReceive

    deconnexion = Common.disconnect
    sendRaw = Common.sendPacket


client_class = None

def connexion (host='im2ag-sncf.univ-grenoble-alpes.fr', port=9999):
    global client_class
    client_class = NetClient (host, port)

def envoyer (msg):
    global client_class
    client_class.envoyer(msg)

def recevoir ():
    global client_class
    return client_class.recevoir()

def envoyerRecevoir (msg):
    envoyer (msg)
    msg = recevoir()
    if do_attente_automatique:
        attendre()
    return msg

def deconnexion ():
    global client_class
    client_class.disconnect()

def debug_mode (mode):
    global soft_debug_mode
    soft_debug_mode = mode

debug=debug_mode

def attente_automatique (mode):
    global do_attente_automatique
    do_attente_automatique = mode

def sendRaw (msg):
    global client_class
    client_class.sendRaw (msg)

def attendre():
    color_print("--- appuyez sur entree pour continuer ---\n", WAIT)
    input ()

def attendre_message():
    color_print("--- entrez votre message et appuyez sur entree pour continuer ---\n", WAIT)
