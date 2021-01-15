#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Programme principale du SpaceInvader
Eliott RAJAUD et Axel GUILLET
18/12/20
TODO :
    Mettre role, entree sortie de toutes les fcts
    Modif nom variable
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
        '''Role : Initialise la fenètre tkinter du Jeu
        Sortie : la fonction n'as pas de sortie mais certain boutton appel d'autre fonction
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
        self.listAlienBonus = []
        self.démarrer = 0
        self.score = 0
        self.end_game = 0
        self.AlienBonus_present = 0
        self.listeClasseInit()
        self.ilots()

    def ilots(self):
        self.protections = []
        self.listeIlot= []
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
        self.listAlien = []
        for j in range(0,3):
            for i in range(0,2):
                cAlien = Alien(self.can,i*60,j*60)
                self.listAlien.append(cAlien)

    def init_partie(self):
        if self.démarrer == 0:
            for i in range(0,len(self.listAlien)):
                self.listAlien[i].deplacementAlien()
                self.listAlien[i].laser()
            self.bind("<Left>",cVaisseau.deplacementVaisseauLeft)
            self.bind("<Right>",cVaisseau.deplacementVaisseauRight)
            self.bind("<space>",cVaisseau.laser)
            self.Create_Alien_Bonus()
            self.text2.set("Lifes : "+str(cVaisseau.vie))
            self.text1.set("Score : "+str(self.score))
            self.démarrer = 1
            cVaisseau.stop = 0

    def rejouer(self):
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
        self.ilots()
        self.listeClasseInit()
        self.démarrer = 0
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
        self.AlienBonus_present = 0
        self.end_game = 0




    def Create_Alien_Bonus(self):
        if self.end_game == 0:
            notAliensup = 0
            for i in range (len(self.listAlien)):
                if self.listAlien[i].y == 0:
                    notAliensup = 1
            if notAliensup == 0 and self.AlienBonus_present == 0:
                rnd = rd.random()*40
                if rnd <= 1:
                    cAlienBonus = AlienBonus(self.can)
                    if len(self.listAlienBonus) == 1:
                        self.listAlienBonus.pop(0)
                    self.listAlienBonus.append(cAlienBonus)
                    self.AlienBonus_present = 1
                    cAlienBonus.deplacementAlienBonus()
            space.after(200,self.Create_Alien_Bonus)


class Alien():
    def __init__(self,canvas,x,y):
        self.can = canvas
        self.x  = x
        self.y  = y
        self.dx = 7
        self.stop = 0
        self.present = 0
        self.toucher_droit = 0
        self.toucher_gauche = 0
        self.alien = PhotoImage(file = 'alien.gif')

        self.imgAlien = self.can.create_image(self.x, self.y, anchor ='nw',image = self.alien)
        self.xl = self.x + self.alien.height()/2
        self.yl = self.y + self.alien.width()
        self.dy = 10
        self.a = -1
        self.verif = 0
        self.score_alien = 100


    def deplacementAlien(self):
        if self.stop == 0:
            self.toucher_droit = 0
            if (space.listAlien)[len(space.listAlien)-1].x+(space.listAlien)[len(space.listAlien)-1].dx+(space.listAlien)[len(space.listAlien)-1].alien.width() > space.longueur:
                for i in range(len(space.listAlien)):
                    space.listAlien[i].toucher_droit = 1


            if self.verif % 2 == 0:
                if space.listAlien[0].x+space.listAlien[0].dx< 0:
                    for i in range(len(space.listAlien)):
                        space.listAlien[i].toucher_gauche = 1
                        space.listAlien[i].verif = 1

            if self.toucher_droit == 1:
                self.dx = -self.dx
                self.toucher_droit = 0


            if self.toucher_gauche == 1:
                self.dx = -self.dx
                self.y += self.alien.height()
                self.toucher_gauche = 0
            self.x += self.dx

            if self.y >= space.hauteur/2:
                self.can.coords(self.imgAlien,self.x,self.y)
                self.can.delete(cVaisseau.imgVaisseau)
                cVaisseau.vie = 0
                space.text2.set("Lifes : "+str(cVaisseau.vie))
                for i in range(len(space.listAlien)):
                    space.listAlien[i].present = 1
                    space.listAlien[i].stop = 1
                    if space.AlienBonus_present == 1:
                        space.listAlienBonus[0].stop = 1
                space.end_game = 1
                messagebox.showinfo('GameOver','Vous avez perdu')

            else:
                self.can.coords(self.imgAlien,self.x,self.y)
                space.after(200,self.deplacementAlien)
                self.verif += 1


    def laser(self):
        if self.stop == 0 and self.present == 0:
            rnd = rd.random()*5
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
        self.a = -1
        if self.yl >= space.hauteur:
            self.present = 0
            self.can.delete(self.tir)
            space.after(800,self.laser)

        else:
            self.yl += self.dy
            self.can.coords(self.tir, self.xl-2, self.yl, self.xl+2, self.yl + 30)
            space.after(20, self.deplacementLaser)

        if self.present == 1:
            if (cVaisseau.xv <= self.can.coords(self.tir)[0] <= cVaisseau.xv + cVaisseau.vaisseau.width()) and (cVaisseau.yv - cVaisseau.vaisseau.height()<= self.can.coords(self.tir)[3] <= cVaisseau.yv):
                self.present = 0
                self.can.delete(self.tir)
                cVaisseau.vie -= 1
                space.text2.set("Lifes : "+str(cVaisseau.vie))

                if cVaisseau.vie == 0:
                    self.can.delete(cVaisseau.imgVaisseau)
                    for i in range(len(space.listAlien)):
                        space.listAlien[i].stop = 1
                        if space.AlienBonus_present == 1:
                            space.listAlienBonus[0].stop = 1
                    space.end_game = 1
                    messagebox.showinfo('GameOver','Vous avez perdu')

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
        self.can = canvas
        self.xb  = 500
        self.yb  = 0
        self.dx = 7
        self.alienBonus = PhotoImage(file = 'alienBonus.gif')
        self.imgAlienBonus = self.can.create_image(self.xb, self.yb, anchor ='nw',image = self.alienBonus)
        self.stop = 0
        self.score_alien_bonus = 200

    def deplacementAlienBonus(self):
        if self.stop == 0:
            self.xb -= self.dx
            self.can.coords(self.imgAlienBonus,self.xb,self.yb)
            if self.xb + self.alienBonus.width() <= 0:
                self.can.delete(self.imgAlienBonus)
                self.stop = 1
                space.AlienBonus_present = 0
            space.after(100,self.deplacementAlienBonus)



class Vaisseau():
    def __init__(self):
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
        if self.stop == 0:
            if self.vie > 0:
                if self.xv > 0:
                    self.xv -= 20
                self.can.coords(self.imgVaisseau, self.xv, self.yv)

    def deplacementVaisseauRight(self,event):
        if self.stop == 0:
            if self.vie > 0:
                if self.xv + self.vaisseau.width() < space.longueur:
                    self.xv += 20
                self.can.coords(self.imgVaisseau, self.xv, self.yv)

    def laser(self,event):
        if self.present == 0 and self.vie > 0 and self.stop == 0:
            self.xl = self.xv
            self.yl = self.yv
            self.tir = self.can.create_rectangle(self.xl+self.vaisseau.width()/2-2, self.yl-self.vaisseau.height()-30, self.xl+self.vaisseau.width()/2+2, self.yl-self.vaisseau.height(),fill='blue')
            self.present = 1
            self.deplacementLaser()


    def deplacementLaser(self):
        self.a = -1
        if self.yl <= 0:
            self.can.delete(self.tir)
            self.present = 0

        else:
            self.yl -= self.dy
            self.can.coords(self.tir, self.xl+self.vaisseau.width()/2-2, self.yl-self.vaisseau.height()-30, self.xl+self.vaisseau.width()/2+2, self.yl-self.vaisseau.height())
            space.after(20, self.deplacementLaser)



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
                        if space.AlienBonus_present == 1:
                            space.listAlienBonus[0].stop = 1
                        space.end_game = 1
                        messagebox.showinfo('Gagné','Vous avez gagné, félicitations')

        if space.AlienBonus_present == 1:
            if self.present == 1:
                if (space.listAlienBonus[0].xb <= self.can.coords(self.tir)[0] <= space.listAlienBonus[0].xb + space.listAlienBonus[0].alienBonus.width()) and (space.listAlienBonus[0].yb <= self.can.coords(self.tir)[1] <= space.listAlienBonus[0].yb + space.listAlienBonus[0].alienBonus.height()):
                    self.can.delete(space.listAlienBonus[0].imgAlienBonus)
                    self.can.delete(self.tir)
                    self.present = 0
                    space.listAlienBonus[0].stop = 1
                    space.AlienBonus_present = 0
                    space.score += space.listAlienBonus[0].score_alien_bonus
                    space.text1.set("Score : "+str(space.score))



space = SpaceInvader()
cVaisseau = Vaisseau()


space.mainloop()
