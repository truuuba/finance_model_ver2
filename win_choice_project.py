from win_choice_st import *

class win_choice_project(CTk.CTk):
    def __init__(self, id_c):
        super().__init__()
        self.geometry("1200x700")
        self.title("ФМ Калькулятор")
        self.resizable(True, True)
        self.protocol('WM_DELETE_WINDOW', self._done)
        self.id_c = id_c

        self.ch_lab = CTk.CTkLabel(master=self, text="Выберите проект или создайте новый")
        self.ch_lab.grid(row=0, column=0, padx=(0,0))

        self.old_pr_lab = CTk.CTkLabel(master=self, text="Текущие проекты")
        self.old_pr_lab.grid(row=3, column=0, padx=(0,0))
        arr = self.make_list_nazv()
        self.old_pr = CTk.CTkComboBox(master=self, values=arr)                                                  
        self.old_pr.grid(row=4, column=0, padx=(0,0))
        
        #Дописать переход к проекту
        self.old_pr_but = CTk.CTkButton(master=self, text="Перейти к проекту")
        self.old_pr_but.grid(row=5, column=0, padx=(20,20), pady=(20,20))

        self.pr = CTk.CTkLabel(master=self, text="Создайте новый проект")
        self.pr.grid(row=7, column=0, padx=(0,0))
        self.new_pr_but = CTk.CTkButton(master=self, text="Создать", command=self.new_pr)
        self.new_pr_but.grid(row=8, column=0, padx=(0,0))

    def _done(self):
        self.destroy()
        os.system('main.py')
        sys.exit(0)

    def new_pr(self):
        self.withdraw()
        c = win_choice_stati(self.id_c)
        c.mainloop()

    def make_list_nazv(self):
        arr = sql.make_arr_nazv(self.id_c)
        if len(arr) == 0:
            arr = ['Проекты отсутствуют']
        return arr
    
    def open_tables(self):
        val = self.old_pr.get()
    

    



