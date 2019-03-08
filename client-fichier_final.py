#!/usr/bin/env python3

from lib.Network import *

# Affiche les échanges avec le serveur (false pour désactiver)
debug_mode (True)

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
        lettre=list(reponse.lower())
        
        d=ord(lettre[0])-ord("c")

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

    elif load== "load crypteSeq":

        attendre_message()
        reponse=envoyerRecevoir("depart")

        liste="""Chere Alice,

Tu as raison, il faut anticiper avant que nous ne soyons reperes. J'ai termine 
dans l'urgence mon nouveau schema de chiffrement. En voici le principe :
- durant l'encryptage, je maintiens une sequence de tous les caracteres deja 
  rencontres, dans l'ordre
- pour chaque caractere c a crypter, je cherche dans la sequence s'il a deja 
  ete rencontre
  - si c'est la premiere fois, je l'ajoute en fin de sequence et je le laisse 
    inchange dans le message crypte
  - sinon, je considere d qui est soit:
    - le caractere qui precede c dans la sequence
    - le dernier caractere de la sequence si c est le premier caractere de la 
      sequence
    je remplace c par d dans le message crypte et je deplace c a la fin de la 
    sequence

Je sais que tu es l'une des rares personne a pouvoir mettre en oeuvre une 
technique complexe comme celle-ci, cela devrait nous proteger un peu plus 
encore. Cependant, pour me montrer que tu as bien compris ma methode, il faut 
dans un premier temps que tu me renvoies ce message crypte comme je viens de 
te l'expliquer. Je t'enverrai alors mon prochain message. Mets ton message 
dans l'exercice 'crypteSeq' (le mot de passe est hasta la victoria siempre).

Bien a toi,
Bob.

PS: (optionnel) pour valider cet exercice sur AppoLab, il suffit de donner le 
mot de passe de crypteSeq (cf ci-dessus) decale a l'oppose comme pour le 
message precedent.

PPS: Pour t'aider, le debut de ce message serait transforme en :

> Cherh Alicr,
> ,TurasuhuluoneuaA,frTtlfou,AtpATuuv uurqfptasqTeeqsuqysu...

Et voici un exemple d'encryption sur le texte 'abcbcca'

Input: abcbcca

Seq:    <vide>
Output: <vide>

Char: a
Seq:    a
Output: a

Char: b
Seq:    ab
Output: ab

Char: c
Seq:    abc
Output: abc

Char: b
Seq:    acb
Output: abca

Char: c
Seq:    abc
Output: abcaa

Char: c
Seq:    abc
Output: abcaab

Char: a
Seq:    bca
Output: abcaabc

Output final: abcaabc
"""

        liste=list(liste)

        liste_f=liste_finale(liste)

        reponse=envoyerRecevoir(''.join(liste_f))

        print(reponse)

        liste=list("""Cherh Alicr,
,MalntciMeirquitnqesiM ulhypeqcsitAoMrolppslllqvrsevrmlsCndmAlmhnp,rtuudimqug ooAmgrpua,sdnv nutiinngn
tsihetvcpd.aSq.r,iloaS
oluusdruvanrrqcvevhmqcr'gmS,MS'thsqem'uiqtaulati,dh rS staS,s mviv
MScvpmmmmnoMMi'ldmdldoguycumtoyMg paodleinod.qnCaa
s'ro Sojl,iousC ebajlsSSinguovuicavnglbonbbSqlstf
shscssndn.Nf'c.mmaN'uuCglNjpmfsntisolrfnifobveeropmsmicceuu
aNuevrmtsonratrui rnataoamosfoMr.rciloutlsNvraetymnvltce
pSCrSp,egtxtvpxrl,egmlysS
exqru'tvorxslfgmMwNwmn genc,uwNewltSguwaddsaoawHpfHuvty,gjtfd.BrpvavnsmBw..tu'""")

        liste_f=retour(liste)

        print(''.join(liste_f))

        liste="""Cher Bob,
,Jhrsui eunqe Jtibsjt,chBuJennjsnrJealgtcceCmunmcimsogpsotmvgmvBarJoJl,mjjBoom
rvttdssb'nhd vp
mo.d.VilJo.aVuicsldn:t-e,d-,jj,lm r,ttissVpmpdthssdjccr''utemeuVvnneuecmmpssadJJsvpuJdhbrd,bcs:e
irgnkdg
qqrjkrnnve
einsogtudodVsnhlk:ddmbodrrhoc 
u tbukpqd,qkan,uunclq
rqnir
kl
:a,anp
so,kc ,l tllpharsrmeeupclrea,pult(oiuqoorlllcariqsqcteqqreieents(iske
mlki
pcsulx  ltapkyix )iVxsd-yctburpiafkmde((Jo-sroylmlxxfes  hsicti,(tsrlce'oedlc d cdqo,'-ec es tn)e
rdc
neaind
tte',capc  r)iamt-ptueeiaojc,rl do-fdepfpqa,dvoc vv tnneprVrrdc ai'ie'lvl,)cn't'cpp,uums
pr)od
pjrrejcasdiVtpfs:ccvnhnrd,mvsnmhaaciuod,vas
r dpcrappc ol tlr
rrrcc rcve
mlt
mtr
almrucmmlc
e,t
dsncfisdruhaugqa,cqgl,v p,auunrrrhraruv pcsrrcjgsnmc
dfnraiet'rcsr
p,nssgc sv tumttarncoaacue't
dsncmosdruv)adc-ndpc pl tlprrpitc'ddidri'odcqcsscqcddd mdlcctn,uderpu c pidnslm,im duga,qn
,ustmh,s
-mvpaper'ncsvv-pnssec s
 turorrrcc r,qcaijor-iuu'eucasdvhtu'spccpnavndag-r'rcsd,m'annoovao o-tq,c'dctcoc)ueetcnve
odjosiauJd.B,lfdcde'x iiqgedsyp   yrhuuei-mmhu)g,tjdgpjllssduuphq)crcmemny'h-yvvpmovmiesma.fo-idqfvrsmeftepnlc-lMgpmeu.hMfe
cMhifdsnqoMraottfdidc( MdurxtfsccdqelluimMjxxaahqMsp

jc'ueq
urtucieyjmctvlggsrdgdevnvdMss
pejncfc-m.i-Jyd'oecoJrcgeyihl'spulmdgiemmsvlehdmdl.fghviMqpmnrlhJMhsss -.AM omg,.PSbrdc:vJmtpJh''luesm rsnatztlAtoosmzullt,nnazosnvM iyrt,d  dopemf dJzxnadzeppr.oln

ly,Vvaab' Al.PtfPt:::<,,oS>.OsxmOOqqqqqqqqq>
ycstth>.d.rr:::krz(kr.pp.OOqq,)a>> >ttxt>>>rr:::>h>(>::r:(ar>pp>OOqaq,)b>> >ttxb>>>rr:::>h>(>::t:(aaara(br>pp>OOqbqq,)c>> >tttc>>>rr:::>h>r>::ta(bbbaa:cr>pp>OOqc,(q )a>>c>ttbb>>>rr:::>h>r>::ta:ccc:b:ar>pp>OOqaq,(  )b>>c>tttb>>>rr:::>h>r>::ta(cccaa:br>pp>OOqb,q(  c)a>>b>tthb>>>rr:::>c>(>::t:(bbbrb(cr>pp>OOqc,qq  cb)a)pp)OO:Fvobs)tnc)  cb)
"""
        liste=list(liste)

        liste_f=retour(liste)

        print(''.join(liste_f))

    
    break

    
    
