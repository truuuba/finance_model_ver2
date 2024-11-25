from win_bdr3 import *

class win_for_trati_obj(CTk.CTkScrollableFrame):
    def __init__(self, master, objects_, entry_bdr_stati, id_bdr_st):
        super().__init__(master, width=1000, height=550)
        cnt = 0
        for el in objects_:
            self.ttle_obj = CTk.CTkLabel(master=self, text=el.nazv, bg_color="#E63946")
            self.ttle_obj.grid(row=cnt, column=1, padx=(5,5), pady=(5,5))
            cnt += 1
            stati_obj = sql.stati_obj_str(el.id_) #статьи по объекту
            idishniki = []
            checkbox = []
            for elem in stati_obj:
                per = sql.take_st_3(elem.id_st_3) #название по статье объекта
                self.ttle_n_st = CTk.CTkLabel(master=self, text=(per.code + " " + per.nazv))
                self.ttle_n_st.grid(row=cnt, column=1, padx=(5,5), pady=(5,5))
                cnt += 1
                bdr_st = sql.take_data_BDR_obj(elem.id_) #статьи по БДР
                for i in range(len(bdr_st)):
                    self.dates = CTk.CTkLabel(master=self, text=(bdr_st[i].mnt + " " + str(bdr_st[i].yr)))
                    self.dates.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
                    self.entry_ds = CTk.CTkEntry(master=self)
                    self.entry_ds.grid(row=cnt, column=2, padx=(5,5), pady=(5,5))
                    cnt += 1
                    idishniki.append(bdr_st[i].id_)
                    checkbox.append(self.entry_ds)
            entry_bdr_stati.append(checkbox)
            id_bdr_st.append(idishniki)

class win_bdr2(CTk.CTk):
    def __init__(self, id_p):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.id_p = id_p
        self.objects = sql.obj_str_gpr(self.id_p)
        self.entry_bdr_stati = []
        self.id_bdr_st = []

        ttle = CTk.CTkLabel(master=self, text="Введите предполагаемые затраты статей по месяцам для каждого объекта")
        ttle.grid(row=0, column=0, padx=(5,5), pady=(5,5))

        win_trt = win_for_trati_obj(self, self.objects, self.entry_bdr_stati, self.id_bdr_st)
        win_trt.grid(row=1, column=0, padx=(5,5), pady=(5,5))

        self.but_next = CTk.CTkButton(master=self, text="Обновить данные", command=self.next_win)
        self.but_next.grid(row=2, column=0, padx=(5,5), pady=(5,5))

        if sql.found_zapisi_GPR_obj(self.id_p):
            self.but_next2 = CTk.CTkButton(master=self, text="Использовать существующие данные", command=self.next_win2)
            self.but_next2.grid(row=3, column=0, padx=(5,5), pady=(5,5))

    def next_win2(self):
        self.withdraw()
        a = win_bdr3(id_p=self.id_p)
        a.mainloop()

    def next_win(self):
        prov = True
        patt = r"^[0-9]+$"
        for el in self.entry_bdr_stati:
            for elem in el:
                match_ds = re.match(patt, elem.get())
                if not match_ds:
                    prov = False
        if prov:
            for i in range(len(self.entry_bdr_stati)):
                for j in range(len(self.entry_bdr_stati[i])):
                    sql.update_bdr_obj(id_=self.id_bdr_st[i][j], plan_ds=self.entry_bdr_stati[i][j].get())
            self.withdraw()
            a = win_bdr3(id_p=self.id_p)
            a.mainloop()
        else:
            mb.showerror('Ошибка!', 'Неверно введены данные!')
