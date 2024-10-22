import customtkinter as CTk
import os
import sys
from connect_db import sql
from tkinter import messagebox as mb
import re

CTk.set_appearance_mode("dark")
CTk.set_default_color_theme("green")

class For_PPO(CTk.CTkScrollableFrame):
    def __init__(self, master, objects_, prod_pl, price, kvartiri, sr_pl_r, d_ipoteka, d_rassr, d_full_pl, vs_rassr):
        super().__init__(master, width=1100, height=500)
        self.ttle = CTk.CTkLabel(master=self, text="Данные для ППО")
        self.ttle.grid(row=0, column=0, padx=(5,5), pady=(5,5))
        #Данные по каждому объекту
        cnt = 1
        for el in objects_:
            self.ttle_obj = CTk.CTkLabel(master=self, text=el.nazv, bg_color="#E63946")
            self.ttle_obj.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            self.prod_pl = CTk.CTkLabel(master=self, text="Продаваемая площадь, в кв/м")
            self.prod_pl.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            self.pr_pl = CTk.CTkEntry(master=self)
            self.pr_pl.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            prod_pl.append(self.pr_pl)
            self.stoim_kv_m = CTk.CTkLabel(master=self, text="Цена за квадратный метр, в рублях")
            self.stoim_kv_m.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            self.stoim = CTk.CTkEntry(master=self)
            self.stoim.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            price.append(self.stoim)
            self.cnt_kvart = CTk.CTkLabel(master=self, text="Количество квартир")
            self.cnt_kvart.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            self.cnt_kv = CTk.CTkEntry(master=self)
            self.cnt_kv.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            kvartiri.append(self.cnt_kv)
            self.sr_platej_rassr = CTk.CTkLabel(master=self, text="Средний ежемесячный платеж по рассрочке (в тысячах рублях)")
            self.sr_platej_rassr.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            self.sr_pl_r = CTk.CTkEntry(master=self)
            self.sr_pl_r.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            sr_pl_r.append(self.sr_pl_r)
            self.dol_ipoteka = CTk.CTkLabel(master=self, text="Доля договоров по ипотеке (в процентах)")
            self.dol_ipoteka.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            self.d_ip = CTk.CTkEntry(master=self)
            self.d_ip.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            d_ipoteka.append(self.d_ip)
            self.dol_rassr_pl = CTk.CTkLabel(master=self, text="Доля договоров с рассрочкой платежа (в процентах)")
            self.dol_rassr_pl.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            self.d_rass_pl = CTk.CTkEntry(master=self)
            self.d_rass_pl.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            d_rassr.append(self.d_rass_pl)
            self.d_full_oplata = CTk.CTkLabel(master=self, text="Доля договоров по полной предоплате (в процентах)")
            self.d_full_oplata.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            self.d_f_opl = CTk.CTkEntry(master=self)
            self.d_f_opl.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            d_full_pl.append(self.d_f_opl)
            self.perv_vsnos_rassr = CTk.CTkLabel(master=self, text="Первоначальный взнос по рассрочке (в процентах)")
            self.perv_vsnos_rassr.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            self.p_vs_r = CTk.CTkEntry(master=self)
            self.p_vs_r.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            vs_rassr.append(self.p_vs_r)

class win_for_obj(CTk.CTk):
    def __init__(self, id_p):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.protocol('WM_DELETE_WINDOW', self._done)
        self.id_p = id_p
        list_obj = sql.take_obj_str(id_p)
        self.prod_pl = []
        self.price = []
        self.kvartiri = []
        self.sr_pl_r = []
        self.d_ipoteka = []
        self.d_rassr = []
        self.d_full_pl = []
        self.vs_rassr = []

        patt = r".*Корпус.*"
        self.objects_ = []
        #Проверка на тип объекта
        for el in list_obj:
            match_obj = re.match(patt, el.nazv)
            if match_obj:
                self.objects_.append(el)

        self.ttle = CTk.CTkLabel(master=self, text="Введите данные по организациям")
        self.ttle.grid(row=0, column=0, padx=(5,5), pady=(5,5))

        self.win_PPO = For_PPO(self, self.objects_, self.prod_pl, self.price, self.kvartiri, self.sr_pl_r, self.d_ipoteka, self.d_rassr, self.d_full_pl, self.vs_rassr)
        self.win_PPO.grid(row=1, column=0, padx=(5,5), pady=(5,5))

        self.but_input = CTk.CTkButton(master=self, text="Данные введены", command=self.next_win)
        self.but_input.grid(row=2, column=0, padx=(5,5), pady=(5,5))

    def next_win(self):
        prov = True
        patt_pr_pl_price = r"^\d+(\.\d+)?$"
        patt_kv = r"^[0-9]+$"
        for i in range(len(self.objects_)):
            match_pr_pl = re.match(patt_pr_pl_price, self.prod_pl[i].get())
            match_price = re.match(patt_pr_pl_price, self.price[i].get())
            match_kv = re.match(patt_kv, self.kvartiri[i].get())
            match_sr_pl = re.match(patt_kv, self.sr_pl_r[i].get())
            match_ipoteka = re.match(patt_kv, self.d_ipoteka[i].get())
            match_rassr = re.match(patt_kv, self.d_rassr[i].get())
            match_full_pr = re.match(patt_kv, self.d_full_pl[i].get())
            match_vs_rassr = re.match(patt_kv, self.vs_rassr[i].get())
            if not(match_pr_pl and match_price and match_kv and match_sr_pl and match_ipoteka and match_rassr and match_full_pr and match_vs_rassr):
                prov = False
                break
        
        if prov:
            for i in range(len(self.objects_)):
                sql.input_ppo_in_obj(self.objects_[i].id_, prod_pl=self.prod_pl[i].get(), stoim=self.price[i].get(), kv_cnt=self.kvartiri[i].get(), sr_pl_rassr=self.d_rassr[i].get(), dol_ipoteka=self.d_ipoteka[i].get(), dol_rassr=self.d_rassr[i].get(), dol_full_pl=self.d_full_pl[i].get(), vsnos_rassr=self.vs_rassr[i].get())
            mb.showinfo("Ура", "Работает")
        else:
            mb.showerror('Ошибка!', 'Некорректно введены данные по объектам')

    def _done(self):
        self.destroy()
        os.system('main.py')
        sys.exit(0)

'''
            self.etap_str = CTk.CTkLabel(master=self, text="Введите этап строительтва *")
            self.etap_str.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            self.et_str = CTk.CTkEntry(master=self)
            self.et_str.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1

            self.prim = CTk.CTkLabel(master=self, text="Под этапом строительтва подразумевается порядок постройки, этап может включать несколько объектов")
            self.prim.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
'''