import customtkinter as CTk
from connect_db import sql

CTk.set_appearance_mode("dark")
CTk.set_default_color_theme("green")

class BDDS_win(CTk.CTkScrollableFrame):
    def __init__(self, master, stati):
        super().__init__(master, width=1000, height=250, orientation='horizontal')
        #Создаем массив по 4 уровню
        arr = []
        for i in range(len(stati)):
            elem = sql.take_st_ur_4(stati[i].id_o)
            for el in elem:
                arr.append(el.code + " " + el.nazv) #Потом можно сплитануть строку по пробелу и с нулевого индекса вытащить код статьи (через него и осуществлять потом поиск в БД айдишника)

        #Выбор статьи
        self.ttle_stat = CTk.CTkLabel(master=self, text="Выберите статью")
        self.ttle_stat.grid(row=0, column=0, padx=(5,5), pady=(5,5)) 
        self.ttle_st = CTk.CTkComboBox(master=self, values=arr)                            
        self.ttle_st.grid(row=1, column=0, padx=(5,5), pady=(5,5))

        #Выбор месяца
        self.ttle_mounth = CTk.CTkLabel(master=self, text="Выберите месяц")
        self.ttle_mounth.grid(row=0, column=1, padx=(5,5), pady=(5,5))
        self.ttle_mnt = CTk.CTkComboBox(master=self, values=["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"])
        self.ttle_mnt.grid(row=1, column=1, padx=(5,5), pady=(5,5))

        #Выбор года работ
        self.ttle_year = CTk.CTkLabel(master=self, text="Введите год")
        self.ttle_year.grid(row=0, column=2, padx=(5,5), pady=(5,5))
        self.ttle_yr = CTk.CTkEntry(master=self)
        self.ttle_yr.grid(row=1, column=2, padx=(5,5), pady=(5,5))

        #Ввод ДС
        self.ttle_ds_ = CTk.CTkLabel(master=self, text="Введите количество ДС")
        self.ttle_ds_.grid(row=0, column=3, padx=(5,5), pady=(5,5))
        self.ttle_ds = CTk.CTkEntry(master=self)
        self.ttle_ds.grid(row=1, column=3, padx=(5,5), pady=(5,5))

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

        self.ttle = CTk.CTkLabel(master=self, text="Выберите параметр для ввода данных в БДДС")
        self.ttle.grid(row=0, column=0, padx=(5,5), pady=(5,5))

        self.choice_obj = CTk.CTkComboBox(master=self, values=arr)
        self.choice_obj.grid(row=1, column=0, padx=(5,5), pady=(5,5))

        self.but_next = CTk.CTkButton(master=self, text="Параметр выбраны", command=self.open_data)
        self.but_next.grid(row=2, column=0, padx=(5,5), pady=(5,5))


    def open_data(self):
        nazvanie = self.choice_obj.get()
        self.ttle_st = CTk.CTkLabel(master=self, text="Введите информацию в БДДС")
        self.ttle_st.grid(row=3, column=0, padx=(5,5), pady=(5,5))

        if nazvanie == 'Общие статьи':
            stati = sql._take_obsh_stati_(id_p=self.id_p)
        else:
            id_obj = sql.found_id_obj(nazv=nazvanie, id_p=self.id_p)
            stati = sql.found_obj_str_stati_(id_obj)
        self.win_BDDS = BDDS_win(self, stati=stati)
        self.win_BDDS.grid(row=4, column=0, padx=(5,5), pady=(5,5))

        self.but_input = CTk.CTkButton(master=self, text="Данные введены")
        self.but_input.grid(row=5, column=0, padx=(5,5), pady=(5,5))