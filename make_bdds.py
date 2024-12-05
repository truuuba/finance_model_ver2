import os
import pandas as pd
from transliterate import translit
from connect_db import sql

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

def make_shapka(yr, mnt, yr_max):
    arr = ['Наименование статей']
    while yr != yr_max:
        arr.append(mnt + " " + str(yr))
        mnt = changer_mnt(mnt)
        if mnt == 'Январь':
            yr += 1
    for i in range(12):
        arr.append(mnt + " " + str(yr))
        mnt = changer_mnt(mnt)
        if mnt == 'Январь':
            yr += 1
    return arr

def make_bdds(id_pr):
    #Берем данные по названию проекта
    n_t = sql.take_name_pr(id_pr)
    name_table = translit(n_t, language_code='ru', reversed=True)

    #Время старта строительства
    mnt_start = sql.take_mnt_start(id_pr) 
    yr_start = sql.take_yr_start(id_pr)

    #Вытаскиваем объекты строительства
    object_str = sql.take_obj_for_ppo(id_pr)

    #Создаем шапку
    #Сначала проходимся по всем таблицам БДДС
    max_year_obj_str = sql.take_max_year_obj_str(id_pr)
    max_year_obsh = sql.take_max_year_obsh(id_pr)
    if max_year_obj_str > max_year_obsh:
        shapka = make_shapka(yr_start, mnt_start, max_year_obj_str)
    else:
        shapka = make_shapka(yr_start, mnt_start, max_year_obsh)
    
    #Вытаскиваем общие статьи по БДДС
    arr_BDDS_obsh = sql.take_data_BDDS_obsh(id_pr)
    #Вытаскиваем статьи по объектам БДДС
    arr_BDDS_obj = sql.take_data_BDDS_obj(id_pr)
    
    #Берем статьи по уровням - сначала в общих
    obsh_arr_st1 = []
    obsh_arr_st2 = []
    obsh_arr_st3 = []
    obsh_arr_st4 = []
    for el in arr_BDDS_obsh:
        elem4 = sql.found_st_4_ur(el.id_)
        obsh_arr_st4.append(elem4)
    for el in obsh_arr_st4:
        elem3 = sql.found_st_3_ur(el.id_st)
        if not(elem3 in obsh_arr_st3):
            obsh_arr_st3.append(elem3)
    for el in obsh_arr_st3:
        elem2 = sql.found_st_2_ur(el.id_st)
        if not(elem2 in obsh_arr_st2):
            obsh_arr_st2.append(elem2)
    for el in obsh_arr_st2:
        elem1 = sql.found_st_1_ur(el.id_st)
        if not(elem1 in obsh_arr_st1):
            obsh_arr_st1.append(elem1)

make_bdds(17)