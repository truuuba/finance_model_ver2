import customtkinter as CTk
import os
import sys
from spinbox import Spinbox
from connect_db import sql

CTk.set_appearance_mode("dark")
CTk.set_default_color_theme("green")

class GPR_obj(CTk.CTkScrollableFrame):
    def __init__(self, master, objects, prod, zav):
        super().__init__(master, width=1100, height=500)
        for el in objects:
            self.ttle_obj = CTk.CTkLabel(master=self, text=("Объект: " + el.nazv), bg_color="#E63946")
            self.ttle_obj.grid(row=0, column=1, padx=(5,5), pady=(5,5))
            self.w = CTk.CTkLabel(master=self, text="Параметры работ")
            self.w.grid(row=1, column=0, padx=(5,5), pady=(5,5))
            self.pr = CTk.CTkLabel(master=self, text="Продолжительность работ в месяцах")
            self.pr.grid(row=1, column=1, padx=(5,5), pady=(5,5))
            self.zav = CTk.CTkLabel(master=self, text="Зависимости от процессов (пишите номера процессов через пробел)")
            self.zav.grid(row=1, column=2, padx=(5,5), pady=(5,5))
            params_r = sql.take_obj_stati(id_obj=el.id_)
            n = len(params_r)
            entry_prod = []
            entry_zavis = []
            for i in range(n):
                data_st = sql.take_st_3(params_r[i].id_o)
                self.work = CTk.CTkLabel(master=self, text=(data_st.code + " " + data_st.nazv))
                self.work.grid(row=i+2, column=0, padx=(5,5), pady=(5,5))
                self.prodolj = Spinbox(self)
                self.prodolj.grid(row=i+2, column=1, padx=(5,5), pady=(5,5))
                entry_prod.append(self.prodolj)
                self.zavis = CTk.CTkEntry(master=self)
                self.zavis.grid(row=i+2, column=2, padx=(5,5), pady=(5,5))
                entry_zavis.append(self.zavis)
            prod.append(entry_prod)
            zav.append(entry_zavis)

class win_for_obj_gpr(CTk.CTk):
    def __init__(self, id_p):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.protocol('WM_DELETE_WINDOW', self._done)
        self.id_p = id_p
        self.objects = sql.take_obj_str(id_p=self.id_p)
        self.prod = []
        self.zav = []

        self.ttle = CTk.CTkLabel(master=self, text="Введите данные для ГПР по объектам")
        self.ttle.grid(row=0, column=0, padx=(5,5), pady=(5,5))
        self.win_gpr = GPR_obj(self, self.objects, self.prod, self.zav)
        self.win_gpr.grid(row=1, column=0, padx=(5,5), pady=(5,5))

    def next_win(self):
        #Проверка данных
        for i in range(len(self.objects)):
            #Проверка продолжительностей i-того проекта
            for j in range(len(self.prod[i])):
                ...
            #Проверка зависимостей i-того проекта
            for j in range(len(self.zav[i])):
                ...
            

    def _done(self):
        self.destroy()
        os.system('main.py')
        sys.exit(0)

