from win_choice_table import *

class sostav:
    def __init__(self, id_, id_obj, cnt, stoim):
        self.id_ = id_
        self.id_obj = id_obj
        self.cnt = cnt
        self.stoim = stoim

class kommer:
    def __init__(self, id_, id_obj, prod_pl, stoim_kv, cnt_kvart, sr_pl_r, dol_ipoteka, dol_rassr_pl, d_full_oplata, p_vs_r):
        self.id_ = id_
        self.id_obj = id_obj
        self.prod_pl = prod_pl
        self.stoim_kv = stoim_kv
        self.cnt_kvart = cnt_kvart
        self.sr_pl_r = sr_pl_r
        self.dol_ipoteka = dol_ipoteka
        self.dol_rassr_pl = dol_rassr_pl
        self.d_full_oplata = d_full_oplata
        self.p_vs_r = p_vs_r        

class win_input_sost(CTk.CTkScrollableFrame):
    def __init__(self, master, arr_sost_obj, arr_mashinomest, arr_kladov, arr_komm):
        super().__init__(master, width=1000, height=550)
        cnt = 0
        patt_m = r".*Машиноместа.*"
        patt_klad = r".*Кладовые помещения.*"
        for el in arr_sost_obj:
            nazv_obj = sql.take_nazv_obj_str(el.id_obj)
            self.ttle = CTk.CTkLabel(master=self, text=(nazv_obj + " " + el.nazv))
            self.ttle.grid(row=cnt, column=1, padx=(5,5), pady=(5,5))
            cnt += 1
            #Машиноместа
            if re.match(patt_m, el.nazv):
                self.counter_m = CTk.CTkLabel(master=self, text="Количество машиномест")
                self.counter_m.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
                self.entry_cnt_m = CTk.CTkEntry(master=self)
                self.entry_cnt_m.grid(row=cnt, column=2, padx=(5,5), pady=(5,5))
                cnt += 1
                self.stoim_m = CTk.CTkLabel(master=self, text="Стоимость машиноместа")
                self.stoim_m.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
                self.entr_st_m = CTk.CTkEntry(master=self)
                self.entr_st_m.grid(row=cnt, column=2, padx=(5,5), pady=(5,5))
                cnt += 1
                el = sostav(el.id_, el.id_obj, self.entry_cnt_m, self.entr_st_m)
                arr_mashinomest.append(el)
            #Кладовки
            elif re.match(patt_klad, el.nazv):
                self.counter_kl = CTk.CTkLabel(master=self, text="Количество кладовых")
                self.counter_kl.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
                self.entry_cnt_kl = CTk.CTkEntry(master=self)
                self.entry_cnt_kl.grid(row=cnt, column=2, padx=(5,5), pady=(5,5))
                cnt += 1
                self.stoim_kl = CTk.CTkLabel(master=self, text="Стоимость кладовой")
                self.stoim_kl.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
                self.entr_st_kl = CTk.CTkEntry(master=self)
                self.entr_st_kl.grid(row=cnt, column=2, padx=(5,5), pady=(5,5))
                cnt += 1
                el = sostav(el.id_, el.id_obj, self.entry_cnt_kl, self.entr_st_kl)
                arr_kladov.append(el)
            #Коммерческие помещения
            else:
                self.prod_pl = CTk.CTkLabel(master=self, text="Продаваемая площадь, в кв/м")
                self.prod_pl.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
                self.pr_pl = CTk.CTkEntry(master=self)
                self.pr_pl.grid(row=cnt, column=2, padx=(5,5), pady=(5,5))
                cnt += 1
                self.stoim_kv_m = CTk.CTkLabel(master=self, text="Цена за квадратный метр, в рублях")
                self.stoim_kv_m.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
                self.stoim = CTk.CTkEntry(master=self)
                self.stoim.grid(row=cnt, column=2, padx=(5,5), pady=(5,5))
                cnt += 1
                self.cnt_kvart = CTk.CTkLabel(master=self, text="Количество помещений")
                self.cnt_kvart.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
                self.cnt_kv = CTk.CTkEntry(master=self)
                self.cnt_kv.grid(row=cnt, column=2, padx=(5,5), pady=(5,5))
                cnt += 1
                self.sr_platej_rassr = CTk.CTkLabel(master=self, text="Средний ежемесячный платеж по рассрочке (в тысячах рублях)")
                self.sr_platej_rassr.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
                self.sr_pl_r = CTk.CTkEntry(master=self)
                self.sr_pl_r.grid(row=cnt, column=2, padx=(5,5), pady=(5,5))
                cnt += 1
                self.dol_ipoteka = CTk.CTkLabel(master=self, text="Доля договоров по ипотеке (в процентах)")
                self.dol_ipoteka.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
                self.d_ip = CTk.CTkEntry(master=self)
                self.d_ip.grid(row=cnt, column=2, padx=(5,5), pady=(5,5))
                cnt += 1
                self.dol_rassr_pl = CTk.CTkLabel(master=self, text="Доля договоров с рассрочкой платежа (в процентах)")
                self.dol_rassr_pl.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
                self.d_rass_pl = CTk.CTkEntry(master=self)
                self.d_rass_pl.grid(row=cnt, column=2, padx=(5,5), pady=(5,5))
                cnt += 1
                self.d_full_oplata = CTk.CTkLabel(master=self, text="Доля договоров по полной предоплате (в процентах)")
                self.d_full_oplata.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
                self.d_f_opl = CTk.CTkEntry(master=self)
                self.d_f_opl.grid(row=cnt, column=2, padx=(5,5), pady=(5,5))
                cnt += 1
                self.perv_vsnos_rassr = CTk.CTkLabel(master=self, text="Первоначальный взнос по рассрочке (в процентах)")
                self.perv_vsnos_rassr.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
                self.p_vs_r = CTk.CTkEntry(master=self)
                self.p_vs_r.grid(row=cnt, column=2, padx=(5,5), pady=(5,5))
                cnt += 1
                el = kommer(el.id_, el.id_obj, self.pr_pl, self.stoim, self.cnt_kv, self.sr_pl_r, self.d_ip, self.d_rass_pl, self.d_f_opl, self.p_vs_r)
                arr_komm.append(el)

class win_sost_obj_ppo(CTk.CTk):
    def __init__(self, id_p):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.protocol('WM_DELETE_WINDOW', self._done)
        self.id_p = id_p
        self.arr_sost_obj = sql.take_sost_obj(self.id_p)
        self.arr_mashinomest = []
        self.arr_kladov = []
        self.arr_komm = []

        self.ttle = CTk.CTkLabel(master=self, text="Введите данные по составляющим корпусов")
        self.ttle.grid(row=0, column=0, padx=(5,5), pady=(5,5))
        self.win_input_sost = win_input_sost(self, self.arr_sost_obj, self.arr_mashinomest,  self.arr_kladov, self.arr_komm)
        self.win_input_sost.grid(row=1, column=0, padx=(5,5), pady=(5,5))
        self.next_win = CTk.CTkButton(master=self, text="Данные введены", command=self.open_next_win)
        self.next_win.grid(row=2, column=0, padx=(5,5), pady=(5,5))

    def _done(self):
        self.destroy()
        os.system('main.py')
        sys.exit(0)

    def open_next_win(self):
        prov = True
        patt = r'^[0-9]*$'
        #Проверяем машиноместа
        for el in self.arr_mashinomest:
            match_cnt = re.match(patt, el.cnt.get())
            match_stoim = re.match(patt, el.stoim.get())
            if not(match_cnt and match_stoim):
                prov = False
        #Проверяем кладовые
        for el in self.arr_kladov:
            match_cnt = re.match(patt, el.cnt.get())
            match_stoim = re.match(patt, el.stoim.get())
            if not(match_cnt and match_stoim):
                prov = False
        #Проверяем коммерческие помещения
        for el in self.arr_komm:
            match_pr_pl = re.match(patt, el.prod_pl.get())
            match_stoim = re.match(patt, el.stoim_kv.get())
            match_cnt_kv = re.match(patt, el.cnt_kvart.get())
            match_sr_pl_r = re.match(patt, el.sr_pl_r.get())
            match_dol_ipoteka = re.match(patt, el.dol_ipoteka.get())
            match_dol_rassr_pl = re.match(patt, el.dol_rassr_pl.get()) 
            match_d_full_oplata = re.match(patt, el.d_full_oplata.get())
            match_p_vs_r = re.match(patt, el.p_vs_r.get())
            if not(match_pr_pl and match_stoim and match_cnt_kv and match_sr_pl_r and match_dol_ipoteka and match_dol_rassr_pl and match_d_full_oplata and match_p_vs_r):
                prov = False
        #Добавляем данные в состаявляющие строительства
        if prov:
            for el in self.arr_mashinomest:
                sql.input_sost_obj_m_k(id_=el.id_, cnt=el.cnt.get(), stoim=el.stoim.get())
            for el in self.arr_kladov:
                sql.input_sost_obj_m_k(id_=el.id_, cnt=el.cnt.get(), stoim=el.stoim.get())
            for el in self.arr_komm:
                sql.input_sost_komm_pom(id_=el.id_, cnt=el.cnt_kvart.get(), stoim=el.stoim_kv.get(), prod_pl=el.prod_pl.get(), sr_pl_rassr=el.sr_pl_r.get(), dol_ip=el.dol_ipoteka.get(), dol_rass=el.dol_rassr_pl.get(), full_pl=el.d_full_oplata.get(), vsn_r=el.p_vs_r.get())
            self.withdraw()
            a = choice_table(self.id_p)
            a.mainloop()
        else:
            mb.showerror("Ошибка!", "Введены неверные данные")
