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

class stati_t:
    def __init__(self, id_, id_st_3, zav, prod, ind):
        self.id_ = id_
        self.id_st_3 = id_st_3
        self.zav = zav
        self.prod = prod
        self.ind = ind

class obj_str_gpr:
    def __init__(self, id_, nazv, posl):
        self.id_ = id_
        self.nazv = nazv
        self.posl = posl

class obj_str_ppo:
    def __init__(self, id_, nazv, prod, prod_pl, stoim, kv_cnt, sr_pl_rassr, d_ip, d_rassr, d_full, vsnos_r, m_st, yr_st):
        self.id_ = id_
        self.nazv = nazv
        self.prod = prod
        self.prod_pl = prod_pl
        self.stoim = stoim
        self.kv_cnt = kv_cnt
        self.sr_pl_rassr = sr_pl_rassr
        self.d_ip = d_ip
        self.d_rassr = d_rassr
        self.d_full = d_full
        self.vsnos_r = vsnos_r
        self.m_st = m_st
        self.yr_st = yr_st

class bdr:
    def __init__(self, id_, id_st, yr, mnt):
        self.id_ = id_
        self.id_st = id_st
        self.yr = yr
        self.mnt = mnt

class bdr_:
    def __init__(self, id_, id_st, yr, mnt, plan_ds):
        self.id_ = id_
        self.id_st = id_st
        self.yr = yr
        self.mnt = mnt
        self.plan_ds = plan_ds

class st_ur1:
    def __init__(self, id_, code, nazv):
        self.id_ = id_
        self.code = code
        self.nazv = nazv

class bdr_iskl:
    def __init__(self, id_, id_st, ds):
        self.id_ = id_
        self.id_st = id_st
        self.ds = ds

class st_ur4:
    def __init__(self, id_, id_st, code, nazv, param):
        self.id_ = id_
        self.id_st = id_st
        self.code = code
        self.nazv = nazv
        self.param = param

class PPO:
    def __init__(self, id_, id_obj, yr, mnt, dohod):
        self.id_ = id_
        self.id_obj = id_obj
        self.yr = yr
        self.mnt = mnt
        self.dohod = dohod

class sost:
    def __init__(self, id_, id_obj, nazv):
        self.id_ = id_
        self.id_obj = id_obj
        self.nazv = nazv

class sost_ppo:
    def __init__(self, id_, id_obj, nazv, cnt, stoim, prod_pl, sr_pl_rassr, dol_ip, dol_rass, full_pl, vsn_r):
        self.id_ = id_
        self.id_obj = id_obj
        self.nazv = nazv
        self.cnt = cnt
        self.stoim = stoim
        self.prod_pl = prod_pl
        self.sr_pl_rassr = sr_pl_rassr
        self.dol_ip = dol_ip
        self.dol_rass = dol_rass
        self.full_pl = full_pl
        self.vsn_r = vsn_r

class BDDS:
    def __init__(self, id_, id_o, id_st4, mnt, yr, ds):
        self.id_ = id_
        self.id_o = id_o
        self.id_st4 = id_st4
        self.mnt = mnt
        self.yr = yr
        self.ds = ds

class Sql:
    def __init__(self, database="FM_model", server=r"NODE2\DBLMSSQLSRV", username="connect_FM_model", password=r"9*%dA6lU&T6)p2PX", driver="ODBC Driver 17 for SQL Server"):
        connectionString = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
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
        zapros = "SELECT * FROM st_2_ur WHERE st_2_ur.Id_st_1 = 1 OR st_2_ur.Id_st_1 = 2 OR st_2_ur.Id_st_1 = 3 OR st_2_ur.Id_st_1 = 5 OR st_2_ur.Id_st_1 = 6 OR st_2_ur.Id_st_1 = 7 OR st_2_ur.code = '8.2' OR st_2_ur.code = '8.3' OR st_2_ur.code = '8.4' OR st_2_ur.code = '8.5' OR st_2_ur.code = '10.2' OR st_2_ur.code = '11.2' OR st_2_ur.code = '12.2' OR st_2_ur.code = '13.2' OR st_2_ur.code = '14.2' OR st_2_ur.code = '15.2';"
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
    
    def input_gpr_obsh(self, id_st_obsh, zavisim, prod, ind):
        cursor = self.cnxn.cursor()
        zapros = "UPDATE obsh_stati SET zavisim = '" + zavisim + "', prod = " + str(prod) + ", ind = " + str(ind) + " WHERE ID = " + str(id_st_obsh) + ";"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()

    def input_ppo_in_obj(self, id_, prod_pl, stoim, kv_cnt, sr_pl_rassr, dol_ipoteka, dol_rassr, dol_full_pl, vsnos_rassr, m_start_pr, yr_start_pr):
        cursor = self.cnxn.cursor()
        zapros = "UPDATE object_str SET prod_pl = " + str(prod_pl) + ", stoim = " + str(stoim) + ", kv_cnt = " + str(kv_cnt) + ", sr_pl_rassr = " + str(sr_pl_rassr) + ", dol_ipoteka = " + str(dol_ipoteka) + ", dol_rassr = " + str(dol_rassr) + ", dol_full_pl = " + str(dol_full_pl) + ", vsnos_rassr = " + str(vsnos_rassr) + ", m_start_pr = '" + m_start_pr + "', yr_start_pr = " + yr_start_pr + " WHERE ID = " + str(id_) + ";"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()
    
    def input_posl_in_obj(self, posl_str, id_):
        cursor = self.cnxn.cursor()
        zapros = "UPDATE object_str SET posl_str = " + str(posl_str) + " WHERE ID = " + str(id_) + ";"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()

    def take_obj_stati(self, id_obj):
        cursor = self.cnxn.cursor()
        zapros = "SELECT ID, Id_st_3 FROM obj_stati WHERE Id_obj = " + str(id_obj) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = stati(data[i][0], data[i][1])
            datas.append(el)
        return datas
    
    def input_gpr_obj(self, id_st_obj, zavisim, prod, ind):
        cursor = self.cnxn.cursor()
        zapros = "UPDATE obj_stati SET zavisim = '" + str(zavisim) + "', prod = " + str(prod) + ", ind = " + str(ind) + " WHERE ID = " + str(id_st_obj) + ";"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()

    def take_id_project(self, id_c, nazv):
        cursor = self.cnxn.cursor()
        zapros = "SELECT ID FROM project WHERE Id_c = " + str(id_c) + "AND nazv = '" + nazv + "';"
        cursor.execute(zapros)
        data = cursor.fetchall()
        return data[0][0]
    
    def obsh_stati_for_t(self, id_p):
        cursor = self.cnxn.cursor()
        zapros = "SELECT obsh_stati.ID, obsh_stati.Id_st_3, obsh_stati.zavisim, obsh_stati.prod, obsh_stati.ind FROM obsh_stati INNER JOIN st_3_ur ON obsh_stati.Id_st_3 = st_3_ur.ID INNER JOIN st_2_ur ON st_3_ur.Id_st_2 = st_2_ur.ID WHERE obsh_stati.Id_p = " + str(id_p) + " AND (st_2_ur.Id_st_1 = 1 OR st_2_ur.Id_st_1 = 2 OR st_2_ur.Id_st_1 = 3 OR st_2_ur.Id_st_1 = 5) ORDER BY obsh_stati.ind;"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = stati_t(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4])
            datas.append(el)
        for el in datas:
            el.zav = del_probel(el.zav)
        return datas
    
    def take_mnt_start(self, id_p):
        cursor = self.cnxn.cursor()
        zapros = "SELECT mnt_str FROM project WHERE ID = " + str(id_p) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        res = del_probel(data[0][0])
        return res
        
    def take_yr_start(self, id_p):
        cursor = self.cnxn.cursor()
        zapros = "SELECT yr_str FROM project WHERE ID = " + str(id_p) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        return data[0][0]
    
    def take_name_pr(self, id_p):
        cursor = self.cnxn.cursor()
        zapros = "SELECT nazv FROM project WHERE ID = " + str(id_p) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        return del_probel(data[0][0])
    
    def obj_str_gpr(self, id_p):
        cursor = self.cnxn.cursor()
        zapros = "SELECT ID, nazv, posl_str FROM object_str WHERE Id_p = " + str(id_p) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = obj_str_gpr(data[i][0], data[i][1], data[i][2])
            datas.append(el)
        for el in datas:
            el.nazv = del_probel(el.nazv)
        return datas
    
    def stati_obj_str(self, id_obj):
        cursor = self.cnxn.cursor()
        zapros = "SELECT ID, Id_st_3, zavisim, prod, ind FROM obj_stati WHERE Id_obj = " + str(id_obj) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = stati_t(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4])
            datas.append(el)
        for el in datas:
            el.zav = del_probel(el.zav)
        return datas
    
    def input_prod_obj_str(self, id_, prod):
        cursor = self.cnxn.cursor()
        zapros = "UPDATE object_str SET prodolj = " + str(prod) + "WHERE ID = " + str(id_) + ";"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()
    
    def input_prod_pr(self, id_, prod):
        cursor = self.cnxn.cursor()
        zapros = "UPDATE project SET prod = " + str(prod) + "WHERE ID = " + str(id_) + ";"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()

    def take_obj_for_ppo(self, id_pr):
        cursor = self.cnxn.cursor()
        zapros = "SELECT ID, nazv, prodolj, prod_pl, stoim, kv_cnt, sr_pl_rassr, dol_ipoteka, dol_rassr, dol_full_pl, vsnos_rassr, m_start_pr, yr_start_pr FROM object_str WHERE Id_p = " + str(id_pr) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = obj_str_ppo(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5], data[i][6], data[i][7], data[i][8], data[i][9], data[i][10], data[i][11], data[i][12])
            datas.append(el)
        for el in datas:
            el.nazv = del_probel(el.nazv)
            if not(el.m_st == None):
                el.m_st = del_probel(el.m_st)
        return datas
    
    def input_ppo(self, id_obj, yr, mnt, dohod):
        cursor = self.cnxn.cursor()
        id_ = self.create_id("PPO_obj")
        zapros = "INSERT INTO PPO_obj (ID, Id_obj, yr, mnt, dohod) VALUES (" + str(id_) + "," + str(id_obj) + "," + str(yr) + ", '" + str(mnt) + "', " + str(dohod) + ");"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()
    
    def prov_PPO(self, id_obj):
        cursor = self.cnxn.cursor()
        zapros = "SELECT * FROM PPO_obj WHERE Id_obj = " + str(id_obj) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        if len(data) != 0:
            cursor = self.cnxn.cursor()
            zapros = "DELETE FROM PPO_obj WHERE Id_obj = "  + str(id_obj) + ";"
            cursor.execute(zapros)
            self.cnxn.commit()
            cursor.close()

    def prov_BDR(self, id_st_obsh, array):
        cursor = self.cnxn.cursor()
        zapros = "SELECT * FROM BDR_obsh WHERE ID_st_obsh = " + str(id_st_obsh) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        if len(data) != 0:
            for i in range(len(data)):
                cursor = self.cnxn.cursor()
                zapros = "UPDATE BDR_obsh SET yr = " + str(array[i].yr) + ", mnt = '" + array[i].mnt + "' WHERE ID = " + str(data[i][0]) + ";" 
                cursor.execute(zapros)
                self.cnxn.commit()
                cursor.close()
        else:
            for el in array:
                cursor = self.cnxn.cursor()
                id_ = self.create_id("BDR_obsh")
                zapros = "INSERT INTO BDR_obsh (ID, ID_st_obsh, yr, mnt) VALUES (" + str(id_) + ", " + str(id_st_obsh) + ", " + str(el.yr) + ", '" + el.mnt + "');"
                cursor.execute(zapros)
                self.cnxn.commit()
                cursor.close()

    def found_id_st_obsh(self, id_pr, code):
        cursor = self.cnxn.cursor()
        zapros = "SELECT obsh_stati.ID FROM obsh_stati INNER JOIN st_3_ur ON obsh_stati.Id_st_3 = st_3_ur.ID WHERE obsh_stati.Id_p = " + str(id_pr) + " AND st_3_ur.code = '" + code + "';"
        cursor.execute(zapros)
        data = cursor.fetchall()
        return data[0][0]

    def found_id_obj_st(self, id_obj, code):
        cursor = self.cnxn.cursor()
        zapros = "SELECT obj_stati.ID FROM obj_stati INNER JOIN st_3_ur ON obj_stati.Id_st_3 = st_3_ur.ID WHERE obj_stati.Id_obj = " + str(id_obj) + " AND st_3_ur.code = '" + str(code) + "';"
        cursor.execute(zapros)
        data = cursor.fetchall()
        return data[0][0]

    def prov_BDR_obj(self, id_st_obj, array):
        cursor = self.cnxn.cursor()
        zapros = "SELECT ID FROM BDR_obj WHERE ID_st_obj = " + str(id_st_obj) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        if len(data) != 0:
            for i in range(len(data)):
                cursor = self.cnxn.cursor()
                zapros = "UPDATE BDR_obj SET yr = " + str(array[i].yr) + ", mnt = '" + array[i].mnt + "' WHERE ID = " + str(data[i][0]) + ";" 
                cursor.execute(zapros)
                self.cnxn.commit() 
                cursor.close()
        else:
            for el in array:
                cursor = self.cnxn.cursor()
                id_ = self.create_id("BDR_obj")
                zapros = "INSERT INTO BDR_obj (ID, ID_st_obj, yr, mnt) VALUES (" + str(id_) + ", " + str(id_st_obj) + ", " + str(el.yr) + ", '" + el.mnt + "');"
                cursor.execute(zapros)
                self.cnxn.commit()
                cursor.close()

    def take_data_BDR_obsh(self, id_st_obj):
        cursor = self.cnxn.cursor()
        zapros = "SELECT ID, ID_st_obsh, yr, mnt FROM BDR_obsh WHERE ID_st_obsh = " + str(id_st_obj) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = bdr(data[i][0], data[i][1], data[i][2], data[i][3])
            datas.append(el)
        for el in datas:
            el.mnt = del_probel(el.mnt)
        return datas
    
    def take_data_BDR_obj(self, id_st_obj):
        cursor = self.cnxn.cursor()
        zapros = "SELECT ID, ID_st_obj, yr, mnt FROM BDR_obj WHERE ID_st_obj = " + str(id_st_obj) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = bdr(data[i][0], data[i][1], data[i][2], data[i][3])
            datas.append(el)
        for el in datas:
            el.mnt = del_probel(el.mnt)
        return datas
    
    def take_nazv_BDR(self, id_bdr):
        cursor = self.cnxn.cursor()
        zapros = "SELECT st_3_ur.ID, st_3_ur.Id_st_2, st_3_ur.code, st_3_ur.nazv FROM st_3_ur INNER JOIN obsh_stati ON obsh_stati.Id_st_3 = st_3_ur.ID INNER JOIN BDR_obsh ON BDR_obsh.ID_st_obsh = obsh_stati.ID WHERE BDR_obsh.ID = " + str(id_bdr) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = stati_ur(data[i][0], data[i][1], data[i][2], data[i][3])
            datas.append(el)
        for el in datas:
            el.nazv = del_probel(el.nazv)
            el.code = del_probel(el.code)
        return datas[0]
    
    def update_bdr_obsh(self, plan_ds, id_):
        cursor = self.cnxn.cursor()
        zapros = "UPDATE BDR_obsh SET plan_ds = " + str(plan_ds) + " WHERE ID = " + str(id_) + ";"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()

    def found_zapisi_GPR_obsh(self, id_p):
        cursor = self.cnxn.cursor()
        zapros = "SELECT BDR_obsh.plan_ds FROM BDR_obsh INNER JOIN obsh_stati ON BDR_obsh.ID_st_obsh = obsh_stati.ID INNER JOIN project ON obsh_stati.Id_p = project.ID WHERE project.ID = " + str(id_p) + ";"
        cursor.execute(zapros)
        data = make_arr_list(cursor.fetchall())
        for el in data:
            if el == None:
                return False
        return True
    
    def found_zapisi_GPR_obj(self, id_p):
        cursor = self.cnxn.cursor()
        zapros = "SELECT BDR_obj.plan_ds FROM BDR_obj INNER JOIN obj_stati ON BDR_obj.Id_st_obj = obj_stati.ID INNER JOIN object_str ON obj_stati.Id_obj = object_str.ID INNER JOIN project ON object_str.Id_p = project.ID WHERE project.ID = " + str(id_p) + ";"
        cursor.execute(zapros)
        data = make_arr_list(cursor.fetchall())
        for el in data:
            if el == None:
                return False
        return True
    
    def update_bdr_obj(self, id_, plan_ds):
        cursor = self.cnxn.cursor()
        zapros = "UPDATE BDR_obj SET plan_ds = " + str(plan_ds) + " WHERE ID = " + str(id_) + ";"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()

    def take_obsh_stati_GPR(self, id_p):
        cursor = self.cnxn.cursor()
        zapros = "SELECT obsh_stati.ID, obsh_stati.Id_st_3 FROM obsh_stati INNER JOIN st_3_ur ON obsh_stati.Id_st_3 = st_3_ur.ID INNER JOIN st_2_ur ON st_3_ur.Id_st_2 = st_2_ur.ID WHERE obsh_stati.Id_p = " + str(id_p) + " AND (st_2_ur.Id_st_1 = 1 OR st_2_ur.Id_st_1 = 2 OR st_2_ur.Id_st_1 = 3 OR st_2_ur.Id_st_1 = 5);"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = stati(data[i][0], data[i][1])
            datas.append(el)
        return datas
    
    def take_stati_iskl(self, id_p):
        cursor = self.cnxn.cursor()
        zapros = "SELECT obsh_stati.ID, obsh_stati.Id_st_3 FROM obsh_stati INNER JOIN st_3_ur ON obsh_stati.Id_st_3 = st_3_ur.ID INNER JOIN st_2_ur ON st_3_ur.Id_st_2 = st_2_ur.ID WHERE obsh_stati.Id_p = " + str(id_p) + " AND (st_2_ur.Id_st_1 = 6 OR st_2_ur.Id_st_1 = 7 OR st_2_ur.code = '10.2' OR st_2_ur.code = '11.2' OR st_2_ur.code = '12.2' OR st_2_ur.code = '13.2' OR st_2_ur.code = '14.2' OR st_2_ur.code = '15.2');"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = stati(data[i][0], data[i][1])
            datas.append(el)
        return datas
    
    def input_BDR_iskl(self, id_st, ds):
        cursor = self.cnxn.cursor()
        id_ = self.create_id("BDR_iskl")
        zapros = "INSERT INTO BDR_iskl (ID, ID_st_obsh, ds) VALUES (" + str(id_) + ", " + str(id_st) + ", " + str(ds) + ");"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()

    def prov_BDR_iskl(self, id_p):
        cursor = self.cnxn.cursor()
        zapros = "SELECT * FROM BDR_iskl INNER JOIN obsh_stati ON BDR_iskl.ID_st_obsh = obsh_stati.ID WHERE obsh_stati.Id_p = " + str(id_p) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        if len(data) == 0:
            return False
        else:
            return True
    
    def upd_BDR_iskl(self, obsh_st):
        for el in obsh_st:
            cursor = self.cnxn.cursor()
            zapros = "DELETE FROM BDR_iskl WHERE ID_st_obsh = " + str(el.id_) + ";"
            cursor.execute(zapros)
            self.cnxn.commit()
            cursor.close()

    def take_prod_proj(self, id_p):
        cursor = self.cnxn.cursor()
        zapros = "SELECT prod FROM project WHERE ID = " + str(id_p) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        return data[0][0]
    
    def take_st3(self, id_obsh):
        cursor = self.cnxn.cursor()
        zapros = "SELECT st_3_ur.ID, st_3_ur.Id_st_2, st_3_ur.code, st_3_ur.nazv FROM st_3_ur INNER JOIN obsh_stati ON obsh_stati.Id_st_3 = st_3_ur.ID WHERE obsh_stati.ID = " + str(id_obsh) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        el = stati_ur(data[0][0], data[0][1], del_probel(data[0][2]), del_probel(data[0][3]))
        return el
    
    def take_st2(self, id_st3):
        cursor = self.cnxn.cursor()
        zapros = "SELECT st_2_ur.ID, st_2_ur.Id_st_1, st_2_ur.code, st_2_ur.nazv FROM st_2_ur INNER JOIN st_3_ur ON st_3_ur.Id_st_2 = st_2_ur.ID WHERE st_3_ur.ID = " + str(id_st3) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        el = stati_ur(data[0][0], data[0][1], del_probel(data[0][2]), del_probel(data[0][3]))
        return el
    
    def take_st1(self, id_st2):
        cursor = self.cnxn.cursor()
        zapros = "SELECT st_1_ur.ID, st_1_ur.code, st_1_ur.nazv FROM st_1_ur INNER JOIN st_2_ur ON st_2_ur.Id_st_1 = st_1_ur.ID WHERE st_2_ur.ID = " + str(id_st2) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        el = st_ur1(data[0][0], del_probel(data[0][1]), del_probel(data[0][2]))
        return el

    def take_BDR_obsh(self, id_obsh):
        cursor = self.cnxn.cursor()
        zapros = "SELECT ID, ID_st_obsh, mnt, yr, plan_ds FROM BDR_obsh WHERE ID_st_obsh = " + str(id_obsh) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        if len(data) != 0:
            datas = []
            for i in range(len(data)):
                el = bdr_(data[i][0], data[i][1], data[i][3], data[i][2], data[i][4])
                datas.append(el)
            for el in datas:
                el.mnt = del_probel(el.mnt)
            return datas
        else:
            return False
    
    def take_BDR_iskl(self, id_obsh):
        cursor = self.cnxn.cursor()
        zapros = "SELECT ID, ID_st_obsh, ds FROM BDR_iskl WHERE ID_st_obsh = " + str(id_obsh) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        if len(data) != 0:
            el = bdr_iskl(data[0][0], data[0][1], data[0][2])
            return el
        else:
            return False
        
    def take_data_BDR_obj_t(self, id_st_obj):
        cursor = self.cnxn.cursor()
        zapros = "SELECT ID, ID_st_obj, yr, mnt, plan_ds FROM BDR_obj WHERE ID_st_obj = " + str(id_st_obj) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = bdr_(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4])
            datas.append(el)
        for el in datas:
            el.mnt = del_probel(el.mnt)
        return datas
    
    def _take_obsh_stati_(self, id_p):
        cursor = self.cnxn.cursor()
        zapros = "SELECT obsh_stati.ID, obsh_stati.Id_st_3 FROM obsh_stati INNER JOIN st_3_ur ON obsh_stati.Id_st_3 = st_3_ur.ID WHERE obsh_stati.Id_p = " + str(id_p) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = stati(data[i][0], data[i][1])
            datas.append(el)
        return datas
    
    def found_id_obj(self, nazv, id_p):
        cursor = self.cnxn.cursor()
        zapros = "SELECT ID FROM object_str WHERE nazv = '" + nazv + "' AND Id_p = " + str(id_p) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        return data[0][0]
    
    def found_obj_str_stati_(self, id_obj):
        cursor = self.cnxn.cursor()
        zapros = "SELECT ID, Id_st_3 FROM obj_stati WHERE Id_obj = " + str(id_obj) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = stati(data[i][0], data[i][1])
            datas.append(el)
        return datas
    
    def take_st_ur_4(self, id_st3):
        cursor = self.cnxn.cursor()
        zapros = "SELECT * FROM st_4_ur WHERE Id_st_3 = " + str(id_st3) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = st_ur4(data[i][0], data[i][1], del_probel(data[i][2]), del_probel(data[i][3]), data[i][4])
            datas.append(el)
        return datas

    def take_data_PPO(self, id_obj):
        cursor = self.cnxn.cursor()
        zapros = "SELECT ID, Id_obj, yr, mnt, dohod FROM PPO_obj WHERE Id_obj = " + str(id_obj) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = PPO(data[i][0], data[i][1], data[i][2], del_probel(data[i][3]), data[i][4])
            datas.append(el)
        return datas

    def take_mnt_prodaj(self, id_):
        cursor = self.cnxn.cursor()
        zapros = "SELECT m_start_pr FROM object_str WHERE ID = " + str(id_) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        if data[0][0] == None:
            return 0
        else:
            return del_probel(data[0][0])
        
    def take_yr_prodaj(self, id_):
        cursor = self.cnxn.cursor()
        zapros = "SELECT yr_start_pr FROM object_str WHERE ID = " + str(id_) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        if data[0][0] == None:
            return 0
        else:
            return data[0][0]
        
    def input_sost_obj(self, id_obj, nazv):
        cursor = self.cnxn.cursor()
        id_ = sql.create_id(name_t="sost_obj")
        zapros = "INSERT INTO sost_obj (ID, Id_obj, nazv) VALUES (" + str(id_) + ", " + str(id_obj) + ", '" + str(nazv) + "');"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()

    def take_sost_obj(self, id_p):
        cursor = self.cnxn.cursor()
        zapros = "SELECT sost_obj.ID, sost_obj.Id_obj, sost_obj.nazv FROM sost_obj INNER JOIN object_str ON sost_obj.Id_obj = object_str.ID WHERE object_str.Id_p = " + str(id_p) + " ORDER BY sost_obj.Id_obj;"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = sost(data[i][0], data[i][1], del_probel(data[i][2]))
            datas.append(el)
        return datas
    
    def take_nazv_obj_str(self, id_):
        cursor = self.cnxn.cursor()
        zapros = "SELECT nazv FROM object_str WHERE ID = " + str(id_) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        return del_probel(data[0][0])
    
    def input_sost_obj_m_k(self, id_, cnt, stoim):
        cursor = self.cnxn.cursor()
        zapros = "UPDATE sost_obj SET cnt = " + str(cnt) + ", stoim = " + str(stoim) + " WHERE ID = " + str(id_) + ";"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()

    def input_sost_komm_pom(self, id_, cnt, stoim, prod_pl, sr_pl_rassr, dol_ip, dol_rass, full_pl, vsn_r):
        cursor = self.cnxn.cursor()
        zapros = "UPDATE sost_obj SET cnt = " + str(cnt) + ", stoim = " + str(stoim) + ", prod_pl = " + str(prod_pl) + ", sr_pl_rassr = " + str(sr_pl_rassr) + ", dol_ipoteka = " + str(dol_ip) + ", dol_rassr = " + str(dol_rass) + ", dol_full_pl = " + str(full_pl) + ", vsnos_rassr = " + str(vsn_r) + " WHERE ID = " + str(id_) + ";"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()

    def take_sost_obj_ppo(self, id_):
        cursor = self.cnxn.cursor()
        zapros = "SELECT * FROM sost_obj WHERE Id_obj = " + str(id_) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = sost_ppo(data[i][0], data[i][1], del_probel(data[i][2]), data[i][3], data[i][4], data[i][5], data[i][6], data[i][7], data[i][8], data[i][9], data[i][10])
            datas.append(el)
        return datas
    
    def prov_s_PPO(self, id_s_obj):
        cursor = self.cnxn.cursor()
        zapros = "SELECT * FROM PPO_sost_obj WHERE Id_s_obj = " + str(id_s_obj) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        if len(data) != 0:
            cursor = self.cnxn.cursor()
            zapros = "DELETE FROM PPO_sost_obj WHERE Id_s_obj = "  + str(id_s_obj) + ";"
            cursor.execute(zapros)
            self.cnxn.commit()
            cursor.close()

    def input_ppo_sost(self, id_s_obj, yr, mnt, dohod):
        cursor = self.cnxn.cursor()
        id_ = self.create_id("PPO_sost_obj")
        zapros = "INSERT INTO PPO_sost_obj (ID, Id_s_obj, yr, mnt, dohod) VALUES (" + str(id_) + "," + str(id_s_obj) + "," + str(yr) + ", '" + str(mnt) + "', " + str(dohod) + ");"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()

    def take_PPO_sost(self, id_s_obj):
        cursor = self.cnxn.cursor()
        zapros = "SELECT ID, Id_s_obj, yr, mnt, dohod FROM PPO_sost_obj WHERE Id_s_obj = " + str(id_s_obj) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = PPO(data[i][0], data[i][1], data[i][2], del_probel(data[i][3]), data[i][4])
            datas.append(el)
        return datas
    
    def take_nazv_fin_org(self, id_p):
        cursor = self.cnxn.cursor()
        zapros = "SELECT nazv FROM fin_org WHERE Id_p = " + str(id_p) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = make_arr_list(data)
        for i in range(len(datas)):
            datas[i] = del_probel(datas[i])
        return datas    

    def take_st_for_finorg(self):
        cursor = self.cnxn.cursor()
        zapros = "SELECT st_4_ur.ID, st_4_ur.Id_st_3, st_4_ur.code, st_4_ur.nazv FROM st_4_ur INNER JOIN st_3_ur ON st_4_ur.Id_st_3 = st_3_ur.ID WHERE st_3_ur.Id_st_2 = 60;"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = stati_ur(data[i][0], data[i][1], del_probel(data[i][2]), del_probel(data[i][3]))
            datas.append(el)
        return datas
    
    def input_fin_org(self, id_p, nazv):
        cursor = self.cnxn.cursor()
        id_ = sql.create_id("fin_org")
        zapros = "INSERT INTO fin_org (ID, Id_p, nazv) VALUES (" + str(id_) + ", " + str(id_p) + ", '" + nazv + "');"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()

    def take_st4_of_code(self, code):
        cursor = self.cnxn.cursor()
        zapros = "SELECT ID FROM st_4_ur WHERE code = '" + code + "';"
        cursor.execute(zapros)
        data = cursor.fetchall()
        return data[0][0]
    
    def take_nazv_finorg(self, id_p, nazv):
        cursor = self.cnxn.cursor()
        zapros = "SELECT ID FROM fin_org WHERE Id_p = " + str(id_p) + " AND nazv = '" + nazv + "';"
        cursor.execute(zapros)
        data = cursor.fetchall()
        return data[0][0]

    def input_stati_finorg(self, id_f_org, id_st_4, mnt, yr, ds):
        cursor = self.cnxn.cursor()
        id_ = sql.create_id("stat_fin_org")
        zapros = "INSERT INTO stat_fin_org (ID, Id_f_org, Id_st_4, mnt, yr, ds) VALUES (" + str(id_) + ", " + str(id_f_org) + ", " + str(id_st_4) + ", '" + mnt + "', " + str(yr) + ", " + str(ds) + ");"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()

    def take_st3_for_obsh(self, id_st_4):
        cursor = self.cnxn.cursor()
        zapros = "SELECT st_3_ur.ID FROM st_3_ur INNER JOIN st_4_ur ON st_4_ur.Id_st_3 = st_3_ur.ID WHERE st_4_ur.ID = " + str(id_st_4) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        return data[0][0]
    
    def input_data_BDDS_obsh(self, id_obsh, id_st4, yr, mnt, ds):
        cursor = self.cnxn.cursor()
        id_ = sql.create_id("BDDS_obsh")
        zapros = "INSERT INTO BDDS_obsh (ID, ID_st_obsh, Id_st4, yr, mnt, ds) VALUES (" + str(id_) + ", " + str(id_obsh) + ", " + str(id_st4) + ", " + str(yr) + ", '" + str(mnt) + "', " + str(ds) + ");"
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()
    
    def input_data_BDDS_obj(self, id_st_obj, id_st4, yr, mnt, ds):
        cursor = self.cnxn.cursor()
        id_ = sql.create_id("BDDS_obj")
        zapros = "INSERT INTO BDDS_obj (ID, ID_st_obJ, Id_st4, yr, mnt, ds) VALUES (" + str(id_) + ", " + str(id_st_obj) + ", " + str(id_st4) + ", " + str(yr) + ", '" + str(mnt) + "', " + str(ds) + ");"  
        cursor.execute(zapros)
        self.cnxn.commit()
        cursor.close()
    
    def take_max_year_obj_str(self, id_pr):
        cursor = self.cnxn.cursor()
        zapros = "SELECT MAX(yr) FROM BDDS_obj INNER JOIN obj_stati ON BDDS_obj.ID_st_obj = obj_stati.ID INNER JOIN object_str ON obj_stati.Id_obj = object_str.ID WHERE object_str.Id_p = " + str(id_pr) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        return data[0][0]
    
    def take_max_year_obsh(self, id_pr):
        cursor = self.cnxn.cursor()
        zapros = "SELECT MAX(yr) FROM BDDS_obsh INNER JOIN obsh_stati ON BDDS_obsh.ID_st_obsh = obsh_stati.ID WHERE obsh_stati.Id_p = " + str(id_pr) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        return data[0][0]
    
    def take_data_BDDS_obsh(self, id_pr):
        cursor = self.cnxn.cursor()
        zapros = "SELECT BDDS_obsh.ID, BDDS_obsh.ID_st_obsh, BDDS_obsh.Id_st4, BDDS_obsh.mnt, BDDS_obsh.yr, BDDS_obsh.ds FROM BDDS_obsh INNER JOIN obsh_stati ON BDDS_obsh.ID_st_obsh = obsh_stati.ID WHERE obsh_stati.Id_p = " + str(id_pr) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = BDDS(data[i][0], data[i][1], data[i][2], del_probel(data[i][3]), data[i][4], data[i][5])
            datas.append(el)
        return datas
    
    def take_data_BDDS_obj(self, id_pr):
        cursor = self.cnxn.cursor()
        zapros = "SELECT BDDS_obj.ID, BDDS_obj.ID_st_obj, BDDS_obj.Id_st4, BDDS_obj.mnt, BDDS_obj.yr, BDDS_obj.ds FROM BDDS_obj INNER JOIN obj_stati ON BDDS_obj.ID_st_obj = obj_stati.ID INNER JOIN object_str ON obj_stati.Id_obj = object_str.ID WHERE object_str.Id_p = " + str(id_pr) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = BDDS(data[i][0], data[i][1], data[i][2], del_probel(data[i][3]), data[i][4], data[i][5])
            datas.append(el)
        return datas

    def found_st_4_ur(self, id_):
        cursor = self.cnxn.cursor()
        zapros = "SELECT ID, Id_st_3, code, nazv, parametr FROM st_4_ur WHERE ID = " + str(id_) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = st_ur4(data[i][0], data[i][1], del_probel(data[i][2]), del_probel(data[i][3]), del_probel(data[i][4]))
            datas.append(el)
        return datas
    
    def found_st_3_ur(self, id_st4):
        cursor = self.cnxn.cursor()
        zapros = "SELECT st_3_ur.ID, st_3_ur.Id_st_2, st_3_ur.code, st_3_ur.nazv FROM st_3_ur INNER JOIN st_4_ur ON st_4_ur.Id_st_3 = st_3_ur.ID WHERE st_4_ur.ID = " + str(id_st4) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = stati_ur(data[i][0], data[i][1], del_probel(data[i][2]), del_probel(data[i][3]))
            datas.append(el)
        return datas
    
    def found_st_2_ur(self, id_st3):
        cursor = self.cnxn.cursor()
        zapros = "SELECT st_2_ur.ID, st_2_ur.Id_st_1, st_2_ur.code, st_2_ur.nazv FROM st_2_ur INNER JOIN st_3_ur ON st_3_ur.Id_st_2 = st_2_ur.ID WHERE st_3_ur.ID = " + str(id_st3) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = stati_ur(data[i][0], data[i][1], del_probel(data[i][2]), del_probel(data[i][3]))
            datas.append(el)
        return datas
    
    def found_st_1_ur(self, id_st1):
        cursor = self.cnxn.cursor()
        zapros = "SELECT st_1_ur.ID, st_1_ur.code, st_1_ur.nazv FROM st_1_ur INNER JOIN st_2_ur ON st_2_ur.Id_st_1 = st_1_ur.ID WHERE st_2_ur.ID = " + str(id_st1) + ";"
        cursor.execute(zapros)
        data = cursor.fetchall()
        datas = []
        for i in range(len(data)):
            el = st_ur1(data[i][0], del_probel(data[i][1]), del_probel(data[i][2]))
            datas.append(el)
        return datas

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
    return nm
        
sql = Sql()
