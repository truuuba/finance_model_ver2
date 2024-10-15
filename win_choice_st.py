from win_new_project import *

class Stati(CTk.CTkScrollableFrame):
    def __init__(self, master, stat):
        super().__init__(master, width=900, height=350)
        self.ttle = CTk.CTkLabel(master=self, text="Выберите общие статьи по всему проекту")
        self.ttle.grid(row=0, column=0, padx=(5,5), pady=(5,5))

        cnt = 1
        arr = sql.take_list_st_2()
        for el in arr:
            self.nazv = CTk.CTkLabel(master=self, text=(el.code + " " + el.nazv))
            self.nazv.grid(row=cnt, column=0, padx=(5,5), pady=(15,15))
            cnt += 1
            arr2 = sql.take_list_st_3(el.id_)
            for el2 in arr2:
                self.nazv2 = CTk.CTkCheckBox(master=self, text=(el2.code + " " + el2.nazv))
                self.nazv2.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
                stat.append(self.nazv2)
                cnt += 1

class win_choice_stati(CTk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.protocol('WM_DELETE_WINDOW', self._done)
        self.stat = []

        self.nazvanie_proekta = CTk.CTkLabel(master=self, text='Введите название проекта')
        self.nazvanie_proekta.grid(row=0, column=0, padx=(5,5), pady=(5,5))
        self.n_p = CTk.CTkEntry(master=self)
        self.n_p.grid(row=1, column=0, padx=(5,5), pady=(5,5))

        self.ttle_yr = CTk.CTkLabel(master=self, text="Введите год начала строительства")
        self.ttle_yr.grid(row=2, column=0, padx=(5,5), pady=(5,5))
        self.en_yr = CTk.CTkEntry(master=self)
        self.en_yr.grid(row=3, column=0, padx=(5,5), pady=(5,5))

        self.ttle_mnt = CTk.CTkLabel(master=self, text="Введите месяц начала строительства")
        self.ttle_mnt.grid(row=4, column=0, padx=(5,5), pady=(5,5))
        self.en_mnt = CTk.CTkComboBox(master=self, values=["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"])
        self.en_mnt.grid(row=5, column=0, padx=(5,5), pady=(5,5))

        self.ttle = CTk.CTkLabel(master=self, text="Добавление статей по всему проекту")
        self.ttle.grid(row=6, column=0, padx=(5,5), pady=(5,5))

        self.win_stati = Stati(self, self.stat)
        self.win_stati.grid(row=7, column=0, padx=(5,5), pady=(5,5))

        self.button_add = CTk.CTkButton(master=self, text="Добавление статей", command=self.change_win)
        self.button_add.grid(row=8, column=0, padx=(5,5), pady=(5,5))

    def _done(self):
        self.destroy()
        os.system('main.py')
        sys.exit(0)

    def change_win(self):
        prov = True
        nazv_p = self.n_p.get()
        match_nazv = re.match(r'^[А-Яа-яЁё]+$', nazv_p)
        if not(match_nazv):
            mb.showerror("Ошибка!", "Некорректно введено название проекта")
            prov = False

        yr_start = self.en_yr.get()
        match_yr = re.match(r'^[0-9]+$', yr_start)
        if not(match_yr):
            mb.showerror("Ошибка!", "Некорректно введен год проекта")
            prov = False

        list_stat = []
        for el in self.stat:
            if el.get():
                list_stat.append(el.cget("text"))
        if len(list_stat) == 0:
            mb.showerror("Ошибка!", "Не выбраны статьи проекта")
            prov = False
        if prov:
            self.withdraw()
            a = win_new_project()
            a.mainloop()