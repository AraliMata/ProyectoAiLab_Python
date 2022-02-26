import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import csv
from os.path import exists
from Game import GameMode

LARGEFONT = ("Verdana", 35)


# Home page
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #Buttons style
        buttonStyle = ttk.Style()
        buttonStyle.theme_use('alt')
        buttonStyle.configure('TButton', background = '#72c6ff', foreground = 'white', 
                            width = 20, height = 10, borderwidth=1, focusthickness=3, focuscolor='none')
        buttonStyle.map('TButton', background=[('active','#485cc3')])

        #Windows title style
        windowNameStyle = ttk.Style()
        windowNameStyle.configure("wNS.TLabel",background="#F0F0F0", foreground="#F5B041", font=("Verdana", 20))
        
        #Common labels style
        generalLabelStyle = ttk.Style()
        generalLabelStyle.configure("BW.TLabel",background="#F0F0F0")

        #Selected Player Button Style
        buttonPlayerStyle = ttk.Style()
        buttonPlayerStyle.theme_use('alt')
        buttonPlayerStyle.configure("PlayerButton", background = '#ff1943', foreground = 'white', 
                            width = 20, height = 10, borderwidth=1, focusthickness=3, focuscolor='none')
        #buttonPlayerStyle.map('TButton', background=[('active','#485cc3')])


        #Selected Oponent Button Style

        #Welcome label
        welcomeLabel = ttk.Label(self, text="¡Bienvenido!", style="wNS.TLabel", font=("Verdana", 20))
        welcomeLabel.pack(side=tk.TOP, pady=10)

        #Login Button
        loginBtn = ttk.Button(self, text="Iniciar sesión", style="BW.TButton", command=lambda: controller.show_frame(Login))
        loginBtn.pack(side=tk.TOP, padx=10, pady=40, ipady=5)

        #Register Button
        registerBtn = ttk.Button(self, text="Registrarse", style="BW.TButton", command=lambda: controller.show_frame(Register))
        registerBtn.pack(side=tk.TOP, padx=10, pady=10, ipady=5)


#Login page
class Login(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Iniciar sesión", style="wNS.TLabel")
        label.pack(pady=10)

        self.username_verify = StringVar()
        self.password_verify = StringVar()
        self.controller = controller

        #Username label
        ttk.Label(self, text="Nombre de usuario *", style="BW.TLabel").pack(side=tk.TOP,padx=10, pady=10)
        #Username entry
        self.username_login_entry = ttk.Entry(self, textvariable=self.username_verify)
        self.username_login_entry.pack(side=tk.TOP, padx=10, pady=10)

        #Password label
        ttk.Label(self, text="Contraseña * ", style="BW.TLabel").pack(side=tk.TOP, padx=10, pady=10)
        #Password entry
        self.password_login_entry = ttk.Entry(self, textvariable=self.password_verify, show='*')
        self.password_login_entry.pack(side=tk.TOP, padx=10, pady=10)
        
        #Login Button
        ttk.Button(self, text="Iniciar sesión", style="BW.TButton", command=self.login).pack(side=tk.TOP, pady=20, ipady=5)

    #Function to login
    def login(self):
        username_info = self.username_verify.get()
        password_info = self.password_verify.get()

        path_to_file = "InformacionUsuarios/" + username_info + ".csv"

        if exists(path_to_file):
            file = open(path_to_file)

            csv_reader = csv.reader(file)
            count = 0

            for row in csv_reader:
            
                if count == 2:
                    if password_info == row[0]:
                        messagebox.showinfo(message="Sesión iniciada", title="Datamon")
                        self.controller.userData["name"] = username_info
                        self.controller.userData["password"] = password_info
                        self.controller.userData["character"] = int(row[1])
                        self.controller.userData["level"] = int(row[2])
                        self.controller.show_frame(GameMode)
                    else:
                        messagebox.showinfo(message="Contraseña incorrecta, intente de nuevo", title="Datamon")
                        self.password_login_entry.delete(0, 'end')

                count += 1
        else:
            register = messagebox.askokcancel(
                message="No se encontró el usuario ¿Deseas registrar un usuario nuevo?", title="Usuario no encontrado")
        
            if register:
                self.controller.show_frame(Register)
            
            self.clear_data()

    #Function to clear entries
    def clear_data(self):
        self.username_login_entry .delete(0, 'end')
        self.password_login_entry.delete(0, 'end')

#Register page
class Register(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.username = StringVar()
        self.password = StringVar()
        password2 = StringVar()

        #Register label
        ttk.Label(self, text="Registro", style="wNS.TLabel").pack(pady=10)

        #Username label
        ttk.Label(self, text="Usuario", style="BW.TLabel").pack(side=tk.TOP, pady=10)
        #Username entry
        self.username_entry = ttk.Entry(self, textvariable=self.username)
        self.username_entry.pack(side=tk.TOP)

        #Password label
        ttk.Label(self, text="Contraseña", style="BW.TLabel").pack(side=tk.TOP, pady=10)
        #Password entry
        self.password_entry = ttk.Entry(self, textvariable=self.password, show='*')
        self.password_entry.pack(side=tk.TOP)

        #Rewrite password label
        ttk.Label(self, text="Re-escribir contraseña", style="BW.TLabel").pack(side=tk.TOP, pady=10)
        #Rewrite password entry
        self.re_password_entry = ttk.Entry(self, textvariable=password2, show='*')
        self.re_password_entry.pack(side=tk.TOP)

        #Register button
        ttk.Button(self, text="Registrarse", style="BW.TButton", command=self.register_user).pack(side=tk.TOP, pady=20, ipady=5, ipadx=10)

    #Function to register new user
    def register_user(self):
        username_info = self.username.get()
        password_info = self.password.get()

        path_to_file = "InformacionUsuarios/" + username_info + ".csv"

        if not self.same_password():
            messagebox.showinfo(message="Las contraseñas no coinciden, por favor intente de nuevo", title="Contraseñas no coinciden")
            self.clear_data()
        elif exists(path_to_file):
            answer = messagebox.askokcancel(
                message="¿Desea iniciar sesión?", title="Usuario existente")

            if answer == 'OK':
                self.controller.show_frame(Login)
            else:
                self.controller.show_frame(HomePage)
        else:
            file = open(path_to_file, "w")
            writer = csv.writer(file)

            header = ["Contraseña", "Personaje", "Nivel"]
            data = [password_info, "0", "0"]

            writer.writerow(header)
            writer.writerow(data)

            messagebox.showinfo(
                message="Usuario registrado exitosamente", title="Datamon")
            self.controller.show_frame(Login)

    #Function to check if passwords in entries are the same
    def same_password(self):
        if self.password_entry.get() == self.re_password_entry.get():
            return True

        return False

    #Function to clear entries
    def clear_data(self):
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.re_password_entry.delete(0, 'end')
