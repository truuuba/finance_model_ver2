from win_choice_table import *

class GPR_obj(CTk.CTkScrollableFrame):
    def __init__(self, master, objects, prod, zav):
        super().__init__(master, width=1100, height=500)
        cnt = 0
        for el in objects:
            print(el.nazv)
            self.ttle_obj = CTk.CTkLabel(master=self, text=("Объект: " + el.nazv), bg_color="#E63946")
            self.ttle_obj.grid(row=cnt, column=1, padx=(5,5), pady=(15,15))
            cnt += 1
            self.w = CTk.CTkLabel(master=self, text="Параметры работ")
            self.w.grid(row=cnt, column=0, padx=(5,5), pady=(3,3))
            self.pr = CTk.CTkLabel(master=self, text="Продолжительность работ в месяцах")
            self.pr.grid(row=cnt, column=1, padx=(5,5), pady=(3,3))
            self.zav = CTk.CTkLabel(master=self, text="Зависимости от процессов (пишите номера процессов через пробел)")
            self.zav.grid(row=cnt, column=2, padx=(5,5), pady=(3,3))
            cnt += 1
            params_r = sql.take_obj_stati(id_obj=el.id_)
            n = len(params_r)
            entry_prod = []
            entry_zavis = []
            for i in range(n):
                data_st = sql.take_st_3(params_r[i].id_o)
                self.work = CTk.CTkLabel(master=self, text=(data_st.code + " " + data_st.nazv))
                self.work.grid(row=cnt, column=0, padx=(5,5), pady=(3,3))
                self.prodolj = Spinbox(self)
                self.prodolj.grid(row=cnt, column=1, padx=(5,5), pady=(3,3))
                entry_prod.append(self.prodolj)
                self.zavis = CTk.CTkEntry(master=self)
                self.zavis.grid(row=cnt, column=2, padx=(5,5), pady=(3,3))
                cnt += 1
                entry_zavis.append(self.zavis)
            prod.append(entry_prod)
            zav.append(entry_zavis)

class win_for_obj_gpr(CTk.CTk):
    def __init__(self, id_p):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.protocol('WM_DELETE_WINDOW', self._done)
        self.id_p = id_p
        self.objects = sql.take_obj_str(id_p=self.id_p)
        self.prod = []
        self.zav = []

        self.ttle = CTk.CTkLabel(master=self, text="Введите данные для ГПР по объектам")
        self.ttle.grid(row=0, column=0, padx=(5,5), pady=(5,5))
        self.win_gpr = GPR_obj(self, self.objects, self.prod, self.zav)
        self.win_gpr.grid(row=1, column=0, padx=(5,5), pady=(5,5))

        self.but_next = CTk.CTkButton(master=self, text="Данные введены", command=self.next_win)
        self.but_next.grid(row=2, column=0, padx=(5,5), pady=(5,5))

    def next_win(self):
        prov = True
        arr_zav = []
        arr_prod =[]
        #Проверка данных
        for i in range(len(self.objects)):
            list_zav = []
            list_prod = []
            #Проверка продолжительностей i-того объекта
            for j in range(len(self.prod[i])):
                cnt = self.prod[i][j].get()
                if (cnt == None) or (cnt == 0):
                    prov = False
                    break
                list_prod.append(cnt)
            #Проверка зависимостей i-того объекта
            for j in range(len(self.zav[i])):
                txt_zav = self.zav[i][j].get()
                if txt_zav == None:
                    txt_zav = ""
                match_zav = re.match(r'^[0-9 ]*$', txt_zav)
                if not(match_zav):
                    prov = False
                    break
                elif txt_zav == "":
                    list_zav.append("0")
                else:
                    list_zav.append(txt_zav)
            arr_zav.append(list_zav)
            arr_prod.append(list_prod)

        if prov:
            for i in range(len(self.objects)):
                for j in range(len(arr_zav[i])):
                    sql.input_gpr_obj(id_st_obj=self.objects[i].id_, zavisim=arr_zav[i][j], prod=arr_prod[i][j])
            self.withdraw()
            a = choice_table(self.id_p)
            a.mainloop()
        else:
            mb.showerror('Ошибка!', 'Некорректно записаны данные')
                
    def _done(self):
        self.destroy()
        os.system('main.py')
        sys.exit(0)


