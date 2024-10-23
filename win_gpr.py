from win_for_obj import *

class GPR_obsh(CTk.CTkScrollableFrame):
    def __init__(self, master, entry_prod, entry_zavis, params_r):
        super().__init__(master, width=1100, height=500)
        self.w = CTk.CTkLabel(master=self, text="Параметры работ")
        self.w.grid(row=0, column=0, padx=(5,5), pady=(5,5))
        self.pr = CTk.CTkLabel(master=self, text="Продолжительность работ в месяцах")
        self.pr.grid(row=0, column=1, padx=(5,5), pady=(5,5))
        self.zav = CTk.CTkLabel(master=self, text="Зависимости от процессов (пишите номера процессов через пробел)")
        self.zav.grid(row=0, column=2, padx=(5,5), pady=(5,5))
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
        self.params_r = sql.take_obsh_stati(id_p)

        self.make_gpr = CTk.CTkLabel(master=self, text="Создание ГПР по общим статьям")
        self.make_gpr.grid(row=0, column=0, padx=(5,5), pady=(5,5))

        self.ttle = CTk.CTkLabel(master=self, text="Введите продолжительность и зависимоти по общим статьям")
        self.ttle.grid(row=1, column=0, padx=(5,5), pady=(5,5))
        self.win_gpr = GPR_obsh(self, self.entry_prod, self.entry_zavis, self.params_r)
        self.win_gpr.grid(row=2, column=0, padx=(5,5), pady=(5,5))

        self.but_next = CTk.CTkButton(master=self, text="Данные введены", command=self.next_win)
        self.but_next.grid(row=3, column=0, padx=(5,5), pady=(5,5))

    def _done(self):
        self.destroy()
        os.system('main.py')
        sys.exit(0)

    def next_win(self):
        prov = True
        list_zav = []
        for el in self.entry_zavis:
            txt_zav = self.del_probel(el.get())
            if txt_zav == None:
                txt_zav = ""
            match_zav = re.match(r'^[0-9 ]*$', txt_zav)
            if not(match_zav):
                prov = False
            elif txt_zav == "":
                list_zav.append("0")
            else:
                list_zav.append(txt_zav)
                
        for el in self.entry_prod:
            cnt = el.get()
            if (cnt == None) or (cnt == 0):
                prov = False

        if prov:
            #добавление данных в БД
            for i in range(len(self.params_r)):
                sql.input_gpr_obsh(id_st_obsh=self.params_r[i].id_, zavisim=list_zav[i], prod=self.entry_prod[i].get())
            #Открытие следующего окна 
            self.withdraw()
            a = win_for_obj(id_p=self.id_p)
            a.mainloop()
        else:
            mb.showerror("Ошибка!", "Не для всех статей выбраны параметры")

    def del_probel(self, nm):
        n = len(nm)
        for j in range(n-1, 0, -1):
            if nm[j] == " ":
                nm = nm[:-1]
            else:
                return nm
