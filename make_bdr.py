from connect_db import sql
from transliterate import translit

def changer_mnt(mnt):
    ind_i = 0
    arr = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
    for i in range(len(arr)):
        if arr[i] == mnt: 
            ind_i = i
            break
    if ind_i == 11:
        return arr[0]
    else:
        return arr[ind_i + 1]

def make_shapka(yr, mnt, prod):
    arr = ['Наименование статей']
    for i in range(prod):
        arr.append(mnt + " " + str(yr))
        mnt = changer_mnt(mnt)
        if mnt == 'Декабрь':
            yr += 1
    return arr

def create_tabel_bdr(id_pr):
    #Берем данные по названию проекта
    n_t = sql.take_name_pr(id_pr)
    name_table = translit(n_t, language_code='ru', reversed=True)
    sht_name = []

    #Создаем шапку таблицы
    mnt_start = sql.take_mnt_start(id_pr) 
    yr_start = sql.take_yr_start(id_pr)
    prod = sql.take_prod_proj(id_pr)
    shapka = make_shapka(yr=yr_start, mnt=mnt_start, prod=prod)

    #Вытаксиваем общие статьи 1,2,3,5
    #Поиск общих статей
    obsh_st = sql.take_obsh_stati_GPR(id_pr)
    #БДР по общим статьям
    arr_BDR_obsh = []
    arr_BDR_iskl = []
    #Уровни
    arr_st_1 = []
    arr_st_2 = []
    arr_st_3 = []
    #Собираем все необходимые статьи - тут ВСЕ вместе
    for el in obsh_st:
        elem = sql.take_st3(id_obsh=el.id_)
        arr_st_3.append(elem)
        #Вытащить данные по расходам в BDR_obsh 
        BDR_obsh = sql.take_BDR_obsh(id_obsh=el.id_)
        arr_BDR_obsh.append(BDR_obsh)
        #Вытащить данные по расходам в BDR_iskl
        BDR_iskl = sql.take_BDR_iskl(id_obsh=el.id_)
        arr_BDR_iskl.append(BDR_iskl)
    prov_st2 = []
    for el in arr_st_3:
        elem = sql.take_st2(el.id_)
        if elem.code not in prov_st2:
            prov_st2.append(elem.code)
            arr_st_2.append(elem)
    prov_st3 = []
    for el in arr_st_2:
        elem = sql.take_st1(el.id_)
        if elem.code not in prov_st3:
            prov_st3.append(elem.code)
            arr_st_1.append(elem)

    #Начинаем собирать массивы под общие статьи
    for el in arr_st_1:
        #Проверка под общие статы
        if el.id_ == 1 or el.id == 2 or el.id == 3 or el.id == 5:
            for el2 in arr_st_2:
                #Проверка подходящей статьи на втором уровне
                if el.id_st == el2.id:
                    for el3 in arr_st_3:
                        #Проверка подходящей статьи на третьем уровне
                        if el2.id_st == el3.id:
                            #Проверка по БДР
                            for elem in arr_BDR_obsh:
                                
