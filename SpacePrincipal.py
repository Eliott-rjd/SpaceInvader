#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programme principale du SpaceInvader
Eliott RAJAUD et Axel GUILLET
18/12/20
TODO : Faire le menu
    Faire classe alien
    Faire classe vaisseau

"""

from tkinter import Tk,Label,Canvas,Button,StringVar,PhotoImage

class space_invader(Tk):
    def __init__(self):
        global largeur,X,Y,Xv,Yv
        Tk.__init__(self)
        self.geometry('900x700+200+50')
        self.title('Space Invaders')

        self.hauteur = 500
        self.longueur = 500
        self.can = Canvas(self,width = self.hauteur,height = self.longueur)
        self.X = 0
        self.Y = 0
        self.Xv = self.longueur/2
        self.Yv = self.hauteur
        self.dx = 10

        self.alien = PhotoImage(file = 'alien.gif')
        self.photo = PhotoImage(file = 'espace.gif')
        self.vaisseau = PhotoImage(file = 'vaisseau.gif')

        self.item = self.can.create_image(self.X, self.Y, anchor = 'nw', image = self.photo)
        self.imgAlien = self.can.create_image(self.X, self.Y, anchor ='nw',image = self.alien)
        self.imgVaisseau = self.can.create_image(self.Xv, self.Yv, anchor = 'sw', image = self.vaisseau)
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
        self.deplacementAlien()

        self.bind("<Left>",self.déplacementVaisseau_left)
        self.bind("<Right>",self.déplacementVaisseau_right)


    def deplacementAlien(self):
        if self.X+self.dx+self.alien.width() > self.longueur:
            self.dx = -self.dx
        self.X+=self.dx


        if self.X+self.dx< 0:
            self.dx = -self.dx
        self.X=self.X+self.dx

        self.can.coords(self.imgAlien,self.X,self.Y)
        self.after(500,self.deplacementAlien)



    def déplacementVaisseau_left(self,event):
        self.Xv -= 20

        self.can.coords(self.imgVaisseau, self.Xv, self.Yv)

    def déplacementVaisseau_right(self,event):
        self.Xv += 20

        self.can.coords(self.imgVaisseau, self.Xv, self.Yv)



space = space_invader()

space.mainloop()