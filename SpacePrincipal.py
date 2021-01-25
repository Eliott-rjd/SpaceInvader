#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
https://github.com/Eliott-rjd/SpaceInvader.git
Programme principale du SpaceInvader
Eliott RAJAUD et Axel GUILLET
18/12/20
TODO :
    Mettre le deplacement gauche et droite du vaisseau en une seul fct
    Mieux séparer le fichier : faire fichier a part avec les classes et autres avec la creation TkInter

    Regle le bug de deplacement de toute les lignes : lorsqu'il reste de aliens sur la colonne la plus a droite/gauche
    parfois ne prend pas en compte la colonne pour le contact avec le bord du canvas -- souvent lorsque l'alien est détruit
    juste avant la colision

    Ajouter fonctionnalité bonus : sauvegarde du score, plusieurs niveaux
"""

from tkinter import Tk,Label,Canvas,Button,StringVar,PhotoImage,messagebox
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
        self.L= []
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

        self.labelScore.grid(row = 1, column = 1, sticky = 'w')
        self.labelVie.grid(row = 1, column = 2, sticky = 'e')
        self.newGame.grid(row = 2, column = 3, rowspan = 1, sticky = 'e')
        self.buttonReplay.grid(row = 2, column = 4, rowspan = 1, sticky = "e")
        self.buttonQuit.grid(row = 3, column = 3, rowspan = 1, sticky = "e")
        self.can.grid(row = 2 , column = 1, rowspan = 2, columnspan = 2,  sticky = "w")

        self.listAlien = []
        self.listAlienBonus = []
        self.demarrer = 0
        self.score = 0
        self.finPartie = 0
        self.alienBonusPresent = 0
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
        Sortie : Affichage de tous les aliens'''
        self.listAlien = []
        for j in range(0,3):
            for i in range(0,6):
                cAlien = Alien(self.can,i*60,j*60)
                self.listAlien.append(cAlien)

    def initPartie(self):
        '''Role : demarrer la partie à l'appui du bouton. Met en place les commandes, le score et les vies
        Entrée : self.demarrer de la classe, qui passe à 1 après l'initialisation de la partie pour éviter les bugs lier au spam du bouton démarrer
        Sortie : lancement du déplacement des aliens'''
        if self.demarrer == 0:
            for i in range(0,len(self.listAlien)):
                self.listAlien[i].deplacementAlien()
                self.listAlien[i].laser()
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
        Sortie : remise à zero et replacement du vaisseau ainsi que des aliens à leur position initiale, reformation des ilots de protection
        et suppression des tirs lancés au moment du clique sur le bouton.'''

        #Destruction des items
        if cVaisseau.present == 1:
            self.can.delete(cVaisseau.tir)
            cVaisseau.present = 0
        for i in range(len(self.listAlien)):
            self.can.delete(self.listAlien[i].imgAlien)
            self.listAlien[i].stop = 1
            if self.listAlien[i].present == 1:
                self.can.delete(self.listAlien[i].tir)
                self.listAlien[i].present = 0
        for j in range(len(space.listeIlot)):
            self.can.delete(space.listeIlot[j])
            self.can.delete(space.protections[j])

        #reinitialisation des items
        self.ilots()
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
            #creation de l'alien bonus uniquement si les sont descendus au moins une fois
            for i in range (len(self.listAlien)):
                if self.listAlien[i].y == 0:
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
        self.toucherDroit = 0
        self.toucherGauche = 0
        self.alien = PhotoImage(file = 'alien.gif')

        self.imgAlien = self.can.create_image(self.x, self.y, anchor ='nw',image = self.alien)
        self.xl = self.x + self.alien.height()/2
        self.yl = self.y + self.alien.width()
        self.dy = 10
        self.a = -1
        self.verif = 0
        self.score_alien = 100


    def deplacementAlien(self):
        '''Role : permet de déplacer les aliens
        Entrée : la canvas, self.stop (pour savoir si les aliens sont arrêtés, donc s'ils sont détruits ou si la partie est finit), self.toucherDroite et self.toucherGauche (pour savoir
        s'il y a eu contact avec un bord), listAlien, self.dx et self.dy (pour connaitre le décalage) et self.x et self.y
        (pour connaitre la position de l'alien), self.verif (pour être sûre que tous les aliens descendent et tournent à gauche
        en même temps)
        Sortie : les aliens se déplacent ou s'arrêtent à certaines conditions'''

        #deplacement uniquement si la partie n'est pas en pause (fini ou non commencer)
        if self.stop == 0:
            self.toucherDroit = 0

            #contact avec le bord droit
            if (space.listAlien)[len(space.listAlien)-1].x+(space.listAlien)[len(space.listAlien)-1].dx+(space.listAlien)[len(space.listAlien)-1].alien.width() > space.longueur:
                for i in range(len(space.listAlien)):
                    space.listAlien[i].toucherDroit = 1

            #contact avec le bord gauche
            if self.verif % 2 == 0:
                if space.listAlien[0].x+space.listAlien[0].dx< 0:
                    for i in range(len(space.listAlien)):
                        space.listAlien[i].toucherGauche = 1
                        space.listAlien[i].verif = 1

            #changement de direction
            if self.toucherDroit == 1:
                self.dx = -self.dx
                self.toucherDroit = 0

            #changement de direction et descente
            if self.toucherGauche == 1:
                self.dx = -self.dx
                self.y += self.alien.height()
                self.toucherGauche = 0
            self.x += self.dx

            #Arret si les aliens arrivent au milieu du canvas (gameover)
            if self.y >= space.hauteur/2:
                self.can.coords(self.imgAlien,self.x,self.y)
                self.can.delete(cVaisseau.imgVaisseau)
                cVaisseau.vie = 0
                space.text2.set("Lifes : "+str(cVaisseau.vie))
                for i in range(len(space.listAlien)):
                    space.listAlien[i].present = 0
                    space.listAlien[i].stop = 1
                    if space.alienBonusPresent == 1:
                        space.listAlienBonus[0].stop = 1
                space.finPartie = 1
                messagebox.showinfo('GameOver','Vous avez perdu')

            else:
                self.can.coords(self.imgAlien,self.x,self.y)
                space.after(200,self.deplacementAlien)
                self.verif += 1


    def laser(self):
        '''Role : permet de créer un laser tiré par les aliens aléatoirement
        Entrée : self.stop et self.present (même que précédemment, lorsque self.present = 1, il y a déjà un tir présent sur le canvas et l'alien ne pourra pas en retirer un nouveau tant que le tir n'est pas détruit),
        self.yl et self.xl (qui définissent la position du laser)
        Sortie : Affichage du laser sur le canvas et appel de la fonction de déplacement du laser'''

        if self.stop == 0 and self.present == 0:
            rnd = rd.random()*20
            if rnd <= 1:
                self.yl = self.y + self.alien.width()
                self.xl = self.x + self.alien.height()/2
                self.tir = self.can.create_rectangle(self.xl-2, self.yl, self.xl+2, self.yl + 30,fill='red')
                self.present = 1
                self.deplacementLaser()
                space.after(800,self.laser)
            else:
                space.after(800,self.laser)


    def deplacementLaser(self):
        '''Role : Permet de déplace le laser tiré par l'alien
        Entrée : self.a (qui permet de supprimer les petits rectangles des ilots lorsqu'un laser entre en contact), self.xl et self.yl,
        le canvas, la liste des ilots, self.tir (le laser tiré), self.present, le texte pour modifier les vie
        Sortie : le tir se déplace et réduit le nombre de vie s'il touche le vaisseau, détruit un bout de l'ilot s'il
        le touche, se détruit s'il est en dehors du canvas'''

        self.a = -1
        #destruction du laser s'il est en dehors du canvas
        if self.yl >= space.hauteur:
            self.present = 0
            self.can.delete(self.tir)
            space.after(800,self.laser)

        else:
            self.yl += self.dy
            self.can.coords(self.tir, self.xl-2, self.yl, self.xl+2, self.yl + 30)
            space.after(20, self.deplacementLaser)

        #prescence d'un laser sur la canvas
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
                    for i in range(len(space.listAlien)):
                        space.listAlien[i].stop = 1
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
                    self.a = i

        if self.a != -1:
            space.listeIlot.pop(self.a)
            space.protections.pop(self.a)


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
        self.xl = self.xv
        self.yl = self.yv
        self.dy = 10
        self.present = 0
        self.vie = 3
        self.a = -1
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
            self.xl = self.xv
            self.yl = self.yv
            self.tir = self.can.create_rectangle(self.xl+self.vaisseau.width()/2-2, self.yl-self.vaisseau.height()-30, self.xl+self.vaisseau.width()/2+2, self.yl-self.vaisseau.height(),fill='blue')
            self.present = 1
            self.deplacementLaser()


    def deplacementLaser(self):
        '''Role : Permet de déplacer le laser tiré par le vaisseau et finir la partie si tous les aliens sont détruits
        Entrée : self.a (qui permet de supprimer les petits rectangles des ilots lorsqu'un laser entre en contact), self.xl et self.yl,
        le canvas, la liste des ilots, self.tir (le laser tirer), self.present, self.score
        Sortie : le tir se déplace et le score augmente en fonction de l'alien touché, détruit un bout de l'ilot s'il
        le touche, se détruit s'il est en dehors du canvas'''


        self.a = -1
        #destruction du laser s'il arrive trop haut
        if self.yl <= 0:
            self.can.delete(self.tir)
            self.present = 0

        #deplacement du tir vers le haut
        else:
            self.yl -= self.dy
            self.can.coords(self.tir, self.xl+self.vaisseau.width()/2-2, self.yl-self.vaisseau.height()-30, self.xl+self.vaisseau.width()/2+2, self.yl-self.vaisseau.height())
            space.after(20, self.deplacementLaser)


        #destruction des bouts d'ilots au contact du laser
        for i in range(len(space.listeIlot)):
            if self.present == 1:
                if (space.listeIlot[i])[0] <= self.can.coords(self.tir)[0] <= (space.listeIlot[i])[2] and (space.listeIlot[i])[1] <= self.can.coords(self.tir)[1] <= (space.listeIlot[i])[3]:
                    self.can.delete(space.listeIlot[i])
                    self.can.delete(space.protections[i])
                    self.can.delete(self.tir)
                    self.present = 0
                    self.a = i

        if self.a != -1:
            space.listeIlot.pop(self.a)
            space.protections.pop(self.a)

        #test du contact entre le tir et un alien avec victoire s'il sont tous détruits
        for i in range(len(space.listAlien)):
            if self.present == 1:
                if (space.listAlien[i].x <= self.can.coords(self.tir)[0] <= space.listAlien[i].x + space.listAlien[i].alien.width()) and (space.listAlien[i].y <= self.can.coords(self.tir)[1] <= space.listAlien[i].y + space.listAlien[i].alien.height()):
                    self.can.delete(self.tir)
                    self.present = 0
                    self.can.delete(space.listAlien[i].imgAlien)
                    space.listAlien[i].stop = 1
                    space.score += space.listAlien[i].score_alien
                    space.listAlien.pop(i)
                    space.text1.set("Score : "+str(space.score))
                    if space.listAlien == []:
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
