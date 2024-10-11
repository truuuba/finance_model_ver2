import customtkinter as CTk
import os
import sys

CTk.set_appearance_mode("dark")
CTk.set_default_color_theme("green")

class FinOrg(CTk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, width=300, height=330)


class win_fin_organisation(CTk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.protocol('WM_DELETE_WINDOW', self._done)

        self.ttle = CTk.CTkLabel(master=self, text="Добавление финансовых/кредитных организаций")
        self.ttle.grid(row=0, column=0, padx=(5,5), pady=(5,5))

        


        self.button_add = CTk.CTkButton(master=self, text="Добавление организаций")
        self.button_add.grid(row=3, column=0, padx=(5,5), pady=(5,5))

    def _done(self):
        self.destroy()
        os.system('main.py')
        sys.exit(0)