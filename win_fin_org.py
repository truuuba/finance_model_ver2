import customtkinter as CTk

CTk.set_appearance_mode("dark")
CTk.set_default_color_theme("green")

class input_stati_fin(CTk.CTkFrame):
    def __init__(self, master, arr_org, arr_stat):
        super().__init__(master, width=1000, height=450)
        #Организация
        self.ttle_org = CTk.CTkLabel(master=self, text="Организация")
        self.ttle_org.grid(row=0, column=0, padx=(5,5), pady=(5,5))
        self.orgs = CTk.CTkComboBox(master=self, values=arr_org)
        self.orgs.grid(row=1, column=0, padx=(5,5), pady=(5,5))

        #Выбор статьи
        self.ttle_stat = CTk.CTkLabel(master=self, text="Выберите статью")
        self.ttle_stat.grid(row=0, column=1, padx=(5,5), pady=(5,5))
        self.stats = CTk.CTkComboBox(master=self, values=arr_stat)
        self.stats.grid(row=1, column=1, padx=(5,5), pady=(5,5))

        #Ввод месяца
        self.take_mounth = CTk.CTkLabel(master=self, text="Выберите месяц")
        self.take_mounth.grid(row=0, column=2, padx=(5,5), pady=(5,5))
        self.take_mnt = CTk.CTkComboBox(master=self, values=["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"])
        self.take_mnt.grid(row=0, column=2, padx=(5,5), pady=(5,5))

        #Ввод года
        self.take_year = CTk.CTkLabel(master=self, text="Введите год")
        self.take_year.grid(row=0, column=3, padx=(5,5), pady=(5,5))
        self.take_yr = CTk.CTkEntry(master=self)
        self.take_yr.grid(row=0, column=3, padx=(5,5), pady=(5,5))

        #Ввод ДС
        self.take_money = CTk.CTkLabel(master=self, text="Введите денежные средства")
        self.take_money.grid(row=0, column=4, padx=(5,5), pady=(5,5))
        self.money = CTk.CTkEntry(master=self)
        self.money.grid(row=0, column=4, padx=(5,5), padx=(5,5))

class win_fin_org(CTk.CTk):
    def __init__(self, id_p):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.id_p = id_p
        #финансовые организации
        _arr_org = []
        #статьи
        _arr_stat = []

        self.ttle = CTk.CTkLabel(master=self, text="Добавление новой финансовой организации", bg_color="#E63946")
        self.ttle.grid(row=0, column=0, padx=(5,5), pady=(5,5))

        self.entry_organis = CTk.CTkLabel(master=self, text="Название организации")
        self.entry_organis.grid(row=1, column=0, padx=(5,5), pady=(5,5))
        self.entr_org = CTk.CTkEntry(master=self)
        self.entr_org.grid(row=2, column=0, padx=(5,5), pady=(5,5))
        self.but_input_org = CTk.CTkButton(master=self, text="Добавить организацию")
        self.but_input_org.grid(row=3, column=0, padx=(5,5), pady=(5,5))

        self.ttle2 = CTk.CTkLabel(master=self, text="Введите данные по статьям", bg_color="#E63946")
        self.ttle2.grid(row=4, column=0, padx=(5,5), pady=(5,5))
        self.win_input_st = input_stati_fin(self)
        self.win_input_st.grid(row=5, column=0, padx=(5,5), pady=(5,5))
        self.but_input_st = CTk.CTkButton(master=self, text="Ввод данных")
        self.but_input_st.grid(row=6, column=0, padx=(5,5), pady=(5,5))


