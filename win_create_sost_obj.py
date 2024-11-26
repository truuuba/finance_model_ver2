from win_sost_obj_ppo import *

class sost:
    def __init__(self, m, klad, komm):
        self.m = m
        self.klad = klad
        self.komm = komm

class win_sost_obj(CTk.CTkScrollableFrame):
    def __init__(self, master, arr_object, sostavl):
        super().__init__(master, width=1000, height=650)
        cnt = 0
        for i in range(len(arr_object)):
            #Шапка
            self.nazvanie = CTk.CTkLabel(master=self, text=("Составляющие для " + arr_object[i].nazv))
            self.nazvanie.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            #Перечисления всего
            self.mashin = CTk.CTkCheckBox(master=self, text="Машиноместа")
            self.mashin.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            self.klad = CTk.CTkCheckBox(master=self, text="Кладовые помещения")
            self.klad.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            self.komm_pom = CTk.CTkCheckBox(master=self, text="Коммерческие помещения")
            self.komm_pom.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            el = sost(self.mashin, self.klad, self.komm_pom)
            sostavl.append(el)

class win_create_sost_obj(CTk.CTk):
    def __init__(self, id_p):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.protocol('WM_DELETE_WINDOW', self._done)
        self.id_p = id_p
        self.sostavl = []
        #Ищем корпуса из всех объектов
        self.arr_object = []
        patt = r".*Корпус.*"
        list_all_objects = sql.take_obj_str(self.id_p)
        for el in list_all_objects:
            match_obj = re.match(patt, el.nazv)
            if match_obj:
                self.arr_object.append(el)

        self.ttle = CTk.CTkLabel(master=self, text="Введите составляющие корпусов")
        self.ttle.grid(row=0, column=0, padx=(5,5), pady=(5,5))
        self.win_sost = win_sost_obj(self, self.arr_object, self.sostavl)
        self.win_sost.grid(row=1, column=0, padx=(5,5), pady=(5,5))
        self.but_next = CTk.CTkButton(master=self, text="Все параметры выбраны", command=self.next_win)
        self.but_next.grid(row=2, column=0, padx=(5,5), pady=(5,5))

    def _done(self):
        self.destroy()
        os.system('main.py')
        sys.exit(0)

    def next_win(self):
        for i in range(len(self.arr_object)):
            if self.sostavl[i].m.get():
                sql.input_sost_obj(id_obj=self.arr_object[i].id_, nazv="Машиноместа")
            if self.sostavl[i].klad.get():
                sql.input_sost_obj(id_obj=self.arr_object[i].id_, nazv="Кладовые помещения")
            if self.sostavl[i].komm.get():
                sql.input_sost_obj(id_obj=self.arr_object[i].id_, nazv="Коммерческие помещения")
        self.withdraw()
        a = win_sost_obj_ppo(self.id_p)
        a.mainloop()