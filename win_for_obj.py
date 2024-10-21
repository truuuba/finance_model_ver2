import customtkinter as CTk
import os
import sys
from connect_db import sql
import re

CTk.set_appearance_mode("dark")
CTk.set_default_color_theme("green")

class For_PPO(CTk.CTkScrollableFrame):
    def __init__(self, master, list_obj):
        super().__init__(master, width=1100, height=500)
        self.ttle = CTk.CTkLabel(master=self, text="Данные для ППО")
        self.ttle.grid(row=0, column=0, padx=(5,5), pady=(5,5))
        patt = r".*Корпус.*"
        objects_ = []
        #Проверка на тип объекта
        for el in list_obj:
            match_obj = re.match(patt, el.nazv)
            if match_obj:
                objects_.append(el)
        #Данные по каждому объекту
        cnt = 1
        for el in objects_:
            self.ttle_obj = CTk.CTkLabel(master=self, text=el.nazv, bg_color="#E63946")
            self.ttle_obj.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            self.etap_str = CTk.CTkLabel(master=self, text="Введите этап строительтва *")
            self.etap_str.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            self.et_str = CTk.CTkEntry(master=self)
            self.et_str.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            self.prod_pl = CTk.CTkLabel(master=self, text="Продаваемая площадь")
            self.prod_pl.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            self.pr_pl = CTk.CTkEntry(master=self)
            self.pr_pl.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            self.stoim_kv_m = CTk.CTkLabel(master=self, text="Цена за квадратный метр, в рублях")
            self.stoim_kv_m.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            self.stoim = CTk.CTkEntry(master=self)
            self.stoim.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            self.cnt_kvart = CTk.CTkLabel(master=self, text="Количество квартир")
            self.cnt_kvart.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            self.cnt_kv = CTk.CTkEntry(master=self)
            self.cnt_kv.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1

        self.prim = CTk.CTkLabel(master=self, text="Под этапом строительтва подразумевается порядок постройки, этап может включать несколько объектов")
        self.prim.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))

class win_for_obj(CTk.CTk):
    def __init__(self, id_p):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.protocol('WM_DELETE_WINDOW', self._done)
        self.id_p = id_p
        list_obj = sql.take_obj_str(id_p)

        self.ttle = CTk.CTkLabel(master=self, text="Введите данные по организациям")
        self.ttle.grid(row=0, column=0, padx=(5,5), pady=(5,5))

        self.win_PPO = For_PPO(self, list_obj)
        self.win_PPO.grid(row=1, column=0, padx=(5,5), pady=(5,5))

        self.but_input = CTk.CTkButton(master=self, text="Данные введены")
        self.but_input.grid(row=2, column=0, padx=(5,5), pady=(5,5))

    def next_win(self):
        

    def _done(self):
        self.destroy()
        os.system('main.py')
        sys.exit(0)