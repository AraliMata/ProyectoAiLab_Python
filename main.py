import tkinter as tk
from Profile import HomePage, Login, Register, GameMode
from Game import Details, ShowCharacters, Combat

#Frames Controller
class tkinterApp(tk.Tk):
    
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        #Contrainer
        container = tk.Frame(self)
        self.geometry('400x300')
        container.pack(side="top", fill="both", expand=True)
        self.iconbitmap("Images/mousebug.ico")
        self.title("Datamon")
        #container.grid()
        self.mode = ""

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Frames creation
        self.frames = {}
        self.userData = {"name": "Default", "password": "Default", "character": 0, "level": 0}

        for F in (HomePage, Login, Register, GameMode, Details, ShowCharacters, Combat):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)
    
    
    #Function to updates a frame attribute
    def show_param_frame(self, frameName, parameter):
        self.frames[frameName].updateAtribute(parameter)
        self.show_frame(frameName)

    #Function to show a frame
    def show_frame(self, frameName):
        frame = self.frames[frameName]
        frame.tkraise()

    def startStory(self):
        if self.userData["level"] != 0:
            characterNum = self.userData["character"]
            self.frames[Combat].addCharacter(1, self.frames[ShowCharacters].characters[characterNum])
            self.frames[ShowCharacters].mode = "historia"
            self.show_combat(Combat) 
        
        else:
            self.show_param_frame(ShowCharacters, "historia")

    
    def show_combat(self, frameName):
        if(self.frames[ShowCharacters].mode=="historia"):
            oponentNum = self.userData["level"]
            self.frames[Combat].addCharacter(2, self.frames[ShowCharacters].characters[oponentNum]) 

        self.frames[frameName].updateAttributes(self.frames[ShowCharacters].mode)
        self.show_frame(frameName)
        self.frames[frameName].playGame()

    def on_closing(self):
        self.destroy()
    
# Driver Code
app = tkinterApp()
app.mainloop()