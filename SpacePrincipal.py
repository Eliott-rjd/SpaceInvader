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
    les ilots se régénèrent mal avec la fonction rejouer
"""

from tkinter import Tk,Label,Canvas,Button,StringVar,PhotoImage,messagebox
import random as rd
#from ClassVaisseau import Vaisseau
#from ClassAlien import Alien

class SpaceInvader(Tk):
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

        self.text1 = StringVar()
        self.labelScore = Label(self, textvariable = self.text1) #textvariable pour score qui change en fonction du stringvar
        self.text2 = StringVar()
        self.labelVie = Label(self, textvariable = self.text2)

        self.buttonQuit = Button(self , text = 'Quitter' , fg = 'red' , command = self.destroy)
        self.buttonReplay = Button(self, text = 'Rejouer' , command = self.rejouer)

        self.newGame = Button(self, text = 'Démarrer une partie', command = self.init_partie)

        self.labelScore.grid(row = 1, column = 1, sticky = 'w')
        self.labelVie.grid(row = 1, column = 2, sticky = 'e')
        self.newGame.grid(row = 2, column = 3, rowspan = 1, sticky = 'e')
        self.buttonReplay.grid(row = 2, column = 4, rowspan = 1, sticky = "e")
        self.buttonQuit.grid(row = 3, column = 3, rowspan = 1, sticky = "e")
        self.can.grid(row = 2 , column = 1, rowspan = 2, columnspan = 2,  sticky = "w")
        self.listAlien = []
        self.démarrer = 0
        self.score = 0
        self.Liste_classe_init()
        self.ilots()

    def ilots(self):
        self.protections = []
        self.L= []
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
        self.listAlien = []
        for j in range(0,3):
            L = []
            for i in range(0,6):
                C_Alien = Alien(self.can,i*60,j*60)
                L.append(C_Alien)
                self.listAlien.append(L)

    def init_partie(self):
        if self.démarrer == 0:
            for k in range(0,len(self.listAlien)):
                for i in range(0,len(self.listAlien[k])):
                    self.listAlien[k][i].deplacementAlien()
                    self.listAlien[k][i].laser()
            self.bind("<Left>",C_Vaisseau.déplacementVaisseau_left)
            self.bind("<Right>",C_Vaisseau.déplacementVaisseau_right)
            self.bind("<space>",C_Vaisseau.laser)
            self.text2.set("Lifes : "+str(C_Vaisseau.vie))
            self.text1.set("Score : "+str(self.score))
            self.démarrer = 1
            C_Vaisseau.stop = 0

    def rejouer(self):
        for k in range(len(self.listAlien)):
            for i in range(len(self.listAlien[k])):
                self.can.delete(self.listAlien[k][i].imgAlien)
                self.listAlien[k][i].stop = 1
        self.ilots()
        self.Liste_classe_init()
        self.démarrer = 0
        self.can.delete(C_Vaisseau.imgVaisseau)
        C_Vaisseau.imgVaisseau = self.can.create_image(self.longueur/2, self.hauteur, anchor = 'sw', image = C_Vaisseau.vaisseau)
        C_Vaisseau.Xv = self.longueur/2
        C_Vaisseau.stop = 1
        C_Vaisseau.vie = 3
        self.text2.set("Lifes : "+str(C_Vaisseau.vie))
        self.score = 0
        self.text1.set("Score : "+str(self.score))



class Alien():
    def __init__(self,canvas,X,Y):
        self.can = canvas
        self.X  = X
        self.Y  = Y
        self.dx = 7
        self.stop = 0
        self.present = 0
        self.toucher_droit = 0
        self.toucher_gauche = 0
        self.attend = 0
        #self.ind = 0
        self.alien = PhotoImage(file = 'alien.gif')
        self.imgAlien = self.can.create_image(self.X, self.Y, anchor ='nw',image = self.alien)
        self.Xl = self.X + self.alien.height()/2
        self.Yl = self.Y + self.alien.width()
        self.dy = 10
        self.a = -1
        self.verif = 0

    def deplacementAlien(self):

        if self.stop == 0:
            self.toucher_droit = 0
            for k in range(0,len(space.listAlien)):
                if (space.listAlien[k])[len(space.listAlien[k])-1].X+(space.listAlien[k])[len(space.listAlien[k])-1].dx+(space.listAlien[k])[len(space.listAlien[k])-1].alien.width() > space.longueur:
                    for i in range(len(space.listAlien[k])):
                        space.listAlien[k][i].toucher_droit = 1
                    #if self.ind != len(space.listAlien[k])-1:
                        #for i in range(len(space.listAlien[k])):
                            #space.listAlien[k][i].ind += 1
                    #else:
                        #for i in range(len(space.listAlien[k])):
                            #space.listAlien[k][i].ind = 0

            if self.verif % 2 == 0:
                for k in range(len(space.listAlien)):
                    if space.listAlien[k][0].X+space.listAlien[k][0].dx< 0:
                        for i in range(len(space.listAlien[k])):
                            space.listAlien[k][i].toucher_gauche = 1
                            space.listAlien[k][i].verif = 1

            if self.toucher_droit == 1:
                self.dx = -self.dx
                self.toucher_droit = 0

            if self.toucher_gauche == 1:
                print('ddd')
                self.dx = -self.dx
                self.Y += self.alien.height()
                self.toucher_gauche = 0
            self.X += self.dx

            if self.Y >= space.hauteur/2:
                self.can.coords(self.imgAlien,self.X,self.Y)
                self.can.delete(C_Vaisseau.imgVaisseau)
                C_Vaisseau.vie = 0
                space.text2.set("Lifes : "+str(C_Vaisseau.vie))
                for k in range(len(space.listAlien)):
                    for i in range(len(space.listAlien[k])):
                        space.listAlien[k][i].present = 1

            else:
                self.can.coords(self.imgAlien,self.X,self.Y)
                space.after(1000,self.deplacementAlien)
                self.chgtVerif()

    def chgtVerif(self):
        self.verif += 1

    def laser(self):
        if self.stop == 0 and self.present == 0:
            rnd = rd.random()*50
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
                    for k in range(len(space.listAlien)):
                        for i in range(len(space.listAlien[k])):
                            space.listAlien[k][i].stop = 1

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
        self.stop = 0

    def déplacementVaisseau_left(self,event):
        if self.stop == 0:
            if self.vie > 0:
                if self.Xv > 0:
                    self.Xv -= 20
                self.can.coords(self.imgVaisseau, self.Xv, self.Yv)

    def déplacementVaisseau_right(self,event):
        if self.stop == 0:
            if self.vie > 0:
                if self.Xv + self.vaisseau.width() < space.longueur:
                    self.Xv += 20
                self.can.coords(self.imgVaisseau, self.Xv, self.Yv)

    def laser(self,event):
        if self.present == 0 and self.vie > 0 and self.stop == 0:
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

        for k in range(len(space.listAlien)):
            for i in range(len(space.listAlien[k])):
                if self.present == 1:
                    if (space.listAlien[k][i].X <= self.can.coords(self.tir)[0] <= space.listAlien[k][i].X + space.listAlien[k][i].alien.width()) and (space.listAlien[k][i].Y <= self.can.coords(self.tir)[1] <= space.listAlien[k][i].Y + space.listAlien[k][i].alien.height()):
                        self.can.delete(self.tir)
                        self.can.delete(space.listAlien[k][i].imgAlien)
                        space.listAlien[k][i].stop = 1
                        space.listAlien[k].pop(i)
                        self.present = 0
                        space.score += 100
                        space.text1.set("Score : "+str(space.score))


#def rejouer():

space = SpaceInvader()
C_Vaisseau = Vaisseau()

space.mainloop()
