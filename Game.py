import time
import tkinter as tk
from tkinter import ttk
from tkinter import *
from Player import Player
from Character import Character
import random
import csv
from PIL import ImageTk, Image
from tkinter import messagebox


class GameMode(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #title label
        playLabel = ttk.Label(self, text="¡A jugar!", style="wNS.TLabel" , font=("Verdana", 20))
        playLabel.pack(side=tk.TOP, pady=10)

        #Training mode button
        trnModeBtn = ttk.Button(self, text="Modo entrenamiento", style="BW.TButton", command=lambda: controller.show_param_frame(ShowCharacters, "entrenamiento"))
        trnModeBtn.pack(side=tk.TOP, padx=10, pady=40, ipady=5)

        #History mode button
        historyModeBtn = ttk.Button(self, text="Modo historia", style="BW.TButton", command=lambda: controller.startStory())
        historyModeBtn.pack(side=tk.TOP, padx=10, pady=10, ipady=5)

class Details(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.character = Character("Aquarder", "Agua", skills={"Aqua-jet":[3,5,2,5,7,4], "Cola ferrea": [2], "Cabezazo": [2]},
                        advantage=["Roca", "Fuego"], disadvantage=["Electrico", "Planta"], normal=["Agua", "Escarabajo"],
                        booster="Lluvia", path="Personajes/aquarder.png")


        
        img = Image.open("Images/back-icon.png")
        image = img.resize((30,30))
        self.imgBtn = ImageTk.PhotoImage(image)

        ttk.Button(self, image=self.imgBtn, command= lambda:controller.show_frame(ShowCharacters)).grid(row=0, column=0, columnspan=2)

        img = Image.open(self.character.path)
        image = img.resize((70,70))
        self.img1 = ImageTk.PhotoImage(image)

        #Image
        self.imageLabel = ttk.Label(self, image=self.img1)
        self.imageLabel.grid(row=1, column=0, columnspan=7)

        #Type Label
        self.type = tk.StringVar()
        typeLabel = ttk.Label(self, textvariable=self.type, style="BW.TLabel" , font=("Verdana", 12))
        typeLabel.grid(row=2, column=0, columnspan=7)
        #Advantage Label
        self.advantage = tk.StringVar()
        advLabel = ttk.Label(self, textvariable=self.advantage, style="BW.TLabel" , font=("Verdana", 9))
        advLabel.grid(row=3, column=0, columnspan=7)
        #Disadvantage Label
        self.disadvantage = tk.StringVar()
        disadvLabel = ttk.Label(self, textvariable=self.disadvantage, style="BW.TLabel" , font=("Verdana", 9))
        disadvLabel.grid(row=4, column=0, columnspan=7)
        #Normal label
        self.normal = tk.StringVar()
        normalLabel = ttk.Label(self, textvariable=self.normal, style="BW.TLabel" , font=("Verdana", 9))
        normalLabel.grid(row=4, column=0, columnspan=7)

        self.createTable()
        

    def createTable(self):
        firstRowText = ["|Habilidad", "| norm ", "| At vent ", "| At desv ", "| pot norm ", "| pot vent ", "| pot desv |"]
        for columnNum in range(7):
            ttk.Label(self, text=firstRowText[columnNum], style="BW.TLabel", font=("Verdana", 7)).grid(row=5, column=columnNum)
    
        self.skillsColumnText = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]

        for rowNum in range(4):
            ttk.Label(self, textvariable=self.skillsColumnText[rowNum], style="BW.TLabel", font=("Verdana", 7)).grid(row=6+rowNum, column=0)
        
        self.firstSkillRowText = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()] 
        for columnNum in range(6):
            ttk.Label(self, textvariable=self.firstSkillRowText[columnNum], style="BW.TLabel", font=("Verdana", 7)).grid(row=6, column=columnNum+1)

        self.secondSkillText = tk.StringVar()
        self.thirdSkillText = tk.StringVar()
        self.boosterText = "| Potenciador de campo, 1 vez cada 3 turnos"
        self.boosterText2 = "| tiene una duración de 2 turnos."
        
        ttk.Label(self, textvariable=self.secondSkillText, style="BW.TLabel", font=("Verdana", 7)).grid(row=7, column=1)
        ttk.Label(self, textvariable=self.thirdSkillText, style="BW.TLabel", font=("Verdana", 7)).grid(row=8, column=1)
        ttk.Label(self, text=self.boosterText, style="BW.TLabel", font=("Verdana", 7)).grid(row=9, column=1, columnspan=6, sticky=tk.W)
        ttk.Label(self, text=self.boosterText2, style="BW.TLabel", font=("Verdana", 7)).grid(row=10,column=1, columnspan=6, sticky=tk.W)

    
    #Function to update character
    def updateAtribute(self, character):
        self.character = character
        self.updateLabels()
        self.updateImage()
    
    #Fucntion to update labels with the current character
    def updateLabels(self):
        type = self.character.name + ": Tipo " + self.character.type
        self.type.set(type)
        advantage = "Ventaja con: " + ", ".join(self.character.advantage)
        self.advantage.set(advantage)
        disadvantage = "Desventaja con: " + ", ".join(self.character.disadvantage)
        self.disadvantage.set(disadvantage)
        normal = "Normal con: " + ", ".join(self.character.normal)
        self.disadvantage.set(normal)

        skills = list(self.character.skills.keys()) + [self.character.booster]
        for i in range(4):
            self.skillsColumnText[i].set(skills[i])

        firstAttackPoints = self.character.skills[skills[0]]
        for i in range(6):
            self.firstSkillRowText[i].set(firstAttackPoints[i])

        self.secondSkillText.set(self.character.skills[skills[1]])
        self.thirdSkillText.set(self.character.skills[skills[2]])

    #Function to update images
    def updateImage(self):
        img = Image.open(self.character.path).resize((70,70))
        self.img1 = ImageTk.PhotoImage(img)
        self.imageLabel.config(image=self.img1)

class ShowCharacters(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.charButtons = []
        self.characters = self.createCharacters()

        self.aquaImg = self.createImage(self.characters[0].path)
        self.electImg = self.createImage(self.characters[1].path)
        self.fireImg = self.createImage(self.characters[2].path)
        self.mouseImg = self.createImage(self.characters[3].path)
        self.rockImg = self.createImage(self.characters[4].path)
        self.splantImg = self.createImage(self.characters[5].path)

        self.selectNum = 0
        self.controller = controller
        self.mode = "training"
        
        self.showCharacter([0,1,2], 0, 0, self.aquaImg)
        self.showCharacter([0,1,2], 1, 1, self.electImg)
        self.showCharacter([0,1,2], 2, 2, self.fireImg)
        self.showCharacter([4,5,6], 0, 3, self.mouseImg)
        self.showCharacter([4,5,6], 1, 4,  self.rockImg )
        self.showCharacter([4,5,6], 2, 5, self.splantImg )

        charBtn =  ttk.Button(self, text="Iniciar", command= self.startCombat)
        charBtn.grid(row=11, column=1)
    

    def showCharacter(self, rows, column, number, image):
        nameRow, imageRow, detailRow = rows
        nameLbl = ttk.Label(self, text=self.characters[number].name, style="BW.TLabel" , font=("Verdana", 8))
        nameLbl.grid(row=nameRow, column=column)

        charBtn =  ttk.Button(self, image=image, command= lambda:self.playerSelected(self.characters[number], number))
        charBtn.grid(row=imageRow, column=column)
        self.charButtons.append(charBtn)

        detailsBtn =  ttk.Button(self, text="Detalles", style="BW.TButton", command=lambda:self.controller.show_param_frame(Details, self.characters[number]))
        detailsBtn.grid(row=detailRow, column=column)


    def playerSelected(self, character, idx):
        self.selectNum += 1
        if self.mode == "historia":
            self.controller.frames[Combat].addCharacter(1, character)
            self.update()
            messagebox.showinfo(message="Jugador seleccionado", title="Puedes iniciar")
        else:
            if self.selectNum == 1:
                self.controller.frames[Combat].addCharacter(self.selectNum, character)
                messagebox.showinfo(message="Selecciona tu contrincante", title="Contrincante")
            elif self.selectNum == 2:
                messagebox.showinfo(message="Contrincante seleccionado", title="Puedes iniciar")
                self.controller.frames[Combat].addCharacter(self.selectNum, character)
    
    def startCombat(self):
        answer = messagebox.askyesno(message="¿Estás listo? El combate está a punto de comenzar", title="Comencemos")
        if answer:
            self.controller.show_combat(Combat)

    def createImage(self, path):
        img = Image.open(path)
        image = img.resize((70,70))
        img1 = ImageTk.PhotoImage(image)

        return img1

    def updateAtribute(self,mode):
        self.controller.frames[Combat].mode = mode
        self.mode = mode
    

    def createCharacters(self):
        aquarder = Character("Aquarder", "Agua", skills={"Aqua-jet":[3,5,2,5,7,4], "Cola ferrea": [2], "Cabezazo": [2]},
                        advantage=["Roca", "Fuego"], disadvantage=["Electrico", "Planta"], normal=["Agua", "Escarabajo"],
                        booster="Lluvia", path="Personajes/aquarder.png")
        firesor = Character("Firesor","Fuego", skills={"Llamarada":[3,5,2,5,7,4], "Embestida": [2], "Mordisco": [2]},
                        advantage=["Planta", "Escarabajo"], disadvantage=["Agua", "Roca"], normal=["Electrico", "Fuego"],
                        booster="Día soleado", path="Personajes/firesor.png")
        
        electder = Character("electder","Electrico", skills={"Trueno":[3,5,2,5,7,4], "Arañazo": [3], "Mordisco": [3]},
                        advantage=["Agua", "Escarabajo"], disadvantage=["Roca", "Planta"],normal=["Electrico", "Fuego"],
                        booster="Campo magnético", path="Personajes/electder.png")

        mousebug = Character("mousebug","Escarabajo", skills={"Picotazo":[3,5,2,5,7,4], "Embestida": [2], "Cabezazo": [2]},
                        advantage=["Roca", "Planta"], disadvantage=["Electrico", "Fuego"], normal=["Escarabajo", "Agua"],
                        booster="Esporas", path="Personajes/mousebug.png")

        splant = Character("splant", "Planta", skills={"Hoja navaja":[3,5,2,5,7,4], "Mordisco": [2], "Cabezazo": [2]},
                        advantage=["Roca","Agua", "Electrico"], disadvantage=["Fuego", "Escarabajo"], normal=["Planta"],
                        booster="Rayo solar", path="Personajes/splant.png")

        rockdog = Character("rockdog", "Roca", skills={"Roca afilado":[3,5,2,5,7,4], "Velocidad": [2], "Cola ferrea": [2]},
                        advantage=["Electrico", "Fuego"], disadvantage=["Agua", "Planta"], normal=["Roca", "Escarabajo"],
                        booster="Campo rocoso", path="Personajes/rockdog.png")

        return [aquarder, firesor, electder, mousebug, splant, rockdog]
    
class Combat(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.player1 = Player()
        self.player2 = Player()
        self.currentAttack = None

        #self.turn = player1
        self.controller = controller
        self.parent = parent
        self.mode = "Training"
        
        self.attackButtons = []
        #First attack
        self.attack1 = tk.StringVar()
        self.createAttackButton(self.attack1, 0, 0, 0)
        #Second attack
        self.attack2 = tk.StringVar()
        self.createAttackButton(self.attack2, 1, 0, 1)
        #Third attaack
        self.attack3 = tk.StringVar()
        self.createAttackButton(self.attack3, 2, 0, 2)
        #Booster
        self.booster = tk.StringVar()
        self.createAttackButton(self.booster, 3, 0, 3)

        self.waitSelected = tk.IntVar()

        newsize = (100, 100)
        #Image player 1
        img = Image.open("Personajes/aquarder.png")
        img2 = img.resize(newsize)
        self.imagePl1 = ImageTk.PhotoImage(img2)
        self.imgPl1Label =ttk.Label(self, image=self.imagePl1, style="BW.TLabel", font=("Verdana", 9))
        self.imgPl1Label.grid(row=0, column=3, rowspan=4)

        #Image oponent
        img = Image.open("Personajes/electder.png")
        img3 = img.resize(newsize)
        self.imgOp = ImageTk.PhotoImage(img3)
        self.imgOpLabel = ttk.Label(self, image=self.imgOp, style="BW.TLabel", font=("Verdana", 9))
        self.imgOpLabel.grid(row=0, column=6, rowspan=4)

        #Data player 1
        self.namePl1Text = tk.StringVar()
        namePl1Label = ttk.Label(self, textvariable=self.namePl1Text, style="BW.TLabel", font=("Verdana", 18))
        namePl1Label.grid(row=6, column=3)
        self.hpPl1Text = tk.StringVar()
        hpPl1Label = ttk.Label(self, textvariable=self.hpPl1Text, style="BW.TLabel", font=("Verdana", 20))
        hpPl1Label.grid(row=7, column=3)

        #Data oponent
        self.nameOpText = tk.StringVar()
        nameOpLabel = ttk.Label(self, textvariable=self.nameOpText, style="BW.TLabel", font=("Verdana", 18))
        nameOpLabel.grid(row=6, column=6)
        self.hpOpText = tk.StringVar()
        hpOpLabel = ttk.Label(self, textvariable=self.hpOpText, style="BW.TLabel", font=("Verdana", 20))
        hpOpLabel.grid(row=7, column=6)

        #Turn label
        self.turnText = tk.StringVar()
        turnLabel = ttk.Label(self, textvariable=self.turnText, style="BW.TLabel", font=("Verdana", 12))
        turnLabel.grid(row=11, column=0, columnspan=8, sticky=tk.EW)

        #Used attack label
        self.attackUsedText = tk.StringVar()
        attackUsedLabel = ttk.Label(self, textvariable=self.attackUsedText, style="BW.TLabel", font=("Verdana", 12))
        attackUsedLabel.grid(row=14, column=0, columnspan=8, sticky=tk.EW)
    
    def selectAttack(self, num):
        attack = self.attacks[num] if num != 3 else self.player1.character.booster

        if num == 3:
            self.attackButtons[3].config(state=tk.DISABLED)
       
        self.currentAttack = attack
        self.waitSelected.set(1)
        
    def firstTurn(self):
        t=random.randint(1,2)
        if (t==1):
            self.turnText.set("Primer movimiento es tuyo " + self.player1.character.name)
            self.update()
    
        else:
            self.turnText.set("Primer movimiento es del CPU\n¡¡Cuidado!!\n")
            self.update()
          
        time.sleep(1)

        return t

    def playGame(self):
        turn = self.firstTurn()
        self.attacks2 = list(self.player2.character.skills.keys())
        
    
        self.controller.protocol("WM_DELETE_WINDOW", lambda:self.closeGame())

        character1 = self.player1.character.name
        character2 = self.player2.character.name
        

        if not self.player1.booster[0]:
            self.attackButtons[3].config(state=tk.NORMAL)

        while self.player1.hp > 0 and self.player2.hp > 0:
            if turn == 1:
                self.turnText.set("Es tu turno "+ character1)
                self.update()
                self.changeButtonsState(tk.NORMAL)
                self.wait_variable(self.waitSelected)                

                points = self.player1.attack(self.currentAttack)
                self.player2.receiveAttack(points)

                self.updateHpLabels()
                self.attackUsedText.set(character1 + " ha utilizado " + self.currentAttack)
                self.update()

                turn = 2
            elif turn == 2:
                self.changeButtonsState(tk.DISABLED)
                self.turnText.set("Es tu turno oponente "+ character2)
                self.update()
                attack = self.cpuAttack()
                

                points = self.player2.attack(attack)

                self.player1.receiveAttack(points)
                time.sleep(3)
                self.updateHpLabels()
                self.attackUsedText.set("Oponente "+ character2 + " ha utilizado " + attack)
                self.update()
    
                turn = 1

        if self.mode == "historia":
            self.gameOverStory()
        else:
            self.gameOverTraining()

    def gameOverStory(self):
        character = self.player1.character
        hp1 = self.player1.hp
        hp2 = self.player2.hp

        self.player1 = Player()
        self.player2 = Player()

        self.controller.protocol("WM_DELETE_WINDOW", self.controller.on_closing)

        if hp2 > hp1:
            answer = messagebox.askyesno(message="Perdiste :( ¿Deseas reiniciar el combate?", title="Reiniciar")
            self.addCharacter(1, character)
            if answer:
                self.attackUsedText.set("")
                self.controller.startStory()
            else:
                self.controller.show_frame(GameMode)

        elif hp1 > hp2:

            self.controller.userData["level"] += 1

            if self.controller.userData["level"] > 5:
                answer = messagebox.showinfo(message="¡¡Felicidades!! Has terminado el modo historia. Puedes intentar iniciar de nuevo la aventura.", title="Terminado")

                self.controller.userData["level"] = 0
                self.controller.userData["character"] = 0
                self.saveProgress()
                self.controller.show_frame(GameMode)
                
            else:
                self.saveProgress()
                self.addCharacter(1, character)

                answer = messagebox.askyesno(message="¡Felicidades! Ganaste el combate ¿Deseas seguir jugando?", title="Seguir jugando")

                if answer:
                    self.controller.startStory()
                else:
                    self.controller.show_frame(GameMode)

    def gameOverTraining(self):
        self.controller.frames[ShowCharacters].selectNum = 0

        if self.player2.hp > self.player1.hp:
            messagebox.showinfo(message="Perdiste :( Nos vemos en la siguiente partida ", title="Perdiste")
        else:
            messagebox.showinfo(message="¡Felicidades! Nos vemos en la siguiente partida ", title="Ganaste")
        
        self.player1 = Player()
        self.player2 = Player()

        self.controller.protocol("WM_DELETE_WINDOW", self.controller.on_closing)
        self.controller.show_param_frame(ShowCharacters, "entrenamiento")

    def closeGame(self):
        self.controller.protocol("WM_DELETE_WINDOW", self.controller.on_closing)

        character = self.player1.character
        self.player1 = Player()
        self.player2 = Player()

        if self.mode == "historia":
            answer = messagebox.askyesno(message="¿Deseas reiniciar el combate?", title="Reiniciar")
            self.addCharacter(1, character)
            if answer:
                self.attackUsedText.set("")
                self.controller.show_combat(Combat)
            else:
                self.controller.show_frame(GameMode)
        else:
            answer = messagebox.askyesno(message="¿Deseas reintentar?", title="Reintentar")
            self.controller.frames[ShowCharacters].selectNum = 0
            if answer:
                
                self.controller.show_param_frame(ShowCharacters, "entrenamiento")
            else:
                self.controller.destroy()

    def cpuAttack(self):
        if self.player2.boosterAvailable():
            numAttack = random.randint(0,3)
        else:
            numAttack = random.randint(0,2)

        if numAttack == 3:
            attack = self.player2.character.booster
        else:
            attack = self.attacks2[numAttack]

        return attack
    
    def addCharacter(self, type, character):
        if type == 1:
            self.player1.character = character
        else:
            self.player2.character = character
            self.player2.enemyType = self.player1.character.type
            self.player1.enemyType = character.type
    
    def createAttackButton(self, text, row, column, num):
        attackButton = ttk.Button(self, textvariable=text, style="BW.TButton", command=lambda:self.selectAttack(num))
        attackButton.grid(row=row, column=column)

        self.attackButtons.append(attackButton)

    def changeButtonsState(self, state):
        for button in self.attackButtons:
            button.config(state=state)
        
        if self.player1.booster[0]:
            self.attackButtons[3].config(state=tk.DISABLED)

    def updateDataPlayer1(self):
        character = self.player1.character

        self.attacks = list(character.skills.keys())
        self.attack1.set(self.attacks[0])
        self.attack2.set(self.attacks[1])
        self.attack3.set(self.attacks[2])
        self.booster.set(character.booster)

        self.namePl1Text.set(self.player1.character.name)

    def updateHpLabels(self):
        hp1 = 0 if self.player1.hp < 0 else self.player1.hp
        hp2 = 0 if self.player2.hp < 0 else self.player2.hp
        self.hpPl1Text.set(hp1)
        self.hpOpText.set(hp2)

    def updateImage(self, num):
    
        if num == 1:
            self.img = Image.open(self.player1.character.path).resize((70,70))
            self.imagePl1 = ImageTk.PhotoImage(self.img)
            self.imgPl1Label.config(image=self.imagePl1)
        else:
            self.img = Image.open(self.player2.character.path).resize((70,70))
            self.imageOp = ImageTk.PhotoImage(self.img)
            self.imgOpLabel.config(image=self.imageOp)

    def updateAttributes(self, mode):
        self.mode = mode
        self.updateDataPlayer1()
        self.updateImage(1)

        self.updateImage(2)
        self.updateHpLabels()
        self.nameOpText.set(self.player2.character.name)

    def saveProgress(self):
        path_to_file = "InformacionUsuarios/" + self.controller.userData["name"] + ".csv"

        file = open(path_to_file, "w")
        writer = csv.writer(file)

        header = ["Contraseña", "Personaje", "Nivel"]
        data = [self.controller.userData["password"], str(self.controller.userData["character"]), str(self.controller.userData["level"])]

        writer.writerow(header)
        writer.writerow(data)
        