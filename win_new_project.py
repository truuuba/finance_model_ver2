from spinbox import Spinbox
import re
from win_upload_org import *

'''
Необходимо понять в каком виде стоит добавлять данные в базу
При наличии структуры добавить данные в БД
'''

class Object_str(CTk.CTkScrollableFrame):
    def __init__(self, master, obj):
        super().__init__(master, width=400, height=350)
        self.ttle_korp = CTk.CTkLabel(master=self, text="Выберите количество корпусов")
        self.ttle_korp.grid(row=0, padx=(5,5), pady=(5,5))
        self.counter_k = Spinbox(self)
        self.counter_k.grid(row=1, padx=(5,5), pady=(5,5))
        obj.append(self.counter_k)

        self.ttle_sosh = CTk.CTkLabel(master=self, text="Выберите количество СОШ")
        self.ttle_sosh.grid(row=2, padx=(5,5), pady=(5,5))
        self.counter_sosh = Spinbox(self)
        self.counter_sosh.grid(row=3, padx=(5,5), pady=(5,5))
        obj.append(self.counter_sosh)

        self.ttle_sosh = CTk.CTkLabel(master=self, text="Выберите количество ДОУ")
        self.ttle_sosh.grid(row=4, padx=(5,5), pady=(5,5))
        self.counter_dou = Spinbox(self)
        self.counter_dou.grid(row=5, padx=(5,5), pady=(5,5))
        obj.append(self.counter_dou)

        self.ttle_med = CTk.CTkLabel(master=self, text="Выберите количество медучреждений")
        self.ttle_med.grid(row=6, padx=(5,5), pady=(5,5))
        self.counter_med = Spinbox(self)
        self.counter_med.grid(row=7, padx=(5,5), pady=(5,5))
        obj.append(self.counter_med)

        self.ttle_depo = CTk.CTkLabel(master=self, text="Выберите количество Пождепо")
        self.ttle_depo.grid(row=8, padx=(5,5), pady=(5,5))
        self.counter_pd = Spinbox(self)
        self.counter_pd.grid(row=9, padx=(5,5), pady=(5,5))
        obj.append(self.counter_pd)

class win_new_project(CTk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.protocol('WM_DELETE_WINDOW', self._done)
        self.obj = []

        self.ttle = CTk.CTkLabel(master=self, text="Введите данные по объектам и организациям")
        self.ttle.grid(row=0, column=0, padx=(5,5), pady=(15,5))

        self.objects = CTk.CTkLabel(master=self, text="Выберите объекты строительства")
        self.objects.grid(row=1, column=0, padx=(5,5), pady=(15,5))
        self.ob_win = Object_str(self, self.obj)
        self.ob_win.grid(row=2, column=0, padx=(5,5), pady=(5,5))      

        self.next_win = CTk.CTkButton(master=self, text="Все параметры выбраны", command=self.next_win_f)
        self.next_win.grid(row=3, column=0, padx=(5,5), pady=(15,5))

    def _done(self):
        self.destroy()
        os.system('main.py')
        sys.exit(0)

    def next_win_f(self):
        prov = True        
        list_cnt = []
        for el in self.obj:
            list_cnt.append(el.get())
        if sum(list_cnt) == 0:
            mb.showerror("Ошибка!", "Не выбраны объекты")
            prov = False

        if prov:
            self.withdraw()
            a = win_upload_org(cnt_k=list_cnt[0], cnt_s=list_cnt[1], cnt_d=list_cnt[2], cnt_med=list_cnt[3], cnt_p=list_cnt[4])
            a.mainloop()

