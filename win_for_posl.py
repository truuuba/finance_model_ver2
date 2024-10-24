from win_for_obj_gpr import *

class win_zavisim(CTk.CTkScrollableFrame):
    def __init__(self, master, list_obj, list_posl):
        super().__init__(master, width=600, height=500)
        cnt = 0
        for el in list_obj:
            self.ttle_obj = CTk.CTkLabel(master=self, text=("Этап для " + el.nazv))
            self.ttle_obj.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            self.etap = CTk.CTkEntry(master=self)
            self.etap.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            cnt += 1
            list_posl.append(self.etap)

class win_for_posl(CTk.CTk):
    def __init__(self, id_p):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.protocol('WM_DELETE_WINDOW', self._done)
        self.id_p = id_p
        self.list_obj = sql.take_obj_str(id_p)
        self.list_posl = []

        self.ttle = CTk.CTkLabel(master=self, text="Введите этапы постройки")
        self.ttle.grid(row=0, column=0, padx=(5,5), pady=(5,5))
        self.window_z = win_zavisim(self, self.list_obj, self.list_posl)
        self.window_z.grid(row=1, column=0, padx=(5,5), pady=(5,5))
        self.prim = CTk.CTkLabel(master=self, text="Под этапом строительтва подразумевается порядок постройки, этап может включать несколько объектов")
        self.prim.grid(row=2, column=0, padx=(5,5), pady=(5,5))
        self.but_win = CTk.CTkButton(master=self, text="Данные введены", command=self.change_win)
        self.but_win.grid(row=3, column=0, padx=(5,5), pady=(5,5))

    def change_win(self):
        patt = r"^[0-9]+$"
        prov = True
        for el in self.list_posl:
            match_posl = re.match(patt, el.get())
            if not(match_posl):
                prov = False
                mb.showerror("Ошибка!", "Некорректно записаны этапы постройки")
        
        if prov:
            for i in range(len(self.list_obj)):
                sql.input_posl_in_obj(id_=self.list_obj[i].id_, posl_str=self.list_posl[i].get())
            self.withdraw()
            a = win_for_obj_gpr(id_p=self.id_p)
            a.mainloop()

    def _done(self):
        self.destroy()
        os.system('main.py')
        sys.exit(0)
