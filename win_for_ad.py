import customtkinter as CTk
import re
from tkinter import messagebox as mb
from connect_db import sql

CTk.set_appearance_mode("dark")
CTk.set_default_color_theme("green")

class win_for_ad(CTk.CTk):
    def __init__(self, id_c):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.id_c = id_c

        self.tit = CTk.CTkLabel(master=self, text="Выберите опцию")
        self.tit.grid(row=0, column=1, padx=(0,0), pady=(0,0))

        self.add_us = CTk.CTkLabel(master=self, text="Добавление пользователя")
        self.add_us.grid(row=1, column=0, padx=(0,0), pady=(0,0))
        self.familiya = CTk.CTkLabel(master=self, text="Фамилия")
        self.familiya.grid(row=2, column=0, padx=(0,0), pady=(0,0))
        self.fam = CTk.CTkEntry(master=self)
        self.fam.grid(row=3, column=0, padx=(0, 0), pady=(0,0))
        
        self.imya = CTk.CTkLabel(master=self, text="Имя")
        self.imya.grid(row=4, column=0, padx=(0, 0), pady=(0,0))
        self.im = CTk.CTkEntry(master=self)
        self.im.grid(row=5, column=0, padx=(0, 0), pady=(0,0))

        self.otchetstvo = CTk.CTkLabel(master=self, text="Отчество")
        self.otchetstvo.grid(row=6, column=0, padx=(0, 0), pady=(0,0))
        self.otch = CTk.CTkEntry(master=self)
        self.otch.grid(row=7, column=0, padx=(0, 0), pady=(0,0))
        
        self.login = CTk.CTkLabel(master=self, text="Логин")
        self.login.grid(row=8, column=0, padx=(0, 0), pady=(0,0))
        self.log = CTk.CTkEntry(master=self)
        self.log.grid(row=9, column=0, padx=(0, 0), pady=(0,0))
        
        self.password = CTk.CTkLabel(master=self, text="Пароль")
        self.password.grid(row=10, column=0, padx=(0, 0), pady=(0,0))
        self.pas = CTk.CTkEntry(master=self, show="*")
        self.pas.grid(row=11, column=0, padx=(0, 0), pady=(0,0))
        
        self.add_user = CTk.CTkButton(master=self, text="Добавить", command=self.add_user)
        self.add_user.grid(row=12, column=0, padx=(10, 10), pady=(10, 10))

        self.del_proekt = CTk.CTkLabel(master=self, text="Удаление проекта")
        self.del_proekt.grid(row=1, column=2, padx=(0,0), pady=(0,0))
        arr = self.make_arr_nazv_pr()
        self.projects = CTk.CTkComboBox(master=self, values=arr)
        self.projects.grid(row=2, column=2, padx=(0, 0), pady=(0, 0))
        self.del_pr = CTk.CTkButton(master=self, text="Удалить", command=self.delete_proekt)
        self.del_pr.grid(row=3, column=2, padx=(10, 10), pady=(10, 10))

        self.del_user = CTk.CTkLabel(master=self, text="Удаление пользователя")
        self.del_user.grid(row=4, column=2, padx=(0,0), pady=(0,0))
        arr2 = self.make_arr_users()
        self.users = CTk.CTkComboBox(master=self, values=arr2)
        self.users.grid(row=5, column=2, padx=(0,0), pady=(0,0))
        self.del_us = CTk.CTkButton(master=self, text="Удалить", command=self.delete_user)
        self.del_us.grid(row=6, column=2, padx=(10, 10), pady=(10, 10))

    def add_user(self):
        fam = self.fam.get()
        im = self.im.get()
        otch = self.otch.get()
        log = self.log.get()
        pas = self.pas.get()

        match_fam = re.match(r'^[А-Яа-яЁё]+$', fam)
        match_im = re.match(r'^[А-Яа-яЁё]+$', im)
        match_otch = re.match(r'^[А-Яа-яЁё]*$', otch)
        match_log = re.match(r'^[a-zA-Z0-9!@#\$%\^&\*\(\)_\+\-=\[\]\{\};:,<>\.\?\/\\|`~\s]+$', log)
        match_pas = re.match(r'^[a-zA-Z0-9!@#\$%\^&\*\(\)_\+\-=\[\]\{\};:,<>\.\?\/\\|`~\s]+$', pas)

        if not(match_fam):
            mb.showerror("Ошибка!", "Некорректно введена фамилия")
        elif not(match_im):
            mb.showerror("Ошибка!", "Некорректно введено имя")
        elif not(match_otch):
            mb.showerror("Ошибка!", "Некорректно введено отчество")
        elif not(match_log):
            mb.showerror("Ошибка!", "Некорректно введен логин")
        elif not(match_pas):
            mb.showerror("Ошибка!", "Некорректно введен пароль")
        else:
            arr_logs = sql.take_worker(self.id_c)
            prov = True
            for i in range(len(arr_logs)):
                if arr_logs[i].log_ == log:
                    mb.showerror("Ошибка!", "Логин уже занят")
                    prov = False
            if prov:
                sql.input_empl(self.id_c, fam, im, otch, log, pas)
                mb.showinfo('Успешно!', 'Вы добавили пользователя в систему!')
                self.fam.delete(first_index=0, last_index=len(fam))
                self.im.delete(first_index=0, last_index=len(im))
                self.otch.delete(first_index=0, last_index=len(otch))
                self.log.delete(first_index=0, last_index=len(log))
                self.pas.delete(first_index=0, last_index=len(pas))

    def make_arr_nazv_pr(self):
        arr = sql.take_project(self.id_c)
        if len(arr) >= 1:
            return arr
        else:
            arr = ['Проекты отсутствуют']
            return arr
        
    def make_arr_users(self):
        arr = sql.take_list_users(self.id_c)
        if len(arr) == 0:
            arr = ['Пользователи отсутствуют']
        return arr

    def delete_proekt(self):
        if self.projects.get() == 'Проекты отсутствуют':
            mb.showerror('Ошибка!', 'Проекты не найдены')
        #Дописать, когда появится структура!!!
        '''else:
            result = mb.askyesno(title="Подтверждение изменений", message="Вы действительно хотите безвозвратно удалить проект?")
            if result:
                id_comp = sql.found_ind_company(combobox[0].get())
                nazv_ = self.projects.get()
                sql.del_project(id_comp, nazv_)
                mb.showinfo('Успешно!', 'Вы удалили проект!')'''

    def delete_user(self):
        result = mb.askyesno(title="Подтверждение изменений", message="Вы действительно хотите безвозвратно удалить пользователя?")
        if result:
            log_us = self.users.get()
            sql.del_user(Id_c=self.id_c, log_=log_us)
            mb.showinfo('Успешно!', 'Вы удалили пользователя!')

combobox = []