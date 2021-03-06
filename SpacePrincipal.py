#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
https://github.com/Eliott-rjd/SpaceInvader.git
Programme principale du SpaceInvader
Eliott RAJAUD et Axel GUILLET
18/12/20
TODO :
    Mettre le deplacement gauche et droite du vaisseau en une seul fct
    Mieux séparer le fichier : faire fichier a part avec les classes et autres avec la création TkInter

    Ajouter d'autres fonctionnalités bonus : sauvegarde du score, plusieurs niveaux
"""

from tkinter import Tk, Label, Canvas, Button, StringVar, PhotoImage, messagebox, Entry, END
import random as rd


class SpaceInvader(Tk):
    def __init__(self):
        '''Role : Initialise la fenêtre tkinter du Jeu
        Sortie : la fonction n'a pas de sortie mais certains boutons appellent d'autres fonctions
        '''
        Tk.__init__(self)
        self.geometry('900x700+200+50')
        self.title('Space Invaders')

        self.protections = []
        self.hauteur = 500
        self.longueur = 500
        self.can = Canvas(self,width = self.hauteur,height = self.longueur)

        self.photo = PhotoImage(file = 'espace.gif')
        self.item = self.can.create_image(0, 0, anchor = 'nw', image = self.photo)

        self.text1 = StringVar()
        self.labelScore = Label(self, textvariable = self.text1)
        self.text2 = StringVar()
        self.labelVie = Label(self, textvariable = self.text2)

        self.buttonQuit = Button(self , text = 'Quitter' , fg = 'red' , command = self.destroy)
        self.buttonReplay = Button(self, text = 'Rejouer' , command = self.rejouer)
        self.newGame = Button(self, text = 'demarrer une partie', command = self.initPartie)

        self.buttonCheatCode = Button(self, text = 'Entrez un code triche' , command = self.getEntry)
        self.entreeCode = Entry(self, width = 20)

        self.labelScore.grid(row = 1, column = 1, sticky = 'w')
        self.labelVie.grid(row = 1, column = 2, sticky = 'e')
        self.newGame.grid(row = 2, column = 3, rowspan = 1, sticky = 'e')
        self.buttonReplay.grid(row = 2, column = 4, rowspan = 1, sticky = "e")
        self.buttonQuit.grid(row = 3, column = 3, rowspan = 1, sticky = "e")
        self.buttonCheatCode.grid(row = 4, column = 3, rowspan = 1, sticky = "e" )
        self.entreeCode.grid(row = 4, column = 4, sticky = "e"  )
        self.can.grid(row = 2 , column = 1, rowspan = 2, columnspan = 2,  sticky = "w")

        self.listAlien = []
        self.nbAlientot = 0
        self.tempsDeplacementInit = 300
        self.tempsDeplacement = self.tempsDeplacementInit              # Il s'agit du temps de déplacement des aliens
        self.listAlienBonus = []
        self.demarrer = 0
        self.score = 0
        self.finPartie = 0
        self.alienBonusPresent = 0
        self.dejaTouche = 0
        self.cheatCode = {"Merci":"2","2469":"4","72g7hy12":"999999999"}
        self.codeTrouve = []
        self.listeClasseInit()
        self.ilots()

    def ilots(self):
        '''Role: créer les ilots de protection
        Entrée : utilise self.protection (qui va prendre plein de petits rectangles)
        et self.ilots (qui regroupe les 3 ilots dans une liste) de la classe
        Sortie : Créer les 3 ilots sur le canvas'''

        self.protections = []
        self.listeIlot= []
        #Création de 5 petits rectangles sur 3 lignes
        for i in range(5):
            for j in range(3):
                a = self.can.create_rectangle(50+i*16, 380+j*16, 50+i*16+16, 380+j*16+16, fill= "white")
                b = self.can.create_rectangle(210+i*16, 380+j*16, 210+i*16+16, 380+j*16+16, fill= "white")
                c = self.can.create_rectangle(370+i*16, 380+j*16, 370+i*16+16, 380+j*16+16, fill= "white")
                self.protections.extend([a,b,c])

                ilot1 = [50+i*16, 380+j*16, 50+i*16+16, 380+j*16+16]
                ilot2 = [210+i*16, 380+j*16, 210+i*16+16, 380+j*16+16]
                ilot3 = [370+i*16, 380+j*16, 370+i*16+16, 380+j*16+16]
                self.listeIlot.extend([ilot1,ilot2,ilot3])

    def listeClasseInit(self):
        '''Role : Créer les lignes d'aliens (ici il y a 6 aliens par lignes avec 3 lignes)
        Entrée : Utilisation de listAlien de la classe
        Sortie : Affichage de tous les aliens et création de la liste complète des aliens comprenant elle même
        3 listes (qui sont les 3 lignes)'''

        listAlienLigne1 = []
        listAlienLigne2 = []
        listAlienLigne3 = []
        self.listAlien = []
        for j in range(0,3):
            for i in range(0,6):
                if j == 0:
                    cAlien = Alien(self.can,i*60,j*60)
                    listAlienLigne1.append(cAlien)
                    self.nbAlientot += 1
                elif j == 1:
                    cAlien = Alien(self.can,i*60,j*60)
                    listAlienLigne2.append(cAlien)
                    self.nbAlientot += 1
                else:
                    cAlien = Alien(self.can,i*60,j*60)
                    listAlienLigne3.append(cAlien)
                    self.nbAlientot += 1
        self.listAlien = [listAlienLigne1,listAlienLigne2,listAlienLigne3]


    def initPartie(self):
        '''Role : demarrer la partie à l'appui du bouton. Met en place les commandes, le score et les vies
        Entrée : self.demarrer de la classe, qui passe à 1 après l'initialisation de la partie pour éviter les bugs lier au spam du bouton démarrer
        Sortie : lancement du déplacement des aliens'''
        if self.demarrer == 0:
            for k in range(len(self.listAlien)):
                for i in range(len(self.listAlien[k])):
                    self.listAlien[k][i].deplacementAlien()
                    self.listAlien[k][i].laser()
            self.bind("<Left>",cVaisseau.deplacementVaisseauLeft)
            self.bind("<Right>",cVaisseau.deplacementVaisseauRight)
            self.bind("<space>",cVaisseau.laser)
            self.createAlienBonus()
            self.text2.set("Lifes : "+str(cVaisseau.vie))
            self.text1.set("Score : "+str(self.score))
            self.demarrer = 1
            cVaisseau.stop = 0

    def rejouer(self):
        '''Role : permet de rejouer en nettoyant le canvas et en réinitialisant les données (vie, score, images)
        Entrée : prend le canvas, cVaisseau.present (représente la présence ou non d'un laser du vaisseau), la liste des aliens,
        le score et le nombre de vie
        Sortie : remise à zéro et replacement du vaisseau ainsi que des aliens à leur position initiale, reformation des ilots de protection
        et suppression des tirs lancés au moment du clique sur le bouton.'''

        #Destruction des items
        if cVaisseau.present == 1:
            self.can.delete(cVaisseau.tir)
            cVaisseau.present = 0
        for k in range(len(self.listAlien)):
            for i in range(len(self.listAlien[k])):
                self.can.delete(self.listAlien[k][i].imgAlien)
                self.listAlien[k][i].stop = 1
                if self.listAlien[k][i].present == 1:
                    self.can.delete(self.listAlien[k][i].tir)
                    self.listAlien[k][i].present = 0
        for j in range(len(space.listeIlot)):
            self.can.delete(space.listeIlot[j])
            self.can.delete(space.protections[j])

        #reinitialisation des items
        self.ilots()
        self.nbAlientot = 0
        self.listeClasseInit()
        self.demarrer = 0
        self.can.delete(cVaisseau.imgVaisseau)
        cVaisseau.imgVaisseau = self.can.create_image(self.longueur/2, self.hauteur, anchor = 'sw', image = cVaisseau.vaisseau)
        cVaisseau.xv = self.longueur/2
        cVaisseau.stop = 1
        cVaisseau.vie = 3
        self.text2.set("Lifes : "+str(cVaisseau.vie))
        self.score = 0
        self.text1.set("Score : "+str(self.score))
        self.codeTrouve = []

        if len(self.listAlienBonus) == 1:
            self.can.delete(self.listAlienBonus[0].imgAlienBonus)
            self.listAlienBonus[0].stop = 1
        self.alienBonusPresent = 0
        self.finPartie = 0


    def createAlienBonus(self):
        '''Role : création de l'alien bonus de manière aléatoire
        Entrée : self.finParie (pour savoir si il y a une partie en cours, ce qui permet d'arrêter la création d'aliens si la partie se finit,
        listAlien, notAliensup (savoir s'il y a les aliens de base sur la haut du canvas)  et alienBonusPresent (pour savoir s'il y en a deja un)
        Sortie : appartion de l'alien Bonus'''

        if self.finPartie == 0:
            notAliensup = 0
            #creation de l'alien bonus uniquement si les aliens sont descendus au moins une fois
            for k in range(len(self.listAlien)):
                for i in range(len(self.listAlien[k])):
                    if self.listAlien[k][i].y == 0:
                        notAliensup = 1

            #creation de l'alien bonus
            if notAliensup == 0 and self.alienBonusPresent == 0:
                rnd = rd.random()*40
                if rnd <= 1:
                    cAlienBonus = AlienBonus(self.can)
                    if len(self.listAlienBonus) == 1:
                        self.listAlienBonus.pop(0)
                    self.listAlienBonus.append(cAlienBonus)
                    self.alienBonusPresent = 1
                    cAlienBonus.deplacementAlienBonus()
            space.after(200,self.createAlienBonus)


    def bordAlien(self):
        '''Role : Gérer la colision avec les bords
        Entrée : self.dejaTouche, self.tempsDeplacement, la liste des aliens
        Sortie : s'il y a contact, donne la valeur 1 à self.bord pour tous les aliens si le bord droit est touché, -1 si c'est le bord gauche, (ce qui va permettre aux aliens de changer de direction
        dans deplacementAlien), si aucun bord n'est touché, self.bord reste à 0'''

        if self.dejaTouche == 0:
            for k in range(len(self.listAlien)):
                if len(self.listAlien[k]) != 0:
                    if (self.listAlien[k])[len(self.listAlien[k])-1].x+(self.listAlien[k])[len(self.listAlien[k])-1].dx+(self.listAlien[k])[len(self.listAlien[k])-1].alien.width() > self.longueur:
                        for k in range(len(self.listAlien)):
                            for i in range(len(self.listAlien[k])):
                                self.listAlien[k][i].bord = 1

            for k in range(len(self.listAlien)):
                if len(self.listAlien[k]) != 0:
                    if self.listAlien[k][0].x+self.listAlien[k][0].dx < 0:
                        for k in range(len(self.listAlien)):
                            for i in range(len(self.listAlien[k])):
                                self.listAlien[k][i].bord = -1
            self.dejaTouche = 1
            time = 0.5*self.tempsDeplacement
            space.after(int(time),self.reinit)


    def reinit(self):
        '''Role : réinitialiser self.dejaTouche à 0, en restant à 1 un certains temps, on évite que plusieurs aliens rentrent dans la fonction bordAlien et réinitialise le self.bord des aliens qui ont déjà bougé à + ou -1
        lorsque plusieurs aliens touchent le bord en même temps'''
        self.dejaTouche = 0


    def getEntry(self):
        '''Role : Permet de récupérer le cheatCode saisie par l'utilisateur
        Entrée : aucune, on va récuperer ce que l'utilisateur va saisir dans l'Entry(zone de texte)
        Sortie : appel la fonction de verification du code par rapport au code saisie et remet a vide l'Entry '''

        # On récupère la saisie de l'utilisateur, puis on rafraichit la zone de texte
        essaie = self.entreeCode.get()
        self.entreeCode.delete(0,END)
        return self.verifCode(essaie)

    def verifCode(self,essaie):
        '''Role : Vérfier si le code de triche saisie fait partie de la liste des différents codes
        Entrée : essaie (le code de triche saisie) et le dictionnaire contenant les codes et leur valeur (points de vie)
        Sortie : Rajoute un certains nombre de vies en fonction du code saisie, self.codeTrouve empêche le spam d'ajouts de vies une fois que le code a déjà été saisi'''

        for clé in self.cheatCode.keys():
            if essaie == clé and essaie not in self.codeTrouve:
                cVaisseau.vie += int(self.cheatCode[clé])
                self.text2.set("Lifes : "+str(cVaisseau.vie))
                self.codeTrouve.append(clé)

    def vitesseAlien(self):
        '''Role : Accélère la vitesse des aliens lorsque le nombre d'aliens diminue
        Entrée : self.nbAlientot, le nombre initial d'aliens, alienTué et alienCunter nous servent à compter le nombre d'aliens tués
        Sortie : Renvoie le nouveau temps de déplacement des aliens en fonction du nombre d'aliens tués'''

        alienTué = 0
        alienCunter = 0
        for k in range(len(self.listAlien)):
            for i in range(len(self.listAlien[k])):
                alienCunter += 1
        alienTué = self.nbAlientot - alienCunter
        self.tempsDeplacement = self.tempsDeplacementInit*(1 - alienTué*0.05)



class Alien():
    def __init__(self,canvas,x,y):
        '''Role : Initialisation de la classe Alien
        Entrée : le canvas et la position des aliens
        '''
        self.can = canvas
        self.x  = x
        self.y  = y
        self.dx = 7
        self.stop = 0
        self.present = 0
        self.bord = 0
        self.alien = PhotoImage(file = 'alien.gif')

        self.imgAlien = self.can.create_image(self.x, self.y, anchor ='nw',image = self.alien)
        self.xLaser = self.x + self.alien.height()/2
        self.yLaser = self.y + self.alien.width()
        self.dyLaser = 10
        self.ind = -1
        self.score_alien = 100
        self.probaLaser = 20


    def deplacementAlien(self):
        '''Role : permet de déplacer les aliens
        Entrée : la canvas, self.stop (pour savoir si les aliens sont arrêtés, donc s'ils sont détruits ou si la partie est finie), self.bord (pour savoir
        s'il y a eu un contact avec un bord), listAlien, self.dx et self.alien.height() (pour connaitre le décalage des positions selon l'axe des x ou des y) et self.x et self.y
        (pour connaitre la position de l'alien)
        Sortie : les aliens se déplacent ou s'arrêtent à certaines conditions (en fonction de self.stop)'''

        #deplacement uniquement si la partie n'est pas en pause (fini ou non commencer)
        if self.stop == 0:
            space.vitesseAlien()
            space.bordAlien()

            #changement de direction (bord droit)
            if self.bord == 1:
                self.dx = -self.dx
                self.bord = 0

            #changement de direction et descente (bord gauche)
            if self.bord == -1:
                self.dx = -self.dx
                self.y += self.alien.height()
                self.bord = 0
            self.x += self.dx

            #Arret si les aliens arrivent au milieu du canvas (gameover)
            if self.y >= space.hauteur/2:
                self.can.coords(self.imgAlien,self.x,self.y)
                self.can.delete(cVaisseau.imgVaisseau)
                cVaisseau.vie = 0
                space.text2.set("Lifes : "+str(cVaisseau.vie))
                for k in range(len(space.listAlien)-1):
                    for i in range(len(space.listAlien[k])):
                        space.listAlien[k][i].present = 0
                        space.listAlien[k][i].stop = 1
                self.present = 0
                self.stop = 1
                if space.alienBonusPresent == 1:
                    space.listAlienBonus[0].stop = 1
                if space.finPartie == 0:
                    space.finPartie = 1
                    messagebox.showinfo('GameOver','Vous avez perdu')

            else:
                self.can.coords(self.imgAlien,self.x,self.y)
                space.after(int(space.tempsDeplacement),self.deplacementAlien)


    def laser(self):
        '''Role : permet de créer un laser tiré par les aliens aléatoirement
        Entrée : self.stop et self.present (même que précédemment, lorsque self.present = 1, il y a déjà un tir présent sur le canvas et l'alien ne pourra pas en retirer un nouveau tant que le tir n'est pas détruit),
        self.yLaser et self.xLaser (qui définissent la position du laser)
        Sortie : Affichage du laser sur le canvas et appel de la fonction de déplacement du laser'''

        if self.stop == 0 and self.present == 0:
            rnd = rd.random()*self.probaLaser
            if rnd <= 1:
                self.yLaser = self.y + self.alien.width()
                self.xLaser = self.x + self.alien.height()/2
                self.tir = self.can.create_rectangle(self.xLaser-2, self.yLaser, self.xLaser+2, self.yLaser + 30,fill='red')
                self.present = 1
                self.deplacementLaser()
                space.after(800,self.laser)
            else:
                space.after(800,self.laser)


    def deplacementLaser(self):
        '''Role : Permet de déplacer le laser tiré par l'alien
        Entrée : self.ind (qui permet de supprimer les petits rectangles des ilots lorsqu'un laser entre en contact), self.xLaser et self.yLaser,
        le canvas, la liste des ilots, self.tir (le laser tiré), self.present, le texte pour modifier les vies
        Sortie : le tir se déplace et réduit le nombre de vie s'il touche le vaisseau, détruit un bout de l'ilot s'il
        le touche, se détruit s'il est en dehors du canvas'''

        self.ind = -1
        #destruction du laser s'il est en dehors du canvas
        if self.yLaser >= space.hauteur:
            self.present = 0
            self.can.delete(self.tir)
            space.after(800,self.laser)

        else:
            self.yLaser += self.dyLaser
            self.can.coords(self.tir, self.xLaser-2, self.yLaser, self.xLaser+2, self.yLaser + 30)
            space.after(20, self.deplacementLaser)

        #presence d'un laser sur le canvas
        if self.present == 1:
            #le tir touche le vaisseau
            if (cVaisseau.xv <= self.can.coords(self.tir)[0] <= cVaisseau.xv + cVaisseau.vaisseau.width()) and (cVaisseau.yv - cVaisseau.vaisseau.height()<= self.can.coords(self.tir)[3] <= cVaisseau.yv):
                self.present = 0
                self.can.delete(self.tir)
                cVaisseau.vie -= 1
                space.text2.set("Lifes : "+str(cVaisseau.vie))

                #il n'y a plus de vie (gameover)
                if cVaisseau.vie == 0:
                    self.can.delete(cVaisseau.imgVaisseau)
                    for k in range(len(space.listAlien)):
                        for i in range(len(space.listAlien[k])):
                            space.listAlien[k][i].stop = 1
                            if space.alienBonusPresent == 1:
                                space.listAlienBonus[0].stop = 1
                    space.finPartie = 1
                    messagebox.showinfo('GameOver','Vous avez perdu')

        #destruction des bouts d'ilots
        for i in range(len(space.listeIlot)):
            if self.present == 1:
                if (space.listeIlot[i])[0] <= self.can.coords(self.tir)[0] <= (space.listeIlot[i])[2] and (space.listeIlot[i])[1] <= self.can.coords(self.tir)[3] <= (space.listeIlot[i])[3]:
                    self.can.delete(space.listeIlot[i])
                    self.can.delete(space.protections[i])
                    self.present = 0
                    self.can.delete(self.tir)
                    self.ind = i

        if self.ind != -1:
            space.listeIlot.pop(self.ind)
            space.protections.pop(self.ind)


class AlienBonus():
    def __init__(self,canvas):
        '''Role : initialisation de l'alien Bonus
        Entrée : le canvas'''

        self.can = canvas
        self.xb  = 500
        self.yb  = 0
        self.dx = 7
        self.alienBonus = PhotoImage(file = 'alienBonus.gif')
        self.imgAlienBonus = self.can.create_image(self.xb, self.yb, anchor ='nw',image = self.alienBonus)
        self.stop = 0
        self.score_alien_bonus = 200

    def deplacementAlienBonus(self):
        '''Role : déplacement de l'alien bonus
        Entrée : self.stop, self.xb (coordonnée de l'alien bonus), et l'image de l'alien bonus
        Sortie : l'alien bonus se déplace et se détruit s'il va trop loin'''

        if self.stop == 0:
            self.xb -= self.dx
            self.can.coords(self.imgAlienBonus,self.xb,self.yb)
            if self.xb + self.alienBonus.width() <= 0:
                self.can.delete(self.imgAlienBonus)
                self.stop = 1
                space.alienBonusPresent = 0
            space.after(100,self.deplacementAlienBonus)



class Vaisseau():
    def __init__(self):
        '''Role : initalisation de la classe Vaisseau'''
        self.can = space.can
        self.xv = space.longueur/2
        self.yv = space.hauteur
        self.vaisseau = PhotoImage(file = 'vaisseau.gif')
        self.imgVaisseau = self.can.create_image(self.xv, self.yv, anchor = 'sw', image = self.vaisseau)
        self.xLaser = self.xv
        self.yLaser = self.yv
        self.dyLaser = 10
        self.present = 0
        self.vie = 3
        self.ind = -1
        self.stop = 0


    def deplacementVaisseauLeft(self,event):
        '''Role : Déplacer le vaisseau à gauche
        Entrée : self.stop, self.vie, self.xv et self.yv (coordonnée du vaisseau) et l'event de deplacement (bouton
        pressé)'''

        if self.stop == 0:
            if self.vie > 0:
                if self.xv > 0:
                    self.xv -= 20
                self.can.coords(self.imgVaisseau, self.xv, self.yv)

    def deplacementVaisseauRight(self,event):
        '''Role : Déplacer le vaisseau à droite
        Entrée : self.stop, self.vie, self.xv et self.yv (coordonnée du vaisseau) et l'event de déplacement (bouton
        pressé)'''

        if self.stop == 0:
            if self.vie > 0:
                if self.xv + self.vaisseau.width() < space.longueur:
                    self.xv += 20
                self.can.coords(self.imgVaisseau, self.xv, self.yv)

    def laser(self,event):
        '''Role : creation d'un laser lorsque l'utilisateur appuie sur espace
        Entrée : l'event de l'appui sur la touche, self.stop et self.present, self.xv et self.yv (pour savoir où se
        trouve le vaisseau au moment du tir, le canvas
        Sortie ; création du tir du vaisseau et appel de la fonction du déplacement de ce tir'''

        if self.present == 0 and self.vie > 0 and self.stop == 0:
            self.xLaser = self.xv
            self.yLaser = self.yv
            self.tir = self.can.create_rectangle(self.xLaser+self.vaisseau.width()/2-2, self.yLaser-self.vaisseau.height()-30, self.xLaser+self.vaisseau.width()/2+2, self.yLaser-self.vaisseau.height(),fill='blue')
            self.present = 1
            self.deplacementLaser()


    def deplacementLaser(self):
        '''Role : Permet de déplacer le laser tiré par le vaisseau et finir la partie si tous les aliens sont détruits
        Entrée : self.ind (qui permet de supprimer les petits rectangles des ilots lorsqu'un laser entre en contact), self.xLaser et self.yLaser,
        le canvas, la liste des ilots, self.tir (le laser tirer), self.present, self.score
        Sortie : le tir se déplace et le score augmente en fonction de l'alien touché, détruit un bout de l'ilot s'il
        le touche, se détruit s'il est en dehors du canvas'''


        self.ind = -1
        #destruction du laser s'il arrive trop haut
        if self.yLaser <= 0:
            self.can.delete(self.tir)
            self.present = 0

        #deplacement du tir vers le haut
        else:
            self.yLaser -= self.dyLaser
            self.can.coords(self.tir, self.xLaser+self.vaisseau.width()/2-2, self.yLaser-self.vaisseau.height()-30, self.xLaser+self.vaisseau.width()/2+2, self.yLaser-self.vaisseau.height())
            space.after(20, self.deplacementLaser)


        #destruction des bouts d'ilots au contact du laser
        for i in range(len(space.listeIlot)):
            if self.present == 1:
                if (space.listeIlot[i])[0] <= self.can.coords(self.tir)[0] <= (space.listeIlot[i])[2] and (space.listeIlot[i])[1] <= self.can.coords(self.tir)[1] <= (space.listeIlot[i])[3]:
                    self.can.delete(space.listeIlot[i])
                    self.can.delete(space.protections[i])
                    self.can.delete(self.tir)
                    self.present = 0
                    self.ind = i

        if self.ind != -1:
            space.listeIlot.pop(self.ind)
            space.protections.pop(self.ind)

        #test du contact entre le tir et un alien avec victoire s'il sont tous détruits
        for k in range(len(space.listAlien)):
            for i in range(len(space.listAlien[k])):
                if self.present == 1:
                    if (space.listAlien[k][i].x <= self.can.coords(self.tir)[0] <= space.listAlien[k][i].x + space.listAlien[k][i].alien.width()) and (space.listAlien[k][i].y <= self.can.coords(self.tir)[1] <= space.listAlien[k][i].y + space.listAlien[k][i].alien.height()):
                        self.can.delete(self.tir)
                        self.present = 0
                        self.can.delete(space.listAlien[k][i].imgAlien)
                        space.listAlien[k][i].stop = 1
                        space.score += space.listAlien[k][i].score_alien
                        space.listAlien[k].pop(i)
                        space.text1.set("Score : "+str(space.score))
                        if space.listAlien[0] == [] and space.listAlien[1] == [] and space.listAlien[2] == []:
                            cVaisseau.stop = 1
                            if space.alienBonusPresent == 1:
                                space.listAlienBonus[0].stop = 1
                            space.finPartie = 1
                            messagebox.showinfo('Gagné','Vous avez gagné, félicitations')

        #test du contact avec l'alien bonus
        if space.alienBonusPresent == 1:
            if self.present == 1:
                if (space.listAlienBonus[0].xb <= self.can.coords(self.tir)[0] <= space.listAlienBonus[0].xb + space.listAlienBonus[0].alienBonus.width()) and (space.listAlienBonus[0].yb <= self.can.coords(self.tir)[1] <= space.listAlienBonus[0].yb + space.listAlienBonus[0].alienBonus.height()):
                    self.can.delete(space.listAlienBonus[0].imgAlienBonus)
                    self.can.delete(self.tir)
                    self.present = 0
                    space.listAlienBonus[0].stop = 1
                    space.alienBonusPresent = 0
                    space.score += space.listAlienBonus[0].score_alien_bonus
                    space.text1.set("Score : "+str(space.score))


space = SpaceInvader()
cVaisseau = Vaisseau()


space.mainloop()
