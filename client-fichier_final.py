#!/usr/bin/env python3

from lib.Network import *

# Affiche les échanges avec le serveur (false pour désactiver)
debug_mode (True)

#Hello c'est moi :)

def decale (liste, decalage):
    
    """fait un décalage de César d'un message dont la liste de caractères est pris en arguments, et le decalage à effectuer aussi."""

    message_decrypte=""

    
    decalage=-decalage
        
    if decalage<1:
        
        decalage=26+decalage
        
    for lettre in liste:
        
        lettreSuivante=chr((ord(lettre))+decalage)

        if ord(lettreSuivante)>ord("z"):
            
            lettreSuivante=chr((ord(lettreSuivante))-26)
            
        elif ord(lettreSuivante)>ord("Z") and ord(lettreSuivante)<ord("a"):
            
            lettreSuivante=chr((ord(lettreSuivante))-26)
            
        if ord(lettre)<ord("A") or ord(lettre)>ord("z") or (ord(lettre)>ord("Z") and ord(lettre)<ord("a")):

            lettreSuivante=lettre

        if decalage>7 and ord(lettre)>ord("Z")-decalage and ord(lettre)<=ord("Z"):

            lettreSuivante=chr(ord(lettreSuivante)-26)

        message_decrypte=message_decrypte+lettreSuivante

    return message_decrypte

def liste_finale(liste):

    liste_finale=[]

    sequence=[]

    for lettre in liste:

        if lettre not in sequence:

            sequence.append(lettre)
            
            liste_finale.append(lettre)

        else :
            i=sequence.index(lettre)

            if i >=1:
                
                liste_finale.append(sequence[i-1])

            else:
                liste_finale.append(sequence[len(sequence)-1])

            sequence.append(sequence.pop(i))

    return liste_finale

def retour(liste):
    
    sequence=[]
    
    retour=[]
    
    for lettre in liste:

        if lettre not in sequence:

            sequence.append(lettre)

            retour.append(lettre)

        else:

            i=sequence.index(lettre)

            if i==len(sequence)-1:

                retour.append(sequence[0])
                sequence.append(sequence.pop(0))

            else:
                
                retour.append(sequence[i+1])

                sequence.append(sequence.pop(i+1))

    return retour



    
    
print ("Bienvenue dans le client tutoriel d'AppoLab !")

# En cas de problème, essayer sur le port 443 en utilisant à la place la ligne 
# ci-dessous
# connexion ("im2ag-sncf.u-ga.fr", 443)
connexion ()

# modifiez la ligne ci-dessous en mettant vos identifiant et mot de passe.
reponse = envoyerRecevoir("login DALaborie 2600")


while True:
    attendre_message()
    load=input("taper 'load' suivi du nom de l'exercice à charger\n")
    reponse = envoyerRecevoir(load)
    if load=="load projetX":
        attendre_message()
        reponse=envoyerRecevoir("depart")
        reponse=envoyerRecevoir("aide")
        lettre=list(reponse)
        print(lettre)
        d=ord(lettre[0])-ord("C")

        decryptage=decale(lettre, d)
        print(decryptage)
        reponse=envoyerRecevoir("Veni, vidi, vici")

    elif load=="load planB":

        attendre_message()
        reponse=envoyerRecevoir("depart")
        #"hasta la revolucion"
        reponse=envoyerRecevoir("aide")

        lettre=list(reponse)

        d=ord(lettre[0])-ord("C")
        solution='hasta la revolucion'

        decryptage=decale(solution, d)

        reponse=envoyerRecevoir(decryptage)

        lettre=list(reponse)
        d=ord(lettre[17])-ord("C")
        solution='hasta la victoria siempre'

        reponse=envoyerRecevoir(decale(solution, d))

    #elif load==crypteSeq:

    
    break

    
    
