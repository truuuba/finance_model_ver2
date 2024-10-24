import customtkinter as CTk
import os
import sys
from spinbox import Spinbox
from connect_db import sql
import re
from tkinter import messagebox as mb

CTk.set_appearance_mode("dark")
CTk.set_default_color_theme("green")

class choice_table(CTk.CTk):
    def __init__(self, id_p):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.protocol('WM_DELETE_WINDOW', self._done)
        self.id_p = id_p

        #ГПР
        self.gpr = CTk.CTkLabel(master=self, text="Таблица графика производственных работ")
        self.gpr.grid(row=0, column=0, padx=(5,5), pady=(5,5))
        self.gpr_ex = CTk.CTkButton(master=self, text="Создать таблицу ГПР в Excel")
        self.gpr_ex.grid(row=1, column=0, padx=(5,5), pady=(5,5))

        #ППО
        self.ppo = CTk.CTkLabel(master=self, text="Таблица ППО")
        self.ppo.grid(row=2, column=0, padx=(5,5), pady=(5,5))
        self.ppo_ex = CTk.CTkButton(master=self, text="Создать таблицу ППО в Excel")
        self.ppo_ex.grid(row=3, column=0, padx=(5,5), pady=(5,5))

        #БДР
        self.bdr = CTk.CTkLabel(master=self, text="Таблица БДР")
        self.bdr.grid(row=4, column=0, padx=(5,5), pady=(5,5))
        self.bdr_ex = CTk.CTkButton(master=self, text="Открыть таблицу БДР")
        self.bdr_ex.grid(row=5, column=0, padx=(5,5), pady=(5,5))

        #БДДС
        self.bdds = CTk.CTkLabel(master=self, text="Таблица БДДС")
        self.bdds.grid(row=6, column=0, padx=(5,5), pady=(5,5))
        self.bdds_ex = CTk.CTkButton(master=self, text="Создать таблицу БДДС в Excel")
        self.bdds_ex.grid(row=7, column=0, padx=(5,5), pady=(5,5))

        #Изменения в конкретных таблицах
        self.changer = CTk.CTkLabel(master=self, text="Добавить изменения в талицу")
        self.changer.grid(row=8, column=0, padx=(5,5), pady=(15,5))
        self.changer_check_box = CTk.CTkComboBox(master=self, values=["ГПР", "ППО", "БДДС"])
        self.changer_check_box.grid(row=9, column=0, padx=(5,5), pady=(5,5))
        self.changer_but = CTk.CTkButton(master=self, text="Изменить")
        self.changer_but.grid(row=10, column=0, padx=(5,5), pady=(5,5))

        #Изменения в статьях
        self.ch_st = CTk.CTkLabel(master=self, text="Изменить статьи доходов и расходов")
        self.ch_st.grid(row=11, column=0, padx=(5,5), pady=(5,5))
        self.change_stat = CTk.CTkButton(master=self, text="Изменить")
        self.change_stat.grid(row=12, column=0, padx=(5,5), pady=(5,5))

        #Изменить даты начала работ
        self.time_work = CTk.CTkLabel(master=self, text="Изменить даты продаж и строительства")
        self.time_work.grid(row=13, column=0, padx=(5,5), pady=(5,5))
        self.ch_t = CTk.CTkButton(master=self, text="Изменить")
        self.ch_t.grid(row=14, column=0, padx=(5,5), pady=(5,5))

        self.poyasn_t = CTk.CTkLabel(master=self, text="При изменении файла закрывайте его в Excel!", text_color='#EB5E28')
        self.poyasn_t.grid(row=15, column=0, padx=(5,5), pady=(5,5))

    def _done(self):
        self.destroy()
        os.system('main.py')
        sys.exit(0)
