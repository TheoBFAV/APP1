#!/usr/bin/env python3

from lib.Network import *

# Affiche les échanges avec le serveur (false pour désactiver)
debug_mode (False)

print ("""Bienvenue dans cette introduction à AppoLab !

AppoLab est un serveur d'exercices algorithmiques que vous allez devoir 
utiliser pour vos APPs. Je vais vous guider pas à pas pour que vous 
puissiez vous débrouiller tout·e seul·e.""")

attendre()

print ("""
Le client va maintenant tenter de se connecter automatiquement au serveur 
AppoLab. Il vous faut bien entendu pour cela une connection internet.
(En cas d'erreur, éditez le fichier python et modifiez la ligne 
'connexion' comme indiqué dans le commentaire.)""")
attendre()

# En cas de problème, essayer sur le port 443 en utilisant à la place la ligne 
# ci-dessous
# connexion ("im2ag-sncf.u-ga.fr", 443)
connexion ()

print ("""
Si tout va bien, vous devez avoir reçu le message de bienvenue d'AppoLab. Si 
non, arrêtez ce programme (avec Ctrl-C) et demandez de l'aide à un·e 
enseignant·e.""")

attendre()

print ("""
Comme indiqué, commencez par vous loguer avec l'identifiant et le mot de 
passe qui vous ont été fournis. Entrez les au clavier ainsi : 
login toto 12345678""")


attendre_message()
login = "login DABeard 1634"
reponse = envoyerRecevoir(login)
print(reponse)


print ("""
Bravo, vous venez de vous identifier auprès du serveur !""")

attendre()

print ("""
Vous êtes maintenant prêt·e à lancer l'exercice.
Lancez le grâce à la commande 'load'. Vous avez le choix entre "projetX",
"planB" et "crypteSeq" """)

while True :
    attendre_message()
    load = input()
    if load == "":
        print("""Tapez "load projetX", "load planB" ou "load crypteSeq"
        s'il vous plait.""")
    else :
        reponse = envoyerRecevoir(load)
        print(reponse)
        break

if load == "load projetX":
    #démarrer l'exercice
    attendre_message()
    message = "depart"
    print(message,"\n")
    reponse = envoyerRecevoir(message)
    print(reponse)

    #la réponse attendue
    attendre_message()
    message = "Veni, vidi, vici"
    print(message,"\n")
    reponse= envoyerRecevoir(message)
    print(reponse)


elif load == "load planB":
    #démarrer l'exercice
    attendre_message()
    message = "depart"
    print(message,"\n")
    reponse = envoyerRecevoir(message)
    print(reponse)

    attendre_message()
    message = "aide"
    print(message,"\n")
    reponse = envoyerRecevoir(message)
    print(reponse)

    def decalage(message_secret):
        """Fonction pour trouver le décalage utilisé
        en se basant sur la premiere lettre du message """
        liste=list(message_secret)
        decalage = ord(liste[0])-ord("C")
        return decalage

    def cryptage(message,decalage):
        """fonction permettant le cryptage de "message" en fonction du décalage
        "décalage" """
        msg_crypte=""
        if decalage >0 :
            for i in message:
                if ord(i)<ord("A") or ord(i)>ord("z") or(ord(i)>ord("Z") and ord(i)<ord("a")):
                    lettre=i #pour les caractères qui ne sont pas des lettres
                elif ord(i)>=ord("a") and ord(i)<= ord("z"): #pour les minuscules
                    ord_crypte=ord(i)-decalage
                    if ord_crypte<ord("a"):
                        ord_crypte=ord_crypte+26 #pour revenir à "z" avant "a"
                    lettre = chr(ord_crypte)
                else :  #et les majuscules
                    ord_crypte=ord(i)-decalage
                    if ord_crypte<ord("A"):
                        ord_crypte=ord_crypte+26 #pour revenir à "Z" avant "A"
                    lettre = chr(ord_crypte)
                msg_crypte=msg_crypte+lettre
        else :  #même chose avec un décalage dans l'autre sens
            for i in message:
                if ord(i)<ord("A") or ord(i)>ord("z") or(ord(i)>ord("Z") and ord(i)<ord("a")):
                    lettre=i
                elif ord(i)>=ord("a") and ord(i)<= ord("z"):
                    ord_crypte=ord(i)-decalage
                    if ord_crypte>ord("z"):  
                        ord_crypte=ord_crypte-26 #pour revenir à "a" après "z"
                    lettre = chr(ord_crypte)
                else :
                    ord_crypte=ord(i)-decalage
                    if ord_crypte>ord("Z"):
                        ord_crypte=ord_crypte-26 #pour revenir à "A" après "Z"
                    lettre = chr(ord_crypte)
                msg_crypte=msg_crypte + lettre
        return msg_crypte

    decalage = decalage(reponse)
    hasta = cryptage("hasta la revolucion",decalage)

    attendre_message()
    message = hasta
    print(message,"\n")
    reponse = envoyerRecevoir(message)
    print(reponse)

    def decalage_2(message_secret):
        """fonction permettant de trouver le décalage à partir du
        17eme caractère"""
        liste=list(message_secret)
        decalage = ord(liste[16])-ord("C")
        return decalage

    hasta_2=cryptage("hasta la victoria siempre",decalage)

    attendre_message()
    message = hasta_2
    print(message,"\n")
    reponse = envoyerRecevoir(message)
    print(reponse)

elif load == "load crypteSeq":
    def crypteSeq(message): #definition fonction de cryptage par séquence
        sequence = list()        #initialisation de la séquence vide
        n = len(sequence)-1      #n correspondra à l'index de la dernière lettre de la séquence
        message_crypte = ""           #initialisation du message crypte, le return
        for i in message:                   #pour chaque lettre dans le message
            if i not in sequence :       #si elle n'est pas dans la séquence
                message_crypte+= i  #on l'ajoute au message crypté
                sequence.append(i)   #et également à la séquence
            else :
                index_i=sequence.index(i)    #initialisation position de i dans la séquence
                if i == sequence[0]:    #si 1ere lettre de la séquence
                    j = sequence[n] #on prend la derniere lettre de la séquence
                else :
                    j = sequence[index_i-1] #OU on prend la lettre qui précède i
                message_crypte+=j   #on ajoute cette lettre dans le message crypté
                j_s = sequence.pop(index_i) #on retire la lettre i de la séquence
                sequence.append(j_s) #pour la placer à la fin de celle ci
        return message_crypte   #on retourne le message crypté
       
    attendre_message()
    message = "depart"
    print(message,"\n")
    reponse = envoyerRecevoir(message)
    print(reponse)

    f=open("message_decrypté_4.txt")
    msg = f.readlines() #extraire chaque caractère du fichier dans une liste
    f.close()
    msg="".join(msg)    #transtyper la liste en chaine de caractères

    attendre_message()
    message = crypteSeq(msg)
    reponse = envoyerRecevoir(message)
    print(reponse)

attendre()
print ("Au revoir.")
deconnexion()
