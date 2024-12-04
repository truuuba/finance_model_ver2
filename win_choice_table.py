from spinbox import Spinbox
from make_gpr import *
from make_ppo import *
from win_bdr import *
from win_bdds import *
from win_fin_org import *
import sys

class choice_table(CTk.CTk):
    def __init__(self, id_p):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.protocol('WM_DELETE_WINDOW', self._done)
        self.id_p = id_p
        create_tabel_gpr(id_pr=self.id_p, prov_create=False)

        #ГПР
        self.gpr = CTk.CTkLabel(master=self, text="Таблица графика производственных работ")
        self.gpr.grid(row=0, column=0, padx=(5,5), pady=(5,5))
        self.gpr_ex = CTk.CTkButton(master=self, text="Создать таблицу ГПР в Excel", command=self.but_make_gpr)
        self.gpr_ex.grid(row=1, column=0, padx=(5,5), pady=(5,5))

        #ППО
        self.ppo = CTk.CTkLabel(master=self, text="Таблица ППО")
        self.ppo.grid(row=2, column=0, padx=(5,5), pady=(5,5))
        self.ppo_ex = CTk.CTkButton(master=self, text="Создать таблицу ППО в Excel", command=self.but_make_ppo)
        self.ppo_ex.grid(row=3, column=0, padx=(5,5), pady=(5,5))

        #БДР
        self.bdr = CTk.CTkLabel(master=self, text="Таблица БДР")
        self.bdr.grid(row=4, column=0, padx=(5,5), pady=(5,5))
        self.bdr_ex = CTk.CTkButton(master=self, text="Открыть таблицу БДР", command=self.open_win_bdr)
        self.bdr_ex.grid(row=5, column=0, padx=(5,5), pady=(5,5))

        #БДДС
        self.bdds = CTk.CTkLabel(master=self, text="Таблица БДДС")
        self.bdds.grid(row=6, column=0, padx=(5,5), pady=(5,5))
        self.bdds_ex = CTk.CTkButton(master=self, text="Создать таблицу БДДС в Excel", command=self.open_win_bdds)
        self.bdds_ex.grid(row=7, column=0, padx=(5,5), pady=(5,5))

        #Добавление финансовых организаций
        self.fin_organisation = CTk.CTkLabel(master=self, text="Финансовые организации")
        self.fin_organisation.grid(row=8, column=0, padx=(5,5), pady=(5,5))
        self.fin_org = CTk.CTkButton(master=self, text="Открытие фин.организаций", command=self.open_fin_org)
        self.fin_org.grid(row=9, column=0, padx=(5,5), pady=(5,5))

        #Изменения в конкретных таблицах
        self.changer = CTk.CTkLabel(master=self, text="Добавить изменения в таблицу")
        self.changer.grid(row=10, column=0, padx=(5,5), pady=(15,5))
        self.changer_check_box = CTk.CTkComboBox(master=self, values=["ГПР", "ППО", "БДДС"])
        self.changer_check_box.grid(row=11, column=0, padx=(5,5), pady=(5,5))
        self.changer_but = CTk.CTkButton(master=self, text="Изменить")
        self.changer_but.grid(row=12, column=0, padx=(5,5), pady=(5,5))

        #Изменения в статьях
        self.ch_st = CTk.CTkLabel(master=self, text="Изменить статьи доходов и расходов")
        self.ch_st.grid(row=13, column=0, padx=(5,5), pady=(5,5))
        self.change_stat = CTk.CTkButton(master=self, text="Изменить")
        self.change_stat.grid(row=14, column=0, padx=(5,5), pady=(5,5))

        #Изменить даты начала работ
        self.time_work = CTk.CTkLabel(master=self, text="Изменить даты продаж и строительства")
        self.time_work.grid(row=15, column=0, padx=(5,5), pady=(5,5))
        self.ch_t = CTk.CTkButton(master=self, text="Изменить")
        self.ch_t.grid(row=16, column=0, padx=(5,5), pady=(5,5))

        self.poyasn_t = CTk.CTkLabel(master=self, text="При изменении файла закрывайте его в Excel!", text_color='#EB5E28')
        self.poyasn_t.grid(row=17, column=0, padx=(5,5), pady=(5,5))

    def _done(self):
        self.destroy()
        os.system('main.py')
        sys.exit(0)

    def but_make_gpr(self):
        try:
            create_tabel_gpr(id_pr=self.id_p, prov_create=True)
            mb.showinfo('Успешно!', 'Таблица ГПР была успешно создана')
        except SyntaxError:
            mb.showerror('Ошибка!', 'Были записаны неверные данные в ГПР')

    def but_make_ppo(self):
        create_tabel_ppo(id_pr=self.id_p, prov_create=True)
        mb.showinfo('Успешно!', 'Таблица ППО была успешно создана')

    def open_win_bdr(self):
        a = win_bdr(self.id_p)
        a.mainloop()

    def open_win_bdds(self):
        a = win_bdds(self.id_p)
        a.mainloop()

    def open_fin_org(self):
        a = win_fin_org(self.id_p)
        a.mainloop()
