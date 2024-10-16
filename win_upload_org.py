import customtkinter as CTk
import os
import sys
from tkinter import messagebox as mb
from connect_db import sql

CTk.set_appearance_mode("dark")
CTk.set_default_color_theme("green")

class Upload_obekt(CTk.CTkScrollableFrame):
    def __init__(self, master, cnt_k, cnt_s, cnt_d, cnt_med, cnt_p):
        super().__init__(master, width=1000, height=600)
        self.for_obj_2_st = sql.take_list_obj()
        self.tt = CTk.CTkLabel(master=self, text="Выберите статьи по каждому объекту")
        self.tt.grid(row=0, column=0, padx=(5,5), pady=(5,5))
        cnt = 1
        if cnt_k != 0:
            #Дописать к объектам старт строительства
            self.tt_k = CTk.CTkLabel(master=self, text="Выберите статьи по жилым корпусам", bg_color="#E63946")
            self.tt_k.grid(row=cnt, column=0, padx=(5,5), pady=(15,15))
            cnt += 1
            for el in self.for_obj_2_st:
                self.ttle_st_2 = CTk.CTkLabel(master=self, text=(el.code + " " + el.nazv))
                self.ttle_st_2.grid(row=cnt, column=0, padx=(5,5), pady=(15,15))
                cnt += 1
                arr2 = sql.take_list_st_3(el.id_)
                for el2 in arr2:
                    self.nazv2 = CTk.CTkCheckBox(master=self, text=(el2.code + " " + el2.nazv))
                    self.nazv2.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
                    cnt += 1
        for i in range(cnt_s):
            self.tt_s = CTk.CTkLabel(master=self, text=("Выберите статьи по СОШ №" + str(i+1)), bg_color="#E63946")
            self.tt_s.grid(row=cnt, column=0, padx=(5,5), pady=(15,15))
            cnt += 1
            for el in self.for_obj_2_st:
                self.ttle_st_2 = CTk.CTkLabel(master=self, text=(el.code + " " + el.nazv))
                self.ttle_st_2.grid(row=cnt, column=0, padx=(5,5), pady=(15,15))
                cnt += 1
                arr2 = sql.take_list_st_3(el.id_)
                for el2 in arr2:
                    self.nazv2 = CTk.CTkCheckBox(master=self, text=(el2.code + " " + el2.nazv))
                    self.nazv2.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
                    cnt += 1
        for i in range(cnt_d):
            self.tt_d = CTk.CTkLabel(master=self, text=("Выберите статьи по ДОУ №" + str(i+1)), bg_color="#E63946")
            self.tt_d.grid(row=cnt, column=0, padx=(5,5), pady=(15,15))
            cnt += 1
            for el in self.for_obj_2_st:
                self.ttle_st_2 = CTk.CTkLabel(master=self, text=(el.code + " " + el.nazv))
                self.ttle_st_2.grid(row=cnt, column=0, padx=(5,5), pady=(15,15))
                cnt += 1
                arr2 = sql.take_list_st_3(el.id_)
                for el2 in arr2:
                    self.nazv2 = CTk.CTkCheckBox(master=self, text=(el2.code + " " + el2.nazv))
                    self.nazv2.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
                    cnt += 1
        for i in range(cnt_med):
            self.tt_m = CTk.CTkLabel(master=self, text=("Выберите статьи по медучреждению №" + str(i+1)), bg_color="#E63946")
            self.tt_m.grid(row=cnt, column=0, padx=(5,5), pady=(15,15))
            cnt += 1
            for el in self.for_obj_2_st:
                self.ttle_st_2 = CTk.CTkLabel(master=self, text=(el.code + " " + el.nazv))
                self.ttle_st_2.grid(row=cnt, column=0, padx=(5,5), pady=(15,15))
                cnt += 1
                arr2 = sql.take_list_st_3(el.id_)
                for el2 in arr2:
                    self.nazv2 = CTk.CTkCheckBox(master=self, text=(el2.code + " " + el2.nazv))
                    self.nazv2.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
                    cnt += 1
        for i in range(cnt_p):
            self.tt_p = CTk.CTkLabel(master=self, text=("Выберите статьи по пождепо №" + str(i+1)), bg_color="#E63946")
            self.tt_p.grid(row=cnt, column=0, padx=(5,5), pady=(15,15))
            cnt += 1
            for el in self.for_obj_2_st:
                self.ttle_st_2 = CTk.CTkLabel(master=self, text=(el.code + " " + el.nazv))
                self.ttle_st_2.grid(row=cnt, column=0, padx=(5,5), pady=(15,15))
                cnt += 1
                arr2 = sql.take_list_st_3(el.id_)
                for el2 in arr2:
                    self.nazv2 = CTk.CTkCheckBox(master=self, text=(el2.code + " " + el2.nazv))
                    self.nazv2.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
                    cnt += 1

class win_upload_org(CTk.CTk):
    def __init__(self, id_p, cnt_k, cnt_s, cnt_d, cnt_med, cnt_p):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.protocol('WM_DELETE_WINDOW', self._done)
        self.id_p = id_p

        self.ttle = CTk.CTkLabel(master=self, text="Введите данные по объектам и организациям") 
        self.ttle.grid(row=0, column=0, padx=(5,5), pady=(5,5))

        self.win_ob = Upload_obekt(self, cnt_k, cnt_s, cnt_d, cnt_med, cnt_p)
        self.win_ob.grid(row=1, column=0, padx=(5,5), pady=(5,5))

        self.but_next = CTk.CTkButton(master=self, text="Данные введены")
        self.but_next.grid(row=2, column=0, padx=(5,5), pady=(5,5))

    def _done(self):
        self.destroy()
        os.system('main.py')
        sys.exit(0)

    def next_win(self):
        prov = True
        #Дописать условия по проверке выбранных статей
        if not(prov):
            self.withdraw()
            #Следующее окно
        

