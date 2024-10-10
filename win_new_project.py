import customtkinter as CTk
import os
import sys
from connect_db import sql
from spinbox import Spinbox

CTk.set_appearance_mode("dark")
CTk.set_default_color_theme("green")

class Object_str(CTk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, width=400, height=330)
        self.ttle_korp = CTk.CTkLabel(master=self, text="Выберите количество корпусов")
        self.ttle_korp.grid(row=0, column=0, padx=(5,5), pady=(5,5))
        self.counter_k = Spinbox(self)
        self.counter_k.grid(row=1, column=0, padx=(5,5), pady=(5,5))

        self.ttle_sosh = CTk.CTkLabel(master=self, text="Выберите количество СОШ")
        self.ttle_sosh.grid(row=2, column=0, padx=(5,5), pady=(5,5))
        self.counter_sosh = Spinbox(self)
        self.counter_sosh.grid(row=3, column=0, padx=(5,5), pady=(5,5))

        self.ttle_sosh = CTk.CTkLabel(master=self, text="Выберите количество ДОУ")
        self.ttle_sosh.grid(row=4, column=0, padx=(5,5), pady=(5,5))
        self.counter_sosh = Spinbox(self)
        self.counter_sosh.grid(row=5, column=0, padx=(5,5), pady=(5,5))

        self.ttle_med = CTk.CTkLabel(master=self, text="Выберите количество медучреждений")
        self.ttle_med.grid(row=6, column=0, padx=(5,5), pady=(5,5))
        self.counter_med = Spinbox(self)
        self.counter_med.grid(row=7, column=0, padx=(5,5), pady=(5,5))

        self.ttle_depo = CTk.CTkLabel(master=self, text="Выберите количество Пождепо")
        self.ttle_depo.grid(row=8, column=0, padx=(5,5), pady=(5,5))
        self.counter_pd = Spinbox(self)
        self.counter_pd.grid(row=9, column=0, padx=(5,5), pady=(5,5))

class win_new_project(CTk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.protocol('WM_DELETE_WINDOW', self._done)

        self.nazvanie_proekta = CTk.CTkLabel(master=self, text='Введите название проекта')
        self.nazvanie_proekta.grid(row=0, column=1, padx=(5,5), pady=(5,5))
        self.n_p = CTk.CTkEntry(master=self)
        self.n_p.grid(row=1, column=1, padx=(5,5), pady=(5,5))

        self.objects = CTk.CTkLabel(master=self, text="Выберите объекты строительства")
        self.objects.grid(row=2, column=0, padx=(0,0), pady=(0,0))
        self.ob_win = Object_str(self)
        self.ob_win.grid(row=3, column=0, padx=(0,0), pady=(0,0))

        self.stat_proj = CTk.CTkLabel(master=self, text="Выберите статьи по проекту")
        self.stat_proj.grid(row=2, column=1, padx=(0,0), pady=(0,0))        
        #Окно общих статей

        self.fin_organisation = CTk.CTkLabel(master=self, text="Выберите финансовые/кредитные организации")
        self.fin_organisation.grid(row=2, column=2, padx=(0,0), pady=(0,0)) 

        self.next_win = CTk.CTkButton(master=self, text="Все параметры выбраны")
        self.next_win.grid(row=3, column=1, padx=(0,0), pady=(0,0))
        #Дописать команду перехода на другое окно

    def _done(self):
        self.destroy()
        os.system('main.py')
        sys.exit(0)

