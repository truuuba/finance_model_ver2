from connect_db import sql
from spinbox import Spinbox
import re
from tkinter import messagebox as mb
from win_fin_org import *

'''
Необходимо понять в каком виде стоит добавлять данные в базу
При наличии структуры добавить данные в БД
'''

class Object_str(CTk.CTkScrollableFrame):
    def __init__(self, master, obj):
        super().__init__(master, width=250, height=450)
        self.ttle_korp = CTk.CTkLabel(master=self, text="Выберите количество корпусов")
        self.ttle_korp.grid(row=0, column=0, padx=(5,5), pady=(5,5))
        self.counter_k = Spinbox(self)
        self.counter_k.grid(row=1, column=0, padx=(5,5), pady=(5,5))
        obj.append(self.counter_k)

        self.ttle_sosh = CTk.CTkLabel(master=self, text="Выберите количество СОШ")
        self.ttle_sosh.grid(row=2, column=0, padx=(5,5), pady=(5,5))
        self.counter_sosh = Spinbox(self)
        self.counter_sosh.grid(row=3, column=0, padx=(5,5), pady=(5,5))
        obj.append(self.counter_sosh)

        self.ttle_sosh = CTk.CTkLabel(master=self, text="Выберите количество ДОУ")
        self.ttle_sosh.grid(row=4, column=0, padx=(5,5), pady=(5,5))
        self.counter_dou = Spinbox(self)
        self.counter_dou.grid(row=5, column=0, padx=(5,5), pady=(5,5))
        obj.append(self.counter_dou)

        self.ttle_med = CTk.CTkLabel(master=self, text="Выберите количество медучреждений")
        self.ttle_med.grid(row=6, column=0, padx=(5,5), pady=(5,5))
        self.counter_med = Spinbox(self)
        self.counter_med.grid(row=7, column=0, padx=(5,5), pady=(5,5))
        obj.append(self.counter_med)

        self.ttle_depo = CTk.CTkLabel(master=self, text="Выберите количество Пождепо")
        self.ttle_depo.grid(row=8, column=0, padx=(5,5), pady=(5,5))
        self.counter_pd = Spinbox(self)
        self.counter_pd.grid(row=9, column=0, padx=(5,5), pady=(5,5))
        obj.append(self.counter_pd)

class Stati(CTk.CTkScrollableFrame):
    def __init__(self, master, stat):
        super().__init__(master, width=650, height=450)
        self.ttle = CTk.CTkLabel(master=self, text="Выберите общие статьи по всему проекту")
        self.ttle.grid(row=0, column=0, padx=(5,5), pady=(5,5))

        cnt = 1
        arr = sql.take_list_st_2()
        for el in arr:
            self.nazv = CTk.CTkLabel(master=self, text=(el.code + " " + el.nazv))
            self.nazv.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            arr2 = sql.take_list_st_3(el.id_)
            for el2 in arr2:
                self.nazv2 = CTk.CTkCheckBox(master=self, text=(el2.code + " " + el2.nazv))
                self.nazv2.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
                stat.append(self.nazv2)
                cnt += 1

class win_new_project(CTk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.protocol('WM_DELETE_WINDOW', self._done)

        self.stat = []
        self.obj = []

        self.nazvanie_proekta = CTk.CTkLabel(master=self, text='Введите название проекта')
        self.nazvanie_proekta.grid(row=0, column=1, padx=(5,5), pady=(5,5))
        self.n_p = CTk.CTkEntry(master=self)
        self.n_p.grid(row=1, column=1, padx=(5,5), pady=(5,5))

        self.objects = CTk.CTkLabel(master=self, text="Выберите объекты строительства")
        self.objects.grid(row=2, column=0, padx=(5,5), pady=(15,5))
        self.ob_win = Object_str(self, self.obj)
        self.ob_win.grid(row=3, column=0, padx=(5,5), pady=(5,5))

        self.stat_proj = CTk.CTkLabel(master=self, text="Выберите статьи по проекту")
        self.stat_proj.grid(row=2, column=1, padx=(5,5), pady=(15,5))        
        self.obsh_st = Stati(self, self.stat)
        self.obsh_st.grid(row=3, column=1, padx=(5,5), pady=(5,5)) 

        self.next_win = CTk.CTkButton(master=self, text="Все параметры выбраны", command=self.next_win_f)
        self.next_win.grid(row=4, column=1, padx=(5,5), pady=(15,5))

    def _done(self):
        self.destroy()
        os.system('main.py')
        sys.exit(0)

    def next_win_f(self):
        prov = True
        nazv_p = self.n_p.get()
        match_nazv = re.match(r'^[А-Яа-яЁё]+$', nazv_p)
        if not(match_nazv):
            mb.showerror("Ошибка!", "Некорректно введено название проекта")
            prov = False
        
        list_stat = []
        for el in self.stat:
            if el.get():
                list_stat.append(el.cget("text"))
        if len(list_stat) == 0:
            mb.showerror("Ошибка!", "Не выбраны статьи проекта")
            prov = False
        
        list_cnt = []
        for el in self.obj:
            list_cnt.append(el.get())
        if sum(list_cnt) == 0:
            mb.showerror("Ошибка!", "Не выбраны объекты")
            prov = False

        if prov:
            self.withdraw()
            a = win_fin_organisation()
            a.mainloop()
