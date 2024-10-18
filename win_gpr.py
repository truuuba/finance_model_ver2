import customtkinter as CTk
from spinbox import Spinbox
import os
import sys
from connect_db import sql
import re
from tkinter import messagebox as mb

CTk.set_appearance_mode("dark")
CTk.set_default_color_theme("green")

class GPR_obsh(CTk.CTkScrollableFrame):
    def __init__(self, master, id_p, entry_prod, entry_zavis, params_r):
        super().__init__(master, width=1100, height=500)
        self.w = CTk.CTkLabel(master=self, text="Параметры работ")
        self.w.grid(row=0, column=0, padx=(5,5), pady=(5,5))
        self.pr = CTk.CTkLabel(master=self, text="Продолжительность работ в месяцах")
        self.pr.grid(row=0, column=1, padx=(5,5), pady=(5,5))
        self.zav = CTk.CTkLabel(master=self, text="Зависимости от процессов (пишите номера процессов через пробел)")
        self.zav.grid(row=0, column=2, padx=(5,5), pady=(5,5))
        params_r = sql.take_obsh_stati(id_p)
        n = len(params_r)
        for i in range(n):
            data_st = sql.take_st_3(params_r[i].id_o)
            self.work = CTk.CTkLabel(master=self, text=(data_st.code + " " + data_st.nazv))
            self.work.grid(row=i+1, column=0, padx=(5,5), pady=(5,5))
            self.prodolj = Spinbox(self)
            self.prodolj.grid(row=i+1, column=1, padx=(5,5), pady=(5,5))
            entry_prod.append(self.prodolj)
            self.zavis = CTk.CTkEntry(master=self)
            self.zavis.grid(row=i+1, column=2, padx=(5,5), pady=(5,5))
            entry_zavis.append(self.zavis)

class win_for_gpr(CTk.CTk):
    def __init__(self, id_p):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.protocol('WM_DELETE_WINDOW', self._done)
        self.id_p = id_p
        self.entry_prod = []
        self.entry_zavis = []
        self.params_r = []

        self.make_gpr = CTk.CTkLabel(master=self, text="Создание ГПР по общим статьям")
        self.make_gpr.grid(row=0, column=0, padx=(5,5), pady=(5,5))

        self.ttle = CTk.CTkLabel(master=self, text="Введите продолжительность и зависимоти по общим статьям")
        self.ttle.grid(row=1, column=0, padx=(5,5), pady=(5,5))
        self.win_gpr = GPR_obsh(self, self.id_p, self.entry_prod, self.entry_zavis)
        self.win_gpr.grid(row=2, column=0, padx=(5,5), pady=(5,5))

        self.but_next = CTk.CTkButton(master=self, text="Данные введены")
        self.but_next.grid(row=3, column=0, padx=(5,5), pady=(5,5))

    def _done(self):
        self.destroy()
        os.system('main.py')
        sys.exit(0)

    def next_win(self):
        prov = True
        for el in self.entry_zavis:
            txt_zav = el.get()
            match_nazv = re.match(r'^[0-9 ]*$', txt_zav)
            if not(match_nazv):
                prov = False
        for el in self.entry_prod:
            cnt = el.get()
            if (cnt == None) or (cnt == 0):
                prov = False

        if prov:
            #добавление данных в БД
            for i in range(len(self.params_r)):
                sql.input_gpr_obsh(id_st_obsh=)

            mb.showinfo('ура', 'работает')
            #Открытие следующего окна 
        else:
            mb.showerror("Ошибка!", "Не для всех объектов выбраны статьи расходов")
