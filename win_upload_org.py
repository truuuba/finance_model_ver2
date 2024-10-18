from win_gpr import *

'''
for_prov - массив с чекбоксами
id_obj - массив с айдишниками объектов
id_st - массив с айдишниками статей
'''

class Upload_obekt(CTk.CTkScrollableFrame):
    def __init__(self, master, list_ob_str, id_st, id_obj, for_prov):
        super().__init__(master, width=1100, height=600)
        self.for_obj_2_st = sql.take_list_obj()
        id_st.clear()
        id_obj.clear()
        for_prov.clear()
        self.tt = CTk.CTkLabel(master=self, text="Выберите статьи по каждому объекту")
        self.tt.grid(row=0, column=0, padx=(5,5), pady=(5,5))
        cnt = 1
        #Цикл по объектам строительтва
        for elem in list_ob_str:
            checkboxes = []
            self.tt_k = CTk.CTkLabel(master=self, text=("Выберите статьи по " + elem.nazv), bg_color="#E63946")
            self.tt_k.grid(row=cnt, column=0, padx=(5,5), pady=(15,15))
            cnt += 1
            #Цикл по статьям второго уровня
            for el in self.for_obj_2_st:
                self.ttle_st_2 = CTk.CTkLabel(master=self, text=(el.code + " " + el.nazv))
                self.ttle_st_2.grid(row=cnt, column=0, padx=(5,5), pady=(15,15))
                cnt += 1
                arr2 = sql.take_list_st_3(el.id_)
                #Цикл по статьям третьего уровня
                for el2 in arr2:
                    self.nazv2 = CTk.CTkCheckBox(master=self, text=(el2.code + " " + el2.nazv))
                    self.nazv2.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
                    id_st.append(el2.id_)
                    id_obj.append(elem.id_)
                    checkboxes.append(self.nazv2)
                    cnt += 1
            for_prov.append(checkboxes)        

class win_upload_org(CTk.CTk):
    def __init__(self, id_p):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.protocol('WM_DELETE_WINDOW', self._done)
        self.id_p = id_p
        self.list_ob_str = sql.take_obj_str(id_p)
        self.id_obj = []
        self.id_st = []
        self.for_prov = []

        self.ttle = CTk.CTkLabel(master=self, text="Введите данные по объектам и организациям") 
        self.ttle.grid(row=0, column=0, padx=(5,5), pady=(5,5))

        self.win_ob = Upload_obekt(self, self.list_ob_str, self.id_st, self.id_obj, self.for_prov)
        self.win_ob.grid(row=1, column=0, padx=(5,5), pady=(5,5))

        self.but_next = CTk.CTkButton(master=self, text="Данные введены", command=self.next_win)
        self.but_next.grid(row=2, column=0, padx=(5,5), pady=(5,5))

    def _done(self):
        self.destroy()
        os.system('main.py')
        sys.exit(0)

    def next_win(self):
        prov2 = True
        for el in self.for_prov:
            prov = False
            for i in range(len(el)):
                if el[i].get():
                    prov = True
            if not(prov):
                prov2 = False

        if prov2:
            #Добавляем статьи по объекту
            for i in range(len(self.id_st)):
                sql.input_st_obj(self.id_obj[i], self.id_st[i])
            self.withdraw()
            a = win_for_gpr(self.id_p)
            a.mainloop()
        else:
            mb.showerror("Ошибка!", "Не для всех объектов выбраны статьи расходов")
        

