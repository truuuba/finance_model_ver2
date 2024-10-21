import pyodbc

class company:
    def __init__(self, id, nazv):
        self.id = id
        self.nazv = nazv

class employe:
    def __init__(self, log_, pas_):
        self.log_ = log_
        self.pas_ = pas_

class stati_ur:
    def __init__(self, id_, id_st, code, nazv):
        self.id_ = id_
        self.id_st = id_st
        self.code = code
        self.nazv = nazv

class obj_str:
    def __init__(self, id_, nazv):
        self.id_ = id_
        self.nazv = nazv

class stati:
    def __init__(self, id_, id_o):
        self.id_ = id_
        self.id_o = id_o

class Sql:
    def __init__(self, database="FM_model", server=r"NODE2\DBLMSSQLSRV", username="connect_FM_model", password=r"9*%dA6lU&T6)p2PX", driver="ODBC Driver 17 for SQL Server"):
        connectionString = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        #return pyodbc.connect(connectionString)
        self.cnxn = pyodbc.connect(connectionString)

    def create_id(self, name_t):
        id_ = 0
        cursor = self.cnxn.cursor()
        zapros = "SELECT ID FROM " + name_t + ";"
        cursor.execute(zapros)
        data = make_arr_list(cursor.fetchall())
        for i in range(1, len(data)):
            if not(i in data):
                id_ = i
        if id_ == 0:
            if len(data) != 0:
                id_ = max(data) + 1
            else:
                id_ = 1
        return id_

    def take_nazv_company(self):
        cursor = self.cnxn.cursor()
        zapros = "SELECT nazv FROM company;"
        cursor.execute(zapros)
        data = make_arr_list(cursor.fetchall())
        for i in range(len(data)):
            data[i] = del_probel(data[i])
        cursor.close()
        return data
    
    def take_worker(self, id_c):
        cursor = self.cnxn.cursor()
        zapros = "SELECT log_, pas_ FROM employe WHERE Id_c = " + str(id_c) +";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = employe(log_ = data[i][0], pas_= data[i][1])
            datas.append(el)
        for el in datas:
            el.log_ = del_probel(el.log_)
            el.pas_ = del_probel(el.pas_)
        return datas
    
    def take_id_company(self, nazv):
        cursor = self.cnxn.cursor()
        zapros = "SELECT ID FROM company WHERE nazv = '" + nazv + "';"
        cursor.execute(zapros)
        data = make_arr_list(cursor.fetchall())
        return data[0]
    
    def take_adm(self, id_c):
        cursor = self.cnxn.cursor()
        zapros = "SELECT log_, pas_ FROM administ WHERE Id_k = " + str(id_c) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = employe(log_ = data[i][0], pas_= data[i][1])
            datas.append(el)
        for el in datas:
            el.log_ = del_probel(el.log_)
            el.pas_ = del_probel(el.pas_)
        return datas
    
    def input_empl(self, id_c, fam, im, otch, log, pas):
        cursor = self.cnxn.cursor()
        id_ = sql.create_id(name_t="employe")
        zapros = "INSERT INTO employe (ID, Id_c, fam, imya, otch, log_, pas_) VALUES (" + str(id_) + ", "+ str(id_c) + ", '" + fam + "', " + "'" + im + "', " + "'" + otch + "', " + "'" + log + "', " + "'" + pas + "');"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()

    def take_project(self, id_c):
        cursor = self.cnxn.cursor()
        zapros = "SELECT nazv FROM project WHERE Id_c = " + str(id_c) + ";"
        cursor.execute(zapros)
        data = make_arr_list(cursor.fetchall())
        for i in range(len(data)):
            data[i] = del_probel(data[i])
        return data
    
    def take_list_users(self, id_c):
        cursor = self.cnxn.cursor()
        zapros = "SELECT log_ FROM employe WHERE Id_c = " + str(id_c) + ";"
        cursor.execute(zapros)
        data = make_arr_list(cursor.fetchall())
        for i in range(len(data)):
            data[i] = del_probel(data[i])
        return data
    
    def del_user(self, Id_c, log_):
        cursor = self.cnxn.cursor()
        zapros = "DELETE FROM employe WHERE Id_c = " + str(Id_c) + " AND log_='" + log_ + "';"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()

    def make_arr_nazv(self, id_c):
        cursor = self.cnxn.cursor()
        zapros = "SELECT nazv FROM project WHERE Id_c = " + str(id_c) + ";"
        cursor.execute(zapros)
        data = make_arr_list(cursor.fetchall())
        for i in range(len(data)):
            data[i] = del_probel(data[i])
        return data
    
    def take_list_st_2(self):
        cursor = self.cnxn.cursor()
        zapros = "SELECT * FROM st_2_ur WHERE st_2_ur.Id_st_1 = 1 OR st_2_ur.Id_st_1 = 2 OR st_2_ur.Id_st_1 = 3 OR st_2_ur.Id_st_1 = 5;"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = stati_ur(id_ = data[i][0], id_st = data[i][1], code = data[i][2], nazv = data[i][3])
            datas.append(el)
        for el in datas:
            el.code = del_probel(el.code)
            el.nazv = del_probel(el.nazv)
        return datas

    def take_list_st_3(self, id_st):
        cursor = self.cnxn.cursor()
        zapros = "SELECT * FROM st_3_ur WHERE st_3_ur.Id_st_2 = " + str(id_st) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = stati_ur(id_ = data[i][0], id_st = data[i][1], code = data[i][2], nazv = data[i][3])
            datas.append(el)
        for el in datas:
            el.code = del_probel(el.code)
            el.nazv = del_probel(el.nazv)
        return datas
    
    def take_list_obj(self):
        cursor = self.cnxn.cursor()
        zapros = "SELECT * FROM st_2_ur WHERE st_2_ur.Id_st_1 = 4;"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = stati_ur(id_ = data[i][0], id_st = data[i][1], code = data[i][2], nazv = data[i][3])
            datas.append(el)
        for el in datas:
            el.code = del_probel(el.code)
            el.nazv = del_probel(el.nazv)
        return datas
    
    def input_project(self, id_c, nazv, yr_str, mnt_str):
        cursor = self.cnxn.cursor()
        id_ = sql.create_id("project")
        zapros = "INSERT INTO project (ID, id_c, nazv, yr_str, mnt_str) VALUES (" + str(id_) + ", " + str(id_c) + ", '" + nazv + "', " + str(yr_str) + ", '" + mnt_str + "');"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()
        return id_
    
    def input_obsh_stati(self, id_p, id_st_3):
        cursor = self.cnxn.cursor()
        id_ = sql.create_id("obsh_stati")
        zapros = "INSERT INTO obsh_stati (ID, Id_p, Id_st_3) VALUES (" + str(id_) + ", " + str(id_p) + ", " + str(id_st_3) + ");"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()
    
    def input_obj_str(self, id_p, nazv):
        cursor = self.cnxn.cursor()
        id_ = sql.create_id("object_str")
        zapros = "INSERT INTO object_str (ID, Id_p, nazv) VALUES (" + str(id_) + ", " + str(id_p) + ", '" + nazv + "');"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()

    def take_obj_str(self, id_p):
        cursor = self.cnxn.cursor()
        zapros = "SELECT ID, nazv FROM object_str WHERE Id_p = " + str(id_p) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = obj_str(data[i][0], data[i][1])
            datas.append(el)
        for el in datas:
            el.nazv = del_probel(el.nazv)
        return datas
    
    def input_st_obj(self, id_obj, id_st_3):
        cursor = self.cnxn.cursor()
        id_ = sql.create_id("obj_stati")
        zapros = "INSERT INTO obj_stati (ID, Id_obj, Id_st_3) VALUES (" + str(id_) + ", " + str(id_obj) + ", " + str(id_st_3) + ");"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()
    
    def take_obsh_stati(self, id_p):
        cursor = self.cnxn.cursor()
        zapros = "SELECT ID, Id_st_3 FROM obsh_stati WHERE Id_p = " + str(id_p) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = stati(data[i][0], data[i][1])
            datas.append(el)
        return datas
    
    def take_st_3(self, id_):
        cursor = self.cnxn.cursor()
        zapros = "SELECT ID, Id_st_2, code, nazv FROM st_3_ur WHERE ID = " + str(id_) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        el = stati_ur(data[0][0], data[0][1], data[0][2], data[0][3])
        el.code = del_probel(el.code)
        el.nazv = del_probel(el.nazv)
        return el
    
    def input_gpr_obsh(self, id_st_obsh, zavisim, prod):
        cursor = self.cnxn.cursor()
        id_ = sql.create_id("GPR_obsh")
        zapros = "INSERT INTO GPR_obsh (ID, Id_st_obsh, zavisim, prod) VALUES (" + str(id_) + ", " + str(id_st_obsh) + ", '" + zavisim + "', " + str(prod) + ");"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()


def make_arr_list(arr):
    arr2 = []
    for el in arr:
        for i in range(len(el)):
            arr2.append(el[i]) 
    return arr2

def del_probel(nm):
    n = len(nm)
    for j in range(n-1, 0, -1):
        if nm[j] == " ":
            nm = nm[:-1]
        else:
            return nm
        
sql = Sql()
