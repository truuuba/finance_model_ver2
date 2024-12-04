import customtkinter as CTk
import re
from tkinter import messagebox as mb
from make_bdr import * 
from connect_db import sql
from make_ppo import *

CTk.set_appearance_mode("dark")
CTk.set_default_color_theme("green")

class win_for_trati_obj(CTk.CTkScrollableFrame):
    def __init__(self, master, obsh_st, entr_st):
        super().__init__(master, width=1000, height=550)
        cnt = 0
        for el in obsh_st:
            st_3 = sql.take_st_3(el.id_o)
            self.ttle_st = CTk.CTkLabel(master=self, text=(st_3.code + " " + st_3.nazv))
            self.ttle_st.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            self.ent_st = CTk.CTkEntry(master=self)
            self.ent_st.grid(row=cnt, column=1, padx=(5,5), pady=(5,5))
            entr_st.append(self.ent_st)
            cnt += 1

class win_bdr3(CTk.CTk):
    def __init__(self, id_p):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.id_p = id_p
        self.obsh_st = sql.take_stati_iskl(self.id_p)
        self.entr_st = []

        self.ttle = CTk.CTkLabel(master=self, text="Введите предполагаемые расходы по статьям проекта")
        self.ttle.grid(row=0, column=0, padx=(5,5), pady=(5,5))

        win_st = win_for_trati_obj(self, self.obsh_st, self.entr_st)
        win_st.grid(row=1, column=0, padx=(5,5), pady=(5,5))

        self.btn_change = CTk.CTkButton(master=self, text="Данные введены - создать БДР", command=self.input_data)
        self.btn_change.grid(row=2, column=0, padx=(5,5), pady=(5,5))

        if sql.prov_BDR_iskl(id_p=self.id_p):
            self.but_next2 = CTk.CTkButton(master=self, text="Использовать существующие данные - создать БДР", command=self.make_bdr)
            self.but_next2.grid(row=3, column=0, padx=(5,5), pady=(5,5))

    def input_data(self):
        prov = True
        patt = r"^[0-9]+$"
        for el in self.entr_st:
            match_ds = re.match(patt, el.get())
            if not match_ds:
                prov = False
        if prov:
            if sql.prov_BDR_iskl(id_p=self.id_p):
                sql.upd_BDR_iskl(obsh_st=self.obsh_st)
            for i in range(len(self.entr_st)):
                sql.input_BDR_iskl(id_st=self.obsh_st[i].id_, ds=self.entr_st[i].get()) # добавить update
            mb.showinfo("Успешно!", "Таблица БДР создана")
        else:
            mb.showerror("Ошибка!", "Введены неверные значения")

    def make_bdr(self):
        create_tabel_ppo(id_pr=self.id_p, prov_create=False)
        create_tabel_bdr(self.id_p)
        mb.showinfo("Успешно!", "Таблица БДР была успешно создана")
