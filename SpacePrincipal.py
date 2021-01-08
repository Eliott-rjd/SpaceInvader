#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programme principale du SpaceInvader
Eliott RAJAUD et Axel GUILLET
18/12/20
TODO : Faire le menu
    Mettre role, entree sortie de toutes les fcts

"""

from tkinter import Tk,Label,Canvas,Button,StringVar,PhotoImage

class space_invader(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry('900x700+200+50')
        self.title('Space Invaders')

        self.hauteur = 500
        self.longueur = 500
        self.can = Canvas(self,width = self.hauteur,height = self.longueur)


        self.photo = PhotoImage(file = 'espace.gif')

        self.item = self.can.create_image(0, 0, anchor = 'nw', image = self.photo)

        #self.text1 = StringVar()
        self.labelScore = Label(self, text = 'Score = self.text1') #textvariable pour score qui change en fonction du stringvar
        self.labelVie = Label(self, text = 'Vies = 3')

        self.buttonQuit = Button(self , text = 'Quitter' , fg = 'red' , command = self.destroy)

        self.newGame = Button(self, text = 'Démarrer une partie', command = self.init_partie)

        self.labelScore.grid(row = 1, column = 1, sticky = 'w')
        self.labelVie.grid(row = 1, column = 2, sticky = 'e')
        self.newGame.grid(row = 2, column = 3, rowspan = 1, sticky = 'e')
        self.buttonQuit.grid(row = 3, column = 3, rowspan = 1, sticky = "e")
        self.can.grid(row = 2 , column = 1, rowspan = 2, columnspan = 2,  sticky = "w")

    def init_partie(self):
        
        C_Alien.deplacementAlien()
        self.bind("<Left>",C_Vaisseau.déplacementVaisseau_left)
        self.bind("<Right>",C_Vaisseau.déplacementVaisseau_right)
        self.bind("<space>",C_Vaisseau.laser)


class Alien():
    def __init__(self):
        self.can = space.can
        self.X  = 0
        self.Y  = 0
        self.dx = 10
        self.alien = PhotoImage(file = 'alien.gif')
        self.imgAlien = self.can.create_image(self.X, self.Y, anchor ='nw',image = self.alien)

    def deplacementAlien(self):
        if self.X+self.dx+self.alien.width() > space.longueur:
            self.dx = -self.dx
        self.X += self.dx

        if self.X + self.dx< 0:
            self.dx = -self.dx
        self.X += self.dx

        self.can.coords(self.imgAlien,self.X,self.Y)
        space.after(500,self.deplacementAlien)



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

    def déplacementVaisseau_left(self,event):
        if self.Xv > 0:
            self.Xv -= 20

        self.can.coords(self.imgVaisseau, self.Xv, self.Yv)

    def déplacementVaisseau_right(self,event):
        if self.Xv + self.vaisseau.width() < space.longueur:
            self.Xv += 20

        self.can.coords(self.imgVaisseau, self.Xv, self.Yv)

    def laser(self,event):
        if self.present == 0:
            self.Xl = self.Xv
            self.tir = self.can.create_rectangle(self.Xl,self.Yl-self.vaisseau.height()-10,self.Xl+1,self.Yl-self.vaisseau.height(),fill='blue')
            self.deplacementLaser()


    def deplacementLaser(self):
        if self.Yl == 0:
            self.can.delete(self.tir)
            self.present = 0
            self.Yl = self.Yv
            
        elif (C_Alien.X <= self.can.coords(self.tir)[0] <= C_Alien.X + C_Alien.alien.width()) and (C_Alien.Y <= self.can.coords(self.tir)[1] <= C_Alien.alien.height()):
            self.can.delete(self.tir)
            self.can.delete(C_Alien.imgAlien)
            self.present = 0
            self.Yl = self.Yv      
            
        else:
            self.present = 1
            self.Yl -= self.dy

            self.can.coords(self.tir, self.Xl,self.Yl-self.vaisseau.height()-30,self.Xl+10,self.Yl-self.vaisseau.height())
            space.after(20, self.deplacementLaser)

space = space_invader()
C_Alien = Alien()
C_Vaisseau = Vaisseau()

space.mainloop()