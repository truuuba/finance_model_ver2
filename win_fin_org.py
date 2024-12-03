import customtkinter as CTk
from connect_db import sql
import re
from tkinter import messagebox as mb

CTk.set_appearance_mode("dark")
CTk.set_default_color_theme("green")

class input_stati_fin(CTk.CTkFrame):
    def __init__(self, master, arr_org, arr_stat, org, stat, mnt, yr, ds):
        super().__init__(master, width=1000, height=450)
        #Организация
        self.ttle_org = CTk.CTkLabel(master=self, text="Организация")
        self.ttle_org.grid(row=0, column=0, padx=(5,5), pady=(5,5))
        self.orgs = CTk.CTkComboBox(master=self, values=arr_org)
        self.orgs.grid(row=1, column=0, padx=(5,5), pady=(5,5))
        org = self.orgs

        #Выбор статьи
        self.ttle_stat = CTk.CTkLabel(master=self, text="Выберите статью")
        self.ttle_stat.grid(row=0, column=1, padx=(5,5), pady=(5,5))
        self.stats = CTk.CTkComboBox(master=self, values=arr_stat)
        self.stats.grid(row=1, column=1, padx=(5,5), pady=(5,5))
        stat = self.stats

        #Ввод месяца
        self.take_mounth = CTk.CTkLabel(master=self, text="Выберите месяц")
        self.take_mounth.grid(row=0, column=2, padx=(5,5), pady=(5,5))
        self.take_mnt = CTk.CTkComboBox(master=self, values=["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"])
        self.take_mnt.grid(row=1, column=2, padx=(5,5), pady=(5,5))
        mnt = self.take_mnt

        #Ввод года
        self.take_year = CTk.CTkLabel(master=self, text="Введите год")
        self.take_year.grid(row=0, column=3, padx=(5,5), pady=(5,5))
        self.take_yr = CTk.CTkEntry(master=self)
        self.take_yr.grid(row=1, column=3, padx=(5,5), pady=(5,5))
        yr = self.take_yr

        #Ввод ДС
        self.take_money = CTk.CTkLabel(master=self, text="Введите денежные средства")
        self.take_money.grid(row=0, column=4, padx=(5,5), pady=(5,5))
        self.money = CTk.CTkEntry(master=self)
        self.money.grid(row=1, column=4, padx=(5,5), padx=(5,5))
        ds = self.money

class win_fin_org(CTk.CTk):
    def __init__(self, id_p):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.id_p = id_p
        #финансовые организации
        self._arr_org = sql.take_nazv_fin_org(self.id_p)
        if len(self._arr_org) == 0:
            self._arr_org = ["Организации отсутствуют"]
        #статьи
        arr_stat = []
        _arr_stat = sql.take_st_for_finorg()
        for el in _arr_stat:
            arr_stat.append(el.code + " " + el.nazv)
        #данные по вводу статей
        self.org = None
        self.stat = None
        self.mnt = None
        self.yr = None
        self.ds = None

        self.ttle = CTk.CTkLabel(master=self, text="Добавление новой финансовой организации", bg_color="#E63946")
        self.ttle.grid(row=0, column=0, padx=(5,5), pady=(5,5))

        self.entry_organis = CTk.CTkLabel(master=self, text="Название организации")
        self.entry_organis.grid(row=1, column=0, padx=(5,5), pady=(5,5))
        self.entr_org = CTk.CTkEntry(master=self)
        self.entr_org.grid(row=2, column=0, padx=(5,5), pady=(5,5))
        self.but_input_org = CTk.CTkButton(master=self, text="Добавить организацию", command=self.input_fin_org)
        self.but_input_org.grid(row=3, column=0, padx=(5,5), pady=(5,5))

        self.ttle2 = CTk.CTkLabel(master=self, text="Введите данные по статьям", bg_color="#E63946")
        self.ttle2.grid(row=4, column=0, padx=(5,5), pady=(5,5))
        self.win_input_st = input_stati_fin(self, self._arr_org, arr_stat, self.org, self.stat, self.mnt, self.yr, self.ds)
        self.win_input_st.grid(row=5, column=0, padx=(5,5), pady=(5,5))
        self.but_input_st = CTk.CTkButton(master=self, text="Ввод данных")
        self.but_input_st.grid(row=6, column=0, padx=(5,5), pady=(5,5))

    def input_fin_org(self):
        pattern = r"^(?=.*[A-Za-zА-Яа-я])[\wА-Яа-я]+$"
        match_org = re.match(pattern, self.entr_org.get())
        if match_org:
            prov_nazv = True
            #Проверка наличия такого же названия
            for el in self._arr_org:
                if self.entr_org.get() == el:
                    prov_nazv = False
            #ввод фин.организации
            if prov_nazv:
                sql.input_fin_org(self.id_p, self.entr_org.get())
            else:
                mb.showerror("Ошибка!", "Такая организация уже существует")
        else:
            mb.showerror("Ошибка!", "Неверно введено название")

    def input_stati_fin(self):
        pattern = r"^\d+$"
        prov = True
        year = re.match(pattern, self.yr.get())
        if not year:
            prov = False
            mb.showerror("Ошибка!", "Неверно введено значение года")
        ds = re.match(pattern, self.ds.get())
        if not ds:
            prov = False
            mb.showerror("Ошибка", "Неверно введено количество денежных средств")
        m = self.org.get()
        if m == "Организации отсутствуют":
            prov = False
            mb.showerror("Ошибка!", "Не выбрана организация")
        if prov:
            #вытаскиваем статью
            z = self.stat.get()
            z = z.split()
            id_st_4 = sql.take_st4_of_code(z[0])
            #вытаскиваем фин.организацию
            id_f_org = sql.take_nazv_finorg(self.id_p, m)
            #Добавляем статью 
            sql.input_stati_finorg(id_f_org, id_st_4, self.mnt.get(), self.yr.get(), self.ds.get())
            mb.showinfo("Успешно!", "Данные были успешно внесены")
