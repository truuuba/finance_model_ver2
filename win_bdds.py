import customtkinter as CTk
from connect_db import sql
import re
from tkinter import messagebox as mb

CTk.set_appearance_mode("dark")
CTk.set_default_color_theme("green")

class BDDS_win(CTk.CTkFrame):
    def __init__(self, master, _list_, prov_obj):
        super().__init__(master, width=1000, height=250)
        arr = []
        #Создаем массив по статьям
        if prov_obj:
            mass_obj = sql.append_obj_4st()
            for i in range(len(mass_obj)):
                arr.append(mass_obj[i].code + " " + mass_obj[i].nazv)
        else:
            mass_obsh = sql.append_obsh_4st()
            for i in range(len(mass_obsh)):
                arr.append(mass_obsh[i].code + " " + mass_obsh[i].nazv)

        #Выбор статьи
        self.ttle_stat = CTk.CTkLabel(master=self, text="Выберите статью")
        self.ttle_stat.grid(row=0, column=0, padx=(5,5), pady=(5,5)) 
        self.ttle_st = CTk.CTkComboBox(master=self, values=arr)                            
        self.ttle_st.grid(row=1, column=0, padx=(5,5), pady=(5,5))
        _list_.append(self.ttle_st)

        #Выбор месяца
        self.ttle_mounth = CTk.CTkLabel(master=self, text="Выберите месяц")
        self.ttle_mounth.grid(row=0, column=1, padx=(5,5), pady=(5,5))
        self.ttle_mnt = CTk.CTkComboBox(master=self, values=["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"])
        self.ttle_mnt.grid(row=1, column=1, padx=(5,5), pady=(5,5))
        _list_.append(self.ttle_mnt)

        #Выбор года работ
        self.ttle_year = CTk.CTkLabel(master=self, text="Введите год")
        self.ttle_year.grid(row=0, column=2, padx=(5,5), pady=(5,5))
        self.ttle_yr = CTk.CTkEntry(master=self)
        self.ttle_yr.grid(row=1, column=2, padx=(5,5), pady=(5,5))
        _list_.append(self.ttle_yr)

        #Ввод ДС
        self.ttle_ds_ = CTk.CTkLabel(master=self, text="Введите количество ДС")
        self.ttle_ds_.grid(row=0, column=3, padx=(5,5), pady=(5,5))
        self.ttle_ds = CTk.CTkEntry(master=self)
        self.ttle_ds.grid(row=1, column=3, padx=(5,5), pady=(5,5))
        _list_.append(self.ttle_ds)

class win_bdds(CTk.CTk):
    def __init__(self, id_p):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.id_p = id_p
        #Данные по объектам строения
        arr = ['Общие статьи']
        n = sql.take_obj_str(id_p=self.id_p)
        for i in range(len(n)):
            arr.append(n[i].nazv)
        self._list_ = []

        self.ttle = CTk.CTkLabel(master=self, text="Выберите параметр для ввода данных в БДДС")
        self.ttle.grid(row=0, column=0, padx=(5,5), pady=(5,5))

        self.choice_obj = CTk.CTkComboBox(master=self, values=arr)
        self.choice_obj.grid(row=1, column=0, padx=(5,5), pady=(5,5))

        self.but_next = CTk.CTkButton(master=self, text="Параметр выбраны", command=self.open_data)
        self.but_next.grid(row=2, column=0, padx=(5,5), pady=(5,5))

    def open_data(self):
        self._list_ = []
        self.nazvanie = self.choice_obj.get()
        self.ttle_st = CTk.CTkLabel(master=self, text="Введите информацию в БДДС")
        self.ttle_st.grid(row=3, column=0, padx=(5,5), pady=(5,5))
        prov_obj = False

        if not(self.nazvanie == 'Общие статьи'):
            self.id_obj = sql.found_id_obj(nazv=self.nazvanie, id_p=self.id_p)
            prov_obj = True
        self.win_BDDS = BDDS_win(self, _list_=self._list_, prov_obj=prov_obj)
        self.win_BDDS.grid(row=4, column=0, padx=(5,5), pady=(5,5))

        self.but_input = CTk.CTkButton(master=self, text="Данные введены", command=self.input_data_bdds)
        self.but_input.grid(row=5, column=0, padx=(5,5), pady=(5,5))

    def input_data_bdds(self):
        #Сначала надо проверить вводимые параметры
        pattern = r"^[0-9]+$"
        match_yr = re.match(pattern, self._list_[2].get())
        match_ds = re.match(pattern, self._list_[3].get())
        if not match_yr:
            mb.showerror("Ошибка!", "Некорректно введено значение года")
        elif not match_ds:
            mb.showerror("Ошибка!", "Некорректно введено значение денежных средств")
        else:
            #Ввод по общим статьям
            z = self._list_[0].get()
            z = z.split()
            #Поиск айдишника уровня статей
            id_st4 = sql.take_st4_of_code(z[0])
            #Вводим данные в БДДС
            if self.nazvanie == 'Общие статьи':
                sql.input_data_BDDS_obsh(self.id_p, id_st4, self._list_[2].get(), self._list_[1].get(), self._list_[3].get())
            else:
                sql.input_data_BDDS_obj(self.id_obj, id_st4, self._list_[2].get(), self._list_[1].get(), self._list_[3].get())
            mb.showinfo("Успешно!", "Данные были успешно добавлены")

                
