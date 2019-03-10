#!/usr/bin/env python3

from lib.Network import *

# insertion des defs direct dans le fichier
# Gestion des interactions
def menu() :
    affichage = """
************************************************
**** Quel exercice souhaitez-vous lancer ? *****
*       1 : ProjetX                            *
*       2 : Decrypte-v1                        *
*       3 : PlanB                              *
*       4 : CrypteSeq                          *
************************************************ """
    print(affichage)
    choix = input("Votre choix = ")
    
    return choix

#Gestion du cryptage/decryptage
def caesar(ligne) :
    """ Retourne l'écart utilise pour le cryptage"""

    chaine = ligne[0]
    premiere = chaine[0]

    ecart = int(ord("C") - ord(premiere))

    return ecart

def traduitLigne(ligne, decalage) :
    """ Traduit une ligne encodée (string ou liste).
    retourne la ligne traduite """
    #Pour chaque caractère de la ligne, retourner le vrai carac dans la chaine
    origin = ligne
    new = ""

    i = 0
    while i < len(origin) :
        casse = trouveCasse(origin[i])
        new += trouveLettre(origin[i], decalage, casse)
        i +=1

    return new

def trouveCasse(carac) :
    """ retourne la casse d'une lettre """
    if str.isupper(carac) :
        return "maj"
    else :
        return "min"

def trouveLettre(carac, decalage, casse="min") :
	""" Trouve le caractere demande avec le decalage demande et la casse eventuelle
		dans l'alphabet et le retourne""" # Ameliorable je pense

    # ALPHABET ##############################
    liste = []
    char = 97
    
    i = 0
    while i < 26 :
        liste.append(chr(char))
        i += 1
        char += 1
    ##########################################

    neo_carac = carac
    i = 0
    for c in liste :
        if carac.lower() == liste[i] :
            if i + int(decalage) >= len(liste) :
                 neo_carac = liste[(i + int(decalage)) - len(liste)]
            else :
                neo_carac = liste[i + int(decalage)]
        i+= 1

    if casse == "maj" :
        return neo_carac.upper()
    else :
        return neo_carac.lower()

def epureServeur(chaine, suppr) :
	""" Supprime la chaine 'suppr' du début de la chaine 'chaine' 
		Retourne la chaine """
    enleve = suppr
    pure = chaine.lstrip(enleve)

    return pure

def encrypte(message, sequ = []) :
    """ Encrypte une ligne. Retourne la ligne encryptee ainsi
    que la sequence (liste) en cours """
    
    origin = message
    new = ""

    sequence = sequ

    for c in origin :
        if c in sequence :
            if sequence[0] == c :
                 new += sequence[len(sequence)-1]
            else :
                new += sequence[trouveC(c,sequence) - 1]
            sequence.pop(trouveC(c,sequence))
            sequence.append(c)
        else :
            sequence.append(c)
            new += c
            
    return new, sequence

def trouveC(char, sequence, decalage = 0) :
    """ Cherche un carac (char) dans une liste (sequence)
        et renvoie l'indice (int) selon le décalage demandé """
    
    i = 0
    while i < len(sequence) :
        if char == sequence[i] :
            return i + decalage
        i += 1

    return i + decalage

def listToChaine(liste) :
    """ Reçoit une liste Renvoie la liste sous
    format d'une chaine unique """
    texte = ""
    for ligne in liste :
        texte += ligne

    return texte
        
def encrypteFile(file)  :
    """ Traitement complet d'ncryptage de fichier
    Retourne une liste """
    texte = []
    new_texte = []

    f = open(file)

    for ligne in f :
        texte.append(ligne)
        
    f.close()
    new_ligne = ""
    sequence = []
        
    for ligne in texte :        
        new_ligne, sequence = encrypte(ligne, sequence)
        new_texte.append(new_ligne)
     
    return new_texte

def decrypte(message, sequ = []) :
    """ Decrypte une ligne.
    retourne la ligne decryptee """
    
    origin = message
    new = ""
    
    sequence = sequ

    for c in origin :    
        #Je checke si le carac est stocké dans la séquence
        if c in sequence :
            #Il est bien là, je traite
            if sequence[len(sequence) - 1] == c :
                #Si le dernier carac VAUT carac,
                #j'ajoute à ma ligne le premier carac de la seq
                new += sequence[0]
                #ajouter à la fin de la sequence
                sequence.append(sequence[0])
                #supprimer du début de la sequence
                sequence.pop(0)
            else :
                #Je cherche le carac suivant dans la seq
                c_suivant = sequence[trouveC(c,sequence, decalage = 1)]
                #J'ajoute à ma ligne le carac suivant
                new += c_suivant
                #Je supprime de la sequence le carac suivant par son indice            
                indice_suivant = trouveC(c,sequence, decalage = 1)
                sequence.pop(indice_suivant)
                #Et j'ajoute à la sequence le carac suivant
                sequence.append(c_suivant)

        else :
            #Sinon je l'ajoute à ma séquence
            sequence.append(c)
            new += c

    return new

#Traitement des exercices
def runProjetX():
    print("Lancement de ProjetX :")
    #ProjetX
    reponse = envoyerRecevoir("load projetX")
    reponse = envoyerRecevoir("help")
    #récupérer la réponse et la traiter
    decalage = caesar(reponse)
    reponse = envoyerRecevoir(traduitLigne(reponse, decalage ))
    #Envoyer le mdp
    reponse = envoyerRecevoir("start")
    reponse = envoyerRecevoir("Veni, vidi, vici")

def runDecrypte():
    print("Lancement de Decrypte-V1 :")
    #Decrypte-v1
    reponse = envoyerRecevoir("load decrypte-v1")
    reponse = envoyerRecevoir("start")
    
    while reponse != "L'exercice est terminé !" :
        reponse = envoyerRecevoir(traduitLigne(reponse, -5))
    
def runPlanB():
    print("Lancement de PlanB :")
    #Plan B
    reponse = envoyerRecevoir("load planB")
    reponse = envoyerRecevoir("help")
    decalage = caesar(reponse)
    reponse = envoyerRecevoir(traduitLigne(reponse, decalage ))
    reponse = envoyerRecevoir("start")
    reponse = envoyerRecevoir(traduitLigne("hasta la revolucion", decalage))
    texte = epureServeur(reponse, "Bonne réponse !")
    decalage = caesar(texte)
    print(traduitLigne(reponse, decalage))
    reponse = envoyerRecevoir(traduitLigne("hasta la victoria siempre", decalage))
    
def runCrypteSeq():
    print("Lancement de CrypteSeq :")
    #crypteSeq
    reponse = envoyerRecevoir("load crypteSeq")
    fichier = "test.txt"

    texte = encrypteFile(fichier)

    chaine = listToChaine(texte)

    reponse = envoyerRecevoir("start")
    reponse = envoyerRecevoir(chaine)

    #Decryptage de la réponse
    texte = epureServeur(reponse, "Je savais que je pouvais te faire confiance, Alice ! Voici mon message en retour:\n")
    print(decrypte(texte))

# Affiche les échanges avec le serveur (false pour désactiver)
debug_mode (True)

print ("Bienvenue dans le client tutoriel d'AppoLab !")

# En cas de problème, essayer sur le port 443 en utilisant à la place la ligne 
# ci-dessous
connexion ("im2ag-sncf.u-ga.fr", 443)
#connexion ()

# modifiez la ligne ci-dessous en mettant vos identifiant et mot de passe.
reponse = envoyerRecevoir("login DADenizot 9258")

#Menu
choix = menu()
if choix in ["1","2","3","4"] :
    if choix == "1" :
        runProjetX()
    if choix == "2" :
        runDecrypte()
    if choix == "3" :
        runPlanB ()
    if choix == "4" :
        runCrypteSeq()
else :
    print("""
--------------------------------------------------------
!!! Merci de bien vouloir choisir entre 1, 2, 3 ou 4 !!!
    Recommençons
--------------------------------------------------------""")
    menu()


while True:
    attendre_message()
    message = input()
    if message != "":
        reponse = envoyerRecevoir(message)
