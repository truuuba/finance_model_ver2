import customtkinter as CTk
import os
import sys

CTk.set_appearance_mode("dark")
CTk.set_default_color_theme("green")

class win_for_gpr(CTk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.protocol('WM_DELETE_WINDOW', self._done)

        self.make_gpr = CTk.CTkLabel(master=self, text="Создание ГПР")
        self.make_gpr.grid(row=0, column=0, padx=(5,5), pady=(5,5))


    def _done(self):
        self.destroy()
        os.system('main.py')
        sys.exit(0)