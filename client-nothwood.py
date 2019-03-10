#!/usr/bin/env python3

from lib.Network import *

def list_finale(liste):

    liste_finale=[]

    sequence=[]

    for lettre in liste:

            if lettre not in liste_finale:

                sequence.append((lettre, lettre))
            
                liste_finale.append(lettre)  

            else:

                for lettre2 in liste_finale:

                    if (lettre, lettre2) in sequence:

                        k=sequence.index((lettre, lettre2))

                        (a, b)=sequence.pop(k)

                        if k >= 1:

                            (c, d)=sequence.pop(k-1)
                                         
                        else :

                            (c, d)=sequence.pop(len(sequence)-1)

                        e=b
                    
                        b=d

                        d=e

                        if k<1:
                                         
                            sequence.append((c, d))

                        else:

                            sequence.insert(k-1, (c,d))
                    
                        sequence.append((a, b))
                    
                        liste_finale.append(b)

                        break
                    
    

    return liste_finale
        

# Affiche les échanges avec le serveur (false pour désactiver)
debug_mode (True)

print ("Bienvenue dans le client tutoriel d'AppoLab !")

# En cas de problème, essayer sur le port 443 en utilisant à la place la ligne 
# ci-dessous
# connexion ("im2ag-sncf.u-ga.fr", 443)
connexion ()

# modifiez la ligne ci-dessous en mettant vos identifiant et mot de passe.
reponse = envoyerRecevoir("login DALaborie 2600")

reponse = envoyerRecevoir("load Nothwoods")
print(reponse)
while True:
    attendre_message()
    
    
    reponse=envoyerRecevoir("depart")
    listeacrypter=list("""Cher Bob,

Je suis inquiete, je crois que ton algorithme est trop previsible, je te 
propose de l'ameliorer.  Voici mon idee :
- je te propose de conserver ton algorithme a base de sequence, mais de 
  stocker un peu plus de choses : pour chaque caractere, nous allons stocker 
  en plus le caractere auquel il est associe (celui qui est utilise a sa place 
  dans le texte encrypte)
- la premiere fois qu'il est rencontre, lors de son insertion, un caractere 
  est associe a lui meme
- les fois suivantes, lorsqu'un caractere a deja ete vu, nous procederons 
  comme dans ton algorithme, mais au lieu de remplacer le caractere en entree 
  par le precedent dans la sequence, nous echangerons son association avec 
  l'association du caractere precedent dans la sequence
- le caractere de sortie est produit ensuite, apres insertion ou echange, en 
  ecrivant l'association du caractere en entree
- comme dans ton algorithme, l'association est ensuite deplacee en fin de 
  sequence.

J'ai essaye sur quelques messages, je pense que ce nouvel algorithme sera tres 
difficile a craquer. Montre moi dans la suite de cet exercice que tu as compris 
en renvoyant ce message code avec cet algorithme. Je t'enverrai alors mon 
prochain message.

Meilleurs sentiments,
Alice.

PS: Je pense avoir ete assez claire, mais voici tout de meme un exemple sur le 
texte 'abcbcca'.

Seq:    <vide>
Output: <vide>

Char: a
Seq:    (a,a)
Output: a

Char: b
Seq:    (a,a) (b,b)
Output: ab

Char: c
Seq:    (a,a) (b,b) (c,c)
Output: abc

Char: b
Seq:    (a,b) (c,c) (b,a)
Output: abca

Char: c
Seq:    (a,c) (b,a) (c,b)
Output: abcab

Char: c
Seq:    (a,c) (b,b) (c,a)
Output: abcaba

Char: a
Seq:    (b,b) (c,c) (a,a)
Output: abcabaa

Output Final: abcabaa
""")

    repons=list_finale(listeacrypter)
    reponse=envoyerRecevoir(''.join(repons))
    
    break


    
    
