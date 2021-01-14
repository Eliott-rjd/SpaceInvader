#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programme principale du SpaceInvader
Eliott RAJAUD et Axel GUILLET
18/12/20
TODO : Faire le menu
    Mettre role, entree sortie de toutes les fcts
    faire fichier a part avec les classes et autres avec la creation TkInter
    Modifier le progr a fct
    Erreur d'index lors du tir du laser du vaisseau à corriger (erreur sans conséquence sur le jeu du moins)
"""

from tkinter import Tk,Label,Canvas,Button,StringVar,PhotoImage
import random as rd

class space_invader(Tk):
    def __init__(self):
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

        #self.text1 = StringVar()
        self.labelScore = Label(self, text = 'Score = self.text1') #textvariable pour score qui change en fonction du stringvar
        self.text2 = StringVar()
        self.labelVie = Label(self, textvariable = self.text2)

        self.buttonQuit = Button(self , text = 'Quitter' , fg = 'red' , command = self.destroy)
        #self.buttonReplay = Button(self, text = 'Rejouer' , command = self.rejouer )

        self.newGame = Button(self, text = 'Démarrer une partie', command = self.init_partie)

        self.labelScore.grid(row = 1, column = 1, sticky = 'w')
        self.labelVie.grid(row = 1, column = 2, sticky = 'e')
        self.newGame.grid(row = 2, column = 3, rowspan = 1, sticky = 'e')
        #self.buttonReplay.grid(row = 2, column = 4, rowspan = 1, sticky = "e")
        self.buttonQuit.grid(row = 3, column = 3, rowspan = 1, sticky = "e")
        self.can.grid(row = 2 , column = 1, rowspan = 2, columnspan = 2,  sticky = "w")
        self.L_Alien = []
        self.L_Vaisseau = []
        self.démarrer = 0
        self.Liste_classe_init()
        self.ilots()

    def ilots(self):
        for i in range(5):
            for j in range(3):
                a = self.can.create_rectangle(50+i*16, 380+j*16, 50+i*16+16, 380+j*16+16, fill= "white")
                b = self.can.create_rectangle(210+i*16, 380+j*16, 210+i*16+16, 380+j*16+16, fill= "white")
                c = self.can.create_rectangle(370+i*16, 380+j*16, 370+i*16+16, 380+j*16+16, fill= "white")
                self.protections.extend([a,b,c])
                L_a = [50+i*16, 380+j*16, 50+i*16+16, 380+j*16+16]
                L_b = [210+i*16, 380+j*16, 210+i*16+16, 380+j*16+16]
                L_c = [370+i*16, 380+j*16, 370+i*16+16, 380+j*16+16]
                self.L.extend([L_a,L_b,L_c])

    def Liste_classe_init(self):
        for i in range(0,6):
            C_Alien = Alien(self.can,i*60,0)
            self.L_Alien.append(C_Alien)

    def init_partie(self):
        if self.démarrer == 0:
            for i in range(0,6):
                self.L_Alien[i].deplacementAlien()
                self.L_Alien[i].laser()
            self.bind("<Left>",C_Vaisseau.déplacementVaisseau_left)
            self.bind("<Right>",C_Vaisseau.déplacementVaisseau_right)
            self.bind("<space>",C_Vaisseau.laser)
            self.text2.set("Lifes : "+str(C_Vaisseau.vie))
            self.démarrer = 1

class Alien():
    def __init__(self,canvas,X,Y):
        self.can = canvas
        self.X  = X
        self.Y  = Y
        self.dx = 10
        self.stop = 0
        self.present = 0
        self.toucher_droit = 0
        self.toucher_gauche = 0
        self.attend = 0
        self.ind = 0
        self.alien = PhotoImage(file = 'alien.gif')
        self.imgAlien = self.can.create_image(self.X, self.Y, anchor ='nw',image = self.alien)
        self.Xl = self.X + self.alien.height()/2
        self.Yl = self.Y + self.alien.width()
        self.dy = 10
        self.a = -1

    def deplacementAlien(self):
        if self.stop == 0:
            if space.L_Alien[len(space.L_Alien)-1].X+space.L_Alien[len(space.L_Alien)-1].dx+space.L_Alien[len(space.L_Alien)-1].alien.width() > space.longueur:
                for i in range(self.ind,len(space.L_Alien)):
                    space.L_Alien[i].toucher_droit = 1
                if self.ind != len(space.L_Alien)-1:
                    for i in range(len(space.L_Alien)):
                        space.L_Alien[i].ind += 1
                else:
                    for i in range(len(space.L_Alien)):
                        space.L_Alien[i].ind = 0

            if self.X + self.dx< 0:
                for i in range(len(space.L_Alien)):
                    space.L_Alien[i].toucher_gauche = 1

            if self.toucher_droit == 1:
                self.dx = -self.dx
                self.toucher_droit = 0

            if self.toucher_gauche == 1:
                self.dx = -self.dx
                self.Y += self.alien.height()
                self.toucher_gauche = 0
            self.X += self.dx

            if self.Y >= space.hauteur/2:
                self.can.coords(self.imgAlien,self.X,self.Y)
                self.can.delete(C_Vaisseau.imgVaisseau)
                C_Vaisseau.vie = 0
                space.text2.set("Lifes : "+str(C_Vaisseau.vie))
                #for i in range(len(space.L_Alien)):
                    #space.L_Alien[i].stop = 1


            else:
                self.can.coords(self.imgAlien,self.X,self.Y)
                space.after(200,self.deplacementAlien)

    def laser(self):
        if self.stop == 0 and self.present == 0:
            rnd = rd.random()*10
            if rnd <= 1:
                self.Yl = self.Y + self.alien.width()
                self.Xl = self.X + self.alien.height()/2
                self.tir = self.can.create_rectangle(self.Xl-2, self.Yl, self.Xl+2, self.Yl + 30,fill='red')
                self.present = 1
                self.deplacementLaser()
                space.after(800,self.laser)
            else:
                space.after(800,self.laser)

    def deplacementLaser(self):
        self.a = -1
        if self.Yl >= space.hauteur:
            self.present = 0
            self.can.delete(self.tir)
            space.after(800,self.laser)

        else:
            self.Yl += self.dy
            self.can.coords(self.tir, self.Xl-2, self.Yl, self.Xl+2, self.Yl + 30)
            space.after(20, self.deplacementLaser)

        if self.present == 1:
            if (C_Vaisseau.Xv <= self.can.coords(self.tir)[0] <= C_Vaisseau.Xv + C_Vaisseau.vaisseau.width()) and (C_Vaisseau.Yv - C_Vaisseau.vaisseau.height()<= self.can.coords(self.tir)[3] <= C_Vaisseau.Yv):
                self.present = 0
                self.can.delete(self.tir)
                C_Vaisseau.vie -= 1
                space.text2.set("Lifes : "+str(C_Vaisseau.vie))
                if C_Vaisseau.vie == 0:
                    self.can.delete(C_Vaisseau.imgVaisseau)
                    for i in range(len(space.L_Alien)):
                        space.L_Alien[i].stop = 1

        for i in range(len(space.L)):
            if self.present == 1:
                if (space.L[i])[0] <= self.can.coords(self.tir)[0] <= (space.L[i])[2] and (space.L[i])[1] <= self.can.coords(self.tir)[3] <= (space.L[i])[3]:
                    self.can.delete(space.L[i])
                    self.can.delete(space.protections[i])
                    self.present = 0
                    self.can.delete(self.tir)
                    self.a = i

        if self.a != -1:
            space.L.pop(self.a)
            space.protections.pop(self.a)


class Vaisseau():
    def __init__(self):
        self.can = space.can
        self.Xv = space.longueur/2
        self.Yv = space.hauteur
        self.vaisseau = PhotoImage(file = 'vaisseau.gif')
        self.imgVaisseau = self.can.create_image(self.Xv, self.Yv, anchor = 'sw', image = self.vaisseau)
        self.Xl = self.Xv
        self.Yl = self.Yv
        self.dy = 10
        self.present = 0
        self.vie = 3
        self.a = -1

    def déplacementVaisseau_left(self,event):
        if self.vie > 0:
            if self.Xv > 0:
                self.Xv -= 20
            self.can.coords(self.imgVaisseau, self.Xv, self.Yv)

    def déplacementVaisseau_right(self,event):
        if self.vie > 0:
            if self.Xv + self.vaisseau.width() < space.longueur:
                self.Xv += 20
            self.can.coords(self.imgVaisseau, self.Xv, self.Yv)

    def laser(self,event):
        if self.present == 0 and self.vie > 0:
            self.Xl = self.Xv
            self.Yl = self.Yv
            self.tir = self.can.create_rectangle(self.Xl+self.vaisseau.width()/2-2, self.Yl-self.vaisseau.height()-30, self.Xl+self.vaisseau.width()/2+2, self.Yl-self.vaisseau.height(),fill='blue')
            self.present = 1
            self.deplacementLaser()


    def deplacementLaser(self):
        self.a = -1
        if self.Yl <= 0:
            self.can.delete(self.tir)
            self.present = 0

        else:
            self.Yl -= self.dy
            self.can.coords(self.tir, self.Xl+self.vaisseau.width()/2-2, self.Yl-self.vaisseau.height()-30, self.Xl+self.vaisseau.width()/2+2, self.Yl-self.vaisseau.height())
            space.after(20, self.deplacementLaser)

        for i in range(len(space.L)):
            if self.present == 1:
                if (space.L[i])[0] <= self.can.coords(self.tir)[0] <= (space.L[i])[2] and (space.L[i])[1] <= self.can.coords(self.tir)[1] <= (space.L[i])[3]:
                    self.can.delete(space.L[i])
                    self.can.delete(space.protections[i])
                    self.can.delete(self.tir)
                    self.present = 0
                    self.a = i

        if self.a != -1:
            space.L.pop(self.a)
            space.protections.pop(self.a)

        for i in range(len(space.L_Alien)):
            if self.present == 1:
                if (space.L_Alien[i].X <= self.can.coords(self.tir)[0] <= space.L_Alien[i].X + space.L_Alien[i].alien.width()) and (space.L_Alien[i].Y <= self.can.coords(self.tir)[1] <= space.L_Alien[i].Y + space.L_Alien[i].alien.height()):
                    self.can.delete(self.tir)
                    self.can.delete(space.L_Alien[i].imgAlien)
                    space.L_Alien[i].stop = 1
                    space.L_Alien.pop(i)
                    self.present = 0


#def rejouer():

space = space_invader()
C_Vaisseau = Vaisseau()

space.mainloop()

#rejouer()