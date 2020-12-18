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

hauteur = 500
longueur = 500
X = 0
Y = 0
vitesse = 10
dx = vitesse

class space_invader(Tk):
    def __init__(self):
        global hauteur, largeur,X,Y
        Tk.__init__(self)
        self.geometry('900x700+200+50')
        self.title('Space Invaders')
        
        
        self.can = Canvas(self,width = hauteur,height = longueur)
        
        self.alien = PhotoImage(file = 'alien.gif') 
        self.photo = PhotoImage(file = 'espace.gif')  
        self.vaisseau = PhotoImage(file = 'vaisseau.gif')
        
        self.item = self.can.create_image(X, Y, anchor = 'nw', image = self.photo)
        self.imgAlien = self.can.create_image(X, Y, anchor ='nw',image = self.alien)
        self.imgVaisseau = self.can.create_image(longueur/2, hauteur, anchor = 'sw', image = self.vaisseau) 
        #self.text1 = StringVar() 
        self.labelScore = Label(self, text = 'Score = self.text1') #textvariable pour score qui change en fonction du stringvar
        self.labelVie = Label(self, text = 'Vie = 3')
        
        self.buttonQuit = Button(self , text = 'Quitter' , fg = 'red' , command = self.destroy)
        
        self.newGame = Button(self, text = 'Démarrer une partie', command = self.init_partie)
        
        self.labelScore.grid(row = 1, column = 1, sticky = 'w')
        self.labelVie.grid(row = 1, column = 2, sticky = 'e')
        self.newGame.grid(row = 2, column = 3, rowspan = 1, sticky = 'e')
        self.buttonQuit.grid(row = 3, column = 3, rowspan = 1, sticky = "e")
        self.can.grid(row = 2 , column = 1, rowspan = 2, columnspan = 2,  sticky = "w")
        
    def init_partie(self):
        self.deplacementAlien()
        self.can.bind("<key>",self.déplacementVaisseau)

        
    def deplacementAlien(self):
        global hauteur, longueur, X, Y,dx
        
        
        if X+dx+self.alien.width() > longueur:
            dx = -dx
        X=X+dx
       
        
        if X+dx< 0:
            dx = -dx
        X=X+dx
       
        self.can.coords(self.imgAlien,X,Y)
        self.after(500,self.deplacementAlien)
        
    

    def déplacementVaisseau(self,event):
        global X,Y
        touche = event.keysym
        if touche == "left":   # Vers la droite
            X += 20
        if touche == "right":   # Vers la gauche
            X -= 20

        self.can.coords(self.imgVaisseau, X, Y)
        self.can.bind("left",self.déplacementVaisseau)
        self.can.bind("left",self.déplacementVaisseau)
        
space = space_invader()

space.mainloop()