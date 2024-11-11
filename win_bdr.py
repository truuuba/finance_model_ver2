import customtkinter as CTk
from connect_db import sql

CTk.set_appearance_mode("dark")
CTk.set_default_color_theme("green")

class win_for_trati(CTk.CTkScrollableFrame):
    def __init__(self, master, bdr_stati, entry_bdr_stati):
        super().__init__(master, width=1150, height=400)
        txt = ""
        cnt = 0
        for i in range(len(bdr_stati)):
            elem = sql.take_nazv_BDR(bdr_stati[i].id_)
            if txt != elem.nazv:
                self.ttle_label = CTk.CTkLabel(master=self, text=(elem.code + " " + elem.nazv))
                self.ttle_label.grid(row=cnt, column=1, padx=(5,5), pady=(5,5))
                cnt += 1
            txt = elem.nazv
            self.ttle_date = CTk.CTkLabel(master=self, text=(bdr_stati[i].mnt + " " + bdr_stati[i].yr))
            self.ttle_date.grid(row=cnt, column=0, padx=(5,5), pady=(5,5))
            self.entry_date = CTk.CTkEntry(master=self)
            self.entry_date.grid(row=cnt, column=2, padx=(5,5), pady=(5,5))
            entry_bdr_stati.append(self.entry_date)
            cnt += 1


class win_bdr(CTk.CTk):
    def __init__(self, id_p):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.id_p = id_p
        self.obsh_stati = sql.take_obsh_stati(self.id_p) #данные всех общих статей 
        self.bdr_stati = []
        for el in self.obsh_stati:
            l = sql.take_data_BDR_obsh(el.id_)
            self.bdr_stati.append(l)
        self.entry_bdr_stati = [] #массив с чекбоксами

        self.ttle = CTk.CTkLabel(master=self, text="Введите предполагаемые затраты статей по месяцам")
        self.ttle.grid(row=0, column=0, padx=(5,5), pady=(5,5))
        self.win_input_bdr = win_for_trati(self, self.bdr_stati, self.entry_bdr_stati)
        self.win_input_bdr.grid(row=1, column=0, padx=(5,5), pady=(5,5))



