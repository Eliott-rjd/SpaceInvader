#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programme principale du SpaceInvader
Eliott RAJAUD et Axel GUILLET
18/12/20
TODO : 
"""

from tkinter import Tk,Label,Canvas,Button,StringVar,PhotoImage


class space_invader(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry('800x500+500+200')
        self.title('Space Invaders')
        
        self.can=Canvas(self,width=500,height=500)
        self.photo = PhotoImage(file='space.gif')
        self.item = self.can.create_image(0,0, anchor='nw', image=self.photo)
        
        #self.text1 = StringVar() 
        self.LabelScore = Label(self, text = 'self.text1') #textvariable pour score qui change en fonction du stringvar
        self.LabelVie = Label(self, text='3')
        
        self.buttonQuit = Button(self , text='Quitter' , fg = 'red' , command = self.destroy)
        
        self.newGame = Button(self, text='Démarrer une partie') #command = self.init_partie
        
        self.LabelScore.grid(row=1, column=1, sticky='w')
        self.LabelVie.grid(row=1, column=2, sticky='e')
        self.newGame.grid(row=2, column=3,rowspan=1, sticky='e')
        self.buttonQuit.grid(row=3, column = 3, rowspan=1, sticky = "e")
        self.can.grid(row=2, column=1,rowspan=2, columnspan = 2,  sticky = "w")
        

space = space_invader()
space.mainloop()