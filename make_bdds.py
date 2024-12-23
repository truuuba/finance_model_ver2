import os
import pandas as pd
from transliterate import translit
from connect_db import sql
import re

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
        if mnt == 'Январь':
            yr += 1
    return arr

def change_shapka(shapka, m_start_pr, yr_start_pr, prod):
    res_shapka = []
    temp = m_start_pr + " " + str(yr_start_pr)
    prov = False
    #Длина шапки до момента старта продаж
    for i in range(len(shapka)):
        if shapka[i] == temp:
            prov = True
            break
        else:
            res_shapka.append(shapka[i])
    #Увеличиваем продолжительность до старта продаж
    a = res_shapka[len(res_shapka)-1].split()
    mnt = a[0]
    yr = int(a[1])
    if not prov:
        while True:
            mnt = changer_mnt(mnt)
            if mnt == 'Декабрь':
                yr += 1
            temp2 = mnt + " " + str(yr)
            res_shapka.append(temp2)
            if temp == temp2:
                break
    #Доделываем шапку по продолжительности продаж
    for i in range(prod-1):
        res_shapka.append(mnt + " " + str(yr))
        mnt = changer_mnt(mnt)
        if mnt == 'Декабрь':
            yr += 1
    return res_shapka

def make_bdds(id_pr):
    #Берем данные по названию проекта
    n_t = sql.take_name_pr(id_pr)
    name_table = translit(n_t, language_code='ru', reversed=True)

    #Время старта строительства
    mnt_start = sql.take_mnt_start(id_pr) 
    yr_start = sql.take_yr_start(id_pr)
    prod = sql.take_prod_proj(id_pr)

    #Вытаскиваем объекты строительства
    object_str = sql.take_obj_for_ppo(id_pr)

    #Создаем шапку
    #Сначала проходимся по всем таблицам БДДС
    shapka = make_shapka(yr=yr_start, mnt=mnt_start, prod=prod)

    #Ищем максимальную шапку
    max_shapka = shapka
    for el in object_str:
        shapka_obj = []
        m_start_pr = sql.take_mnt_prodaj(el.id_)
        yr_start_pr = sql.take_yr_prodaj(el.id_)
        if not(m_start_pr == 0 or yr_start_pr == 0):
            shapka_obj = change_shapka(shapka, m_start_pr, yr_start_pr, el.prod)
        if len(shapka_obj) > len(max_shapka):
            max_shapka = shapka_obj
    shapka = max_shapka
    prod = len(max_shapka) - 1

    #Вытаскиваем общие статьи по БДДС
    arr_BDDS_obsh = sql.take_data_BDDS_obsh(id_pr)
    #Вытаскиваем статьи по объектам БДДС
    arr_BDDS_obj = sql.take_data_BDDS_obj(id_pr)

    #Начинаем формировать таблицу БДДС - до первого столкновения с объектами строительства
    bdds_res = [] 
    bdds_res.append(shapka)
    #Вытаскиваем статьи по 1, 2, 3
    obsh_arr_st1 = sql.take_stati123_level1()
    obsh_arr_st2 = sql.take_stati123_level2()
    obsh_arr_st3 = []
    obsh_arr_st4 = []
    for el in obsh_arr_st2:
        _arr_ = sql.take_level_down_st3(el.id_)
        for elem in _arr_:
            obsh_arr_st3.append(elem)
    for el in obsh_arr_st3:
        _arr_ = sql.take_level_down_st4(el.id_)
        for elem in _arr_:
            obsh_arr_st4.append(elem)

    #Проходимся по общим статьям
    for el in obsh_arr_st1:
        #Массивы для сортировки
        arr_elems_2 = []
        arr_elems_3 = []
        arr_elems_4 = []
        elem_st1 = [el.code + ' ' + el.nazv]
        for i in range(prod):
            elem_st1.append(0)
        for el2 in obsh_arr_st2:
            #Проверка подходящей статьи на втором уровне
            if el2.id_st == el.id_:
                Arr_elems_3 = []
                Arr_elems_4 = []
                #Создание массива по 2 статье
                elem_st2 = [el2.code + ' ' + el2.nazv]
                for i in range(prod):
                    elem_st2.append(0)
                for el3 in obsh_arr_st3:
                    #Проверка подходящей статьи на третьем уровне
                    if el3.id_st == el2.id_:
                        #Создание массива по 3 статье
                        elem_st3 = [el3.code + ' ' + el3.nazv]
                        for i in range(prod):
                            elem_st3.append(0)
                        ARR_elems_4 = []
                        for el4 in obsh_arr_st4:
                            if el4.id_st == el3.id_:
                                #Создание массива по 4 статье
                                elem_st4 = [el4.code + ' ' + el4.nazv]
                                for i in range(prod):
                                    elem_st4.append(0)
                                #Идем по поиску в общем БДДС
                                for element in arr_BDDS_obsh:
                                    if el4.id_ == element.id_st4:
                                        #Цикл по всей продолжительности проекта
                                        for i, time in enumerate(shapka):
                                            temp = element.mnt + " " + str(element.yr)
                                            #Проверка по времени расходов
                                            if time == temp:
                                                elem_st4[i] += float(element.ds)
                                                elem_st3[i] += float(element.ds)
                                                elem_st2[i] += float(element.ds)
                                                elem_st1[i] += float(element.ds)
                                                break
                                ARR_elems_4.append(elem_st4) #Добавление данных по всему третьему уровню
                        Arr_elems_3.append(elem_st3) #Добавление данных по 3 статье
                        Arr_elems_4.append(ARR_elems_4) #Добавление 4 статьи по каждой статье третьего уровня
                arr_elems_2.append(elem_st2)
                arr_elems_3.append(Arr_elems_3)
                arr_elems_4.append(Arr_elems_4)
        #Добавляем данные по каждой статье
        bdds_res.append(elem_st1)
        for i in range(len(arr_elems_2)):
            bdds_res.append(arr_elems_2[i])
            for j in range(len(arr_elems_3[i])):
                bdds_res.append(arr_elems_3[i][j])
                for k in range(len(arr_elems_4[i][j])):
                    bdds_res.append(arr_elems_4[i][j][k])

    #Берем данные по 4 статье 
    obj_arr_st1 = sql.take_stati4_level1()
    obj_arr_st2 = sql.take_stati4_level2()
    obj_arr_st3 = []
    obj_arr_st4 = []
    for el in obj_arr_st2:
        _arr_ = sql.take_level_down_st3(el.id_)
        for elem in _arr_:
            obj_arr_st3.append(elem)
    for el in obj_arr_st3:
        _arr_ = sql.take_level_down_st4(el.id_)
        for elem in _arr_:
            obj_arr_st4.append(elem)

    #Начинаем проход по объектам строительства
    for el_ in object_str:
        arr_obj = [el_.nazv]
        for i in range(prod):
            arr_obj.append(0)
        #Массивы для сортировки
        arr_elems_1 = []
        arr_elems_2 = []
        arr_elems_3 = []
        arr_elems_4 = []
        #Проходимся по статьям первого уровня
        for el1 in obj_arr_st1:
            elem_st1 = [el1.code + " " + el1.nazv]
            for i in range(prod):
                elem_st1.append(0)
            #Идем по 2 уровню
            Arr_elems_2 = []
            Arr_elems_3 = []
            Arr_elems_4 = []
            for el2 in obj_arr_st2:
                #Ищем подходящие статьи
                if el1.id_ == el2.id_st:
                    elem_st2 = [el2.code + " " + el2.nazv]
                    for i in range(prod):
                        elem_st2.append(0)
                    #Идем по 3 уровню
                    ARR_elems_3 = []
                    ARR_elems_4 = []
                    for el3 in obj_arr_st3:
                        #Ищем подхоядщие статьи
                        if el2.id_ == el3.id_st:
                            elem_st3 = [el3.code + " " + el3.nazv]
                            for i in range(prod):
                                elem_st3.append(0)
                            #Идем по 4 уровню
                            ARR_elements_4 = []
                            for el4 in obj_arr_st4:
                                #Ищем подходящие статьи
                                if el3.id_ == el4.id_st:
                                    elem_st4 = [el4.code + " " + el4.nazv]
                                    for i in range(prod):
                                        elem_st4.append(0)
                                    #Идем по статьям БДДС объекта
                                    for element in arr_BDDS_obj:
                                        if (el4.id_ == element.id_st4) and (el_.id_ == element.id_o):
                                            #Цикл по всей продолжительности проекта
                                            for i, time in enumerate(shapka):
                                                temp = element.mnt + " " + str(element.yr)
                                                #Проверка по времени расходов
                                                if time == temp:
                                                    elem_st4[i] += float(element.ds)
                                                    elem_st3[i] += float(element.ds)
                                                    elem_st2[i] += float(element.ds)
                                                    elem_st1[i] += float(element.ds)
                                                    break
                                    ARR_elements_4.append(elem_st4)
                            ARR_elems_3.append(elem_st3)
                            ARR_elems_4.append(ARR_elements_4)
                    Arr_elems_2.append(elem_st2)
                    Arr_elems_3.append(ARR_elems_3)
                    Arr_elems_4.append(ARR_elems_4)
            arr_elems_4.append(Arr_elems_4)
            arr_elems_3.append(Arr_elems_3)
            arr_elems_2.append(Arr_elems_2)
            arr_elems_1.append(elem_st1)
        #Добавляем все данные по объекту
        bdds_res.append(arr_obj)
        for i in range(len(arr_elems_1)):
            bdds_res.append(arr_elems_1[i])
            for j in range(len(arr_elems_2[i])):
                bdds_res.append(arr_elems_2[i][j])
                for k in range(len(arr_elems_3[i][j])):
                    bdds_res.append(arr_elems_3[i][j][k])
                    for l in range(len(arr_elems_4[i][j][k])):
                        bdds_res.append(arr_elems_4[i][j][k][l])
  
    #Собираем данные по 5, 6, 7
    obsh_arr_st1 = sql.take_obsh_arr567_st1()
    obsh_arr_st2 = sql.take_obsh_arr567_st2()
    obsh_arr_st3 = []
    obsh_arr_st4 = []
    for el in obsh_arr_st2:
        _arr_ = sql.take_level_down_st3(el.id_)
        for elem in _arr_:
            obsh_arr_st3.append(elem)
    for el in obsh_arr_st3:
        _arr_ = sql.take_level_down_st4(el.id_)
        for elem in _arr_:
            obsh_arr_st4.append(elem)

    #Начинаем проход по общим статьям, которые идут после объектов строительства
    for el in obsh_arr_st1:
        #Массивы для сортировки
        arr_elems_2 = []
        arr_elems_3 = []
        arr_elems_4 = []
        elem_st1 = [el.code + ' ' + el.nazv]
        for i in range(prod):
            elem_st1.append(0)
        for el2 in obsh_arr_st2:
            #Проверка подходящей статьи на втором уровне
            if el2.id_st == el.id_:
                Arr_elems_3 = []
                Arr_elems_4 = []
                #Создание массива по 2 статье
                elem_st2 = [el2.code + ' ' + el2.nazv]
                for i in range(prod):
                    elem_st2.append(0)
                for el3 in obsh_arr_st3:
                    #Проверка подходящей статьи на третьем уровне
                    if el3.id_st == el2.id_:
                        #Создание массива по 3 статье
                        elem_st3 = [el3.code + ' ' + el3.nazv]
                        for i in range(prod):
                            elem_st3.append(0)
                        ARR_elems_4 = []
                        for el4 in obsh_arr_st4:
                            if el4.id_st == el3.id_:
                                #Создание массива по 4 статье
                                elem_st4 = [el4.code + ' ' + el4.nazv]
                                for i in range(prod):
                                    elem_st4.append(0)
                                #Идем по поиску в общем БДДС
                                for element in arr_BDDS_obsh:
                                    if el4.id_ == element.id_st4:
                                        #Цикл по всей продолжительности проекта
                                        for i, time in enumerate(shapka):
                                            temp = element.mnt + " " + str(element.yr)
                                            #Проверка по времени расходов
                                            if time == temp:
                                                elem_st4[i] += float(element.ds)
                                                elem_st3[i] += float(element.ds)
                                                elem_st2[i] += float(element.ds)
                                                elem_st1[i] += float(element.ds)
                                                break
                                ARR_elems_4.append(elem_st4) #Добавление данных по всему третьему уровню
                        Arr_elems_3.append(elem_st3) #Добавление данных по 3 статье
                        Arr_elems_4.append(ARR_elems_4) #Добавление 4 статьи по каждой статье третьего уровня
                arr_elems_2.append(elem_st2)
                arr_elems_3.append(Arr_elems_3)
                arr_elems_4.append(Arr_elems_4)
        #Добавляем данные по каждой статье
        bdds_res.append(elem_st1)
        for i in range(len(arr_elems_2)):
            bdds_res.append(arr_elems_2[i])
            for j in range(len(arr_elems_3[i])):
                bdds_res.append(arr_elems_3[i][j])
                for k in range(len(arr_elems_4[i][j])):
                    bdds_res.append(arr_elems_4[i][j][k])

    #Переходим к финансовым организациям - пункт 8.1
    fin_organisation = sql.take_fin_org(id_pr)
    stat_fin_org = []
    #Ищем статьи по 4 уровню в фин.орг
    finorg_arr_st4 = sql.take_st_for_finorg()
    #Добавляем статьи 3 уровня в фин.орг
    finorg_arr_st3 = sql.take_stati_fin_level3()
    #Добавляем все данные БДДС по финансовым организациям этого проекта
    for el in fin_organisation:
        elem = sql.take_stat_fin_org(el.id_)
        for element in elem:
            stat_fin_org.append(element)
    #Переходим на статью 8.5 - по организациям исключениям
    stat_obj_iskl_3ur = sql.take_3_ur_for_85()
    stat_obj_iskl_4ur = sql.take_4_ur_for_85()

    #Начинаем собирать 8 статью 
    arr_elems_1 = ['8 Финансовая деятельность'] #ID = 8
    arr_fin_org = []
    arr_elems_2 = []
    arr_elems_3 = []
    arr_elems_4 = []
    osob_arr_3 = []
    osob_arr_4 = []
    for i in range(prod):
        arr_elems_1.append(0)
    elem_st2 = ['8.1 Кредиты']                  #ID = 60
    for i in range(prod):
        elem_st2.append(0)
    #Идем по финансовым организациям
    for el in fin_organisation:
        elem_obj = [el.nazv]
        for i in range(prod):
            elem_obj.append(0)
        Arr_elems_3 = []
        Arr_elems_4 = []
        for el3 in finorg_arr_st3:
            elem_st3 = [el3.code + " " + el3.nazv]
            for i in range(prod):
                elem_st3.append(0)
            ARR_elems_4 = []
            for el4 in finorg_arr_st4:
                if el4.id_st == el3.id_:
                    elem_st4 = [el4.code + " " + el4.nazv]
                    for i in range(prod):
                        elem_st4.append(0)
                    #Проходимся по записям в статах
                    for elem in stat_fin_org:
                        if (el4.id_ == elem.id_st4) and (elem.id_f_org == el.id_):
                            for i, time in enumerate(shapka):
                                temp = elem.mnt + " " + str(elem.yr)
                                if time == temp:
                                    elem_st4[i] += float(elem.ds)
                                    elem_st3[i] += float(elem.ds)
                                    elem_st2[i] += float(elem.ds)
                                    arr_elems_1[i] += float(elem.ds)
                                    break
                    ARR_elems_4.append(elem_st4)
            Arr_elems_3.append(elem_st3)
            Arr_elems_4.append(ARR_elems_4)
        arr_fin_org.append(elem_obj)   
        osob_arr_3.append(Arr_elems_3)
        osob_arr_4.append(Arr_elems_4) 
    arr_elems_2.append(elem_st2)
    arr_elems_3.append(osob_arr_3)
    arr_elems_4.append(osob_arr_4)

    #Идем по общим в 8 (8.2, 8.3, 8.4)
    arr8_obsh_st2 = sql.take_arr8_obsh_st2()
    arr8_obsh_st3 = sql.take_arr8_obsh_st3()
    arr8_obsh_st4 = []
    for el in arr8_obsh_st3:
        element = sql.take_st_ur_4(el.id_)
        for elem in element:
            arr8_obsh_st4.append(elem)
    for el2 in arr8_obsh_st2:
        Arr_elems_3 = []
        Arr_elems_4 = []
        #Создание массива по 2 статье
        elem_st2 = [el2.code + ' ' + el2.nazv]
        for i in range(prod):
            elem_st2.append(0)
        for el3 in arr8_obsh_st3:
            #Проверка подходящей статьи на третьем уровне
            if el3.id_st == el2.id_:
                #Создание массива по 3 статье
                elem_st3 = [el3.code + ' ' + el3.nazv]
                for i in range(prod):
                    elem_st3.append(0)
                ARR_elems_4 = []
                for el4 in arr8_obsh_st4:
                    if el4.id_st == el3.id_:
                        #Создание массива по 4 статье
                        elem_st4 = [el4.code + ' ' + el4.nazv]
                        for i in range(prod):
                            elem_st4.append(0)
                        #Идем по поиску в общем БДДС
                        for element in arr_BDDS_obsh:
                            if el4.id_ == element.id_st4:
                                #Цикл по всей продолжительности проекта
                                for i, time in enumerate(shapka):
                                    temp = element.mnt + " " + str(element.yr)
                                    #Проверка по времени расходов
                                    if time == temp:
                                        elem_st4[i] += float(element.ds)
                                        elem_st3[i] += float(element.ds)
                                        elem_st2[i] += float(element.ds)
                                        arr_elems_1[i] += float(element.ds)
                                        break
                        ARR_elems_4.append(elem_st4) #Добавление данных по всему третьему уровню
                Arr_elems_3.append(elem_st3) #Добавление данных по 3 статье
                Arr_elems_4.append(ARR_elems_4) #Добавление 4 статьи по каждой статье третьего уровня
        arr_elems_2.append(elem_st2)
        arr_elems_3.append(Arr_elems_3)
        arr_elems_4.append(Arr_elems_4)

    #Проход по 8.5 - исключения из объектов строения
    arr_obj_ = [] 
    elem_st2 = ['8.5 Специальные счета']   #ID = 64
    osob_arr_3 = []
    osob_arr_4 = []
    for i in range(prod):
        elem_st2.append(0)
    #Идем по объектам строения
    for el in object_str:
        elem_obj_ = [el.nazv]
        for i in range(prod):
            elem_obj_.append(0)
        #Идем по статьям
        Arr_elems_3 = []
        Arr_elems_4 = []
        for el3 in stat_obj_iskl_3ur:
            elem_st3 = [el3.code + " " + el3.nazv]
            for i in range(prod):
                elem_st3.append(0)
            ARR_elems_4 = []
            for el4 in stat_obj_iskl_4ur:
                if el4.id_st == el3.id_:
                    elem_st4 = [el4.code + " " + el4.nazv]
                    for i in range(prod):
                        elem_st4.append(0)
                    #Проходимся по статьям
                    for el_ in arr_BDDS_obj:
                        if el_.id_o == el.id_ and el_.id_st4 == el4.id_:
                            for i, time in enumerate(shapka):
                                temp = el_.mnt + " " + str(el_.yr)
                                #Проверка по времени расходов
                                if time == temp:
                                    elem_st4[i] += float(el_.ds)
                                    elem_st3[i] += float(el_.ds)
                                    elem_st2[i] += float(el_.ds)
                                    arr_elems_1[i] += float(el_.ds)
                                    break
                    ARR_elems_4.append(elem_st4)
            Arr_elems_3.append(elem_st3)
            Arr_elems_4.append(ARR_elems_4)
        arr_obj_.append(elem_obj_)
        osob_arr_3.append(Arr_elems_3)
        osob_arr_4.append(Arr_elems_4)
    arr_elems_2.append(elem_st2)
    arr_elems_3.append(osob_arr_3)
    arr_elems_4.append(osob_arr_4)    

    #Сборка в итоговую таблицу блядской 8 статьи
    bdds_res.append(arr_elems_1)
    for i in range(len(arr_elems_2)):
        bdds_res.append(arr_elems_2[i])
        if i == 0:
            for j in range(len(arr_fin_org)):
                bdds_res.append(arr_fin_org[j])
                for k in range(len(arr_elems_3[i][j])):
                    bdds_res.append(arr_elems_3[i][j][k])
                    for l in range(len(arr_elems_4[i][j][k])):
                        bdds_res.append(arr_elems_4[i][j][k][l])
        elif i == (len(arr_elems_2) - 1):
            for j in range(len(arr_obj_)):
                bdds_res.append(arr_obj_[j])
                for k in range(len(arr_elems_3[i][j])):
                    bdds_res.append(arr_elems_3[i][j][k])
                    for l in range(len(arr_elems_4[i][j][k])):
                        bdds_res.append(arr_elems_4[i][j][k][l])
        else:    
            for j in range(len(arr_elems_3[i])):
                bdds_res.append(arr_elems_3[i][j])
                for k in range(len(arr_elems_4[i][j])):
                    bdds_res.append(arr_elems_4[i][j][k])

    #Занимаемся 9ой статьей
    arr_elems_1 = ['9 Поступления от Продажи недвижимости']
    for i in range(prod):
        arr_elems_1.append(0)
    arr_obj_ = []
    arr_elems_2 = []
    arr_elems_3 = []
    arr_elems_4 = []
    obj_arr_st2 = sql.take_2_ur_for_9()
    obj_arr_st3 = sql.take_3_ur_for_9()
    obj_arr_st4 = sql.take_4_ur_for_9()

    #Идем по всему 9ому пункту
    for el_ in object_str:
        elem_obj_ = [el_.nazv]
        Arr2 = []
        Arr3 = []
        Arr4 = []
        for i in range(prod):
            elem_obj_.append(0)
        for el2 in obj_arr_st2:
            Arr_elems_3 = []
            Arr_elems_4 = []
            elem_st2 = [el2.code + " " + el2.nazv]
            for i in range(prod):
                elem_st2.append(0)
            for el3 in obj_arr_st3:
                if el3.id_st == el2.id_:
                    ARR_elems_4 = []
                    elem_st3 = [el3.code + " " + el3.nazv]
                    for i in range(prod):
                        elem_st3.append(0)
                    for el4 in obj_arr_st4:
                        if el4.id_st == el3.id_:
                            elem_st4 = [el4.code + " " + el4.nazv]
                            for i in range(prod):
                                elem_st4.append(0)
                            for elem in arr_BDDS_obj:
                                if (elem.id_st4 == el4.id_) and (elem.id_o == el_.id_):
                                    for i, time in enumerate(shapka):
                                        temp = elem.mnt + " " + str(elem.yr)
                                        #Проверка по времени расходов
                                        if time == temp:
                                            elem_st4[i] += float(elem.ds)
                                            elem_st3[i] += float(elem.ds)
                                            elem_st2[i] += float(elem.ds)
                                            arr_elems_1[i] += float(elem.ds)
                                            break                      
                            ARR_elems_4.append(elem_st4)
                    Arr_elems_3.append(elem_st3)
                    Arr_elems_4.append(ARR_elems_4)
            Arr2.append(elem_st2)
            Arr3.append(Arr_elems_3)
            Arr4.append(Arr_elems_4)
        arr_elems_2.append(Arr2)
        arr_elems_3.append(Arr3)
        arr_elems_4.append(Arr4)            
        arr_obj_.append(elem_obj_)

    #Вводим итоговые данные
    bdds_res.append(arr_elems_1)
    for i in range(len(arr_obj_)):
        bdds_res.append(arr_obj_[i])
        for j in range(len(arr_elems_2[i])):
            bdds_res.append(arr_elems_2[i][j])
            for k in range(len(arr_elems_3[i][j])):
                bdds_res.append(arr_elems_3[i][j][k])
                for l in range(len(arr_elems_4[i][j][k])):
                    bdds_res.append(arr_elems_4[i][j][k][l])

    #Собираем данные по общим статьям исключениям
    obsh_arr_st1 = sql.take_obsh_iskl_last_1()
    obsh_arr_st2 = sql.take_obsh_iskl_last_2()
    obsh_arr_st3 = []
    obsh_arr_st4 = []
    for el in obsh_arr_st2:
        _arr_ = sql.take_level_down_st3(el.id_)
        for elem in _arr_:
            obsh_arr_st3.append(elem)
    for el in obsh_arr_st3:
        _arr_ = sql.take_level_down_st4(el.id_)
        for elem in _arr_:
            obsh_arr_st4.append(elem)

    #Идем по статьям для 10, 11, 12, 13, 14, 15, 16
    arr_elems_1 = []
    arr_elems_2 = []
    arr_elems_3 = []
    arr_elems_4 = []
    for el1 in obsh_arr_st1:
        elem_st1 = [el1.code + " " + el1.nazv]
        for i in range(prod):
            elem_st1.append(0)
        Arr_elems_2 = []
        Arr_elems_3 = []
        Arr_elems_4 = []
        for el2 in obsh_arr_st2:
            ARR_elems_3 = []
            ARR_elems_4 = []
            if el1.id_ == el2.id_st:
                elem_st2 = [el2.code + " " + el2.nazv]
                for i in range(prod):
                    elem_st2.append(0)
                for el3 in obsh_arr_st3:
                    if el3.id_st == el2.id_:
                        Arr_elements_4 = []
                        elem_st3 = [el3.code + " " + el3.nazv]
                        for i in range(prod):
                            elem_st3.append(0)
                        for el4 in obsh_arr_st4:
                            if el4.id_st == el3.id_:
                                elem_st4 = [el4.code + " " + el4.nazv]
                                for i in range(prod):
                                    elem_st4.append(0)
                                for element in arr_BDDS_obsh:
                                    if el4.id_ == element.id_st4:
                                        for i, time in enumerate(shapka):
                                            temp = element.mnt + " " + str(element.yr)
                                            #Проверка по времени расходов
                                            if time == temp:
                                                elem_st4[i] += float(element.ds)
                                                elem_st3[i] += float(element.ds)
                                                elem_st2[i] += float(element.ds)
                                                elem_st1[i] += float(element.ds)
                                                break
                                Arr_elements_4.append(elem_st4)
                        ARR_elems_3.append(elem_st3)
                        ARR_elems_4.append(Arr_elements_4)
                Arr_elems_2.append(elem_st2)
                Arr_elems_3.append(ARR_elems_3)
                Arr_elems_4.append(ARR_elems_4)
        arr_elems_1.append(elem_st1)
        arr_elems_2.append(Arr_elems_2)
        arr_elems_3.append(Arr_elems_3)
        arr_elems_4.append(Arr_elems_4)    
    
    for i in range(len(arr_elems_1)):
        bdds_res.append(arr_elems_1[i])
        for j in range(len(arr_elems_2[i])):
            bdds_res.append(arr_elems_2[i][j])
            for k in range(len(arr_elems_3[i][j])):
                bdds_res.append(arr_elems_3[i][j][k])
                for l in range(len(arr_elems_4[i][j][k])):
                    bdds_res.append(arr_elems_4[i][j][k][l])

    #Считаем сумму по статьям
    bdds_result = []
    #Чуток меняем шапку
    new_shapka = [bdds_res[0][0], 'Итого']
    for i in range(1, len(bdds_res[0])):
        new_shapka.append(bdds_res[0][i])
    bdds_result.append(new_shapka)
    #Выводим новую таблицу 
    for i in range(1, len(bdds_res)):
        elem = [bdds_res[i][0], 0]
        for j in range(1, len(bdds_res[i])):
            elem.append(bdds_res[i][j])
            elem[1] += bdds_res[i][j]
        bdds_result.append(elem)

    #Меняем нули на пустую строку
    for i in range(1, len(bdds_result)):
        for j in range(1, len(bdds_result[i])):
            if bdds_result[i][j] == 0:
                bdds_result[i][j] = ''

    filipath = create_empty_excel(data=bdds_result, filename=("bdds_"+ name_table + ".xlsx"), sheet_name="БДДС")


def create_empty_excel(data, filename: str, sheet_name):
    # Проверяем, существует ли папка, и создаем, если нет
    if not os.path.exists('excel_files'):
        os.makedirs('excel_files')
    
    filepath = os.path.join('excel_files', filename)
    
    # Создаем ExcelWriter
    with pd.ExcelWriter(filepath, engine='xlsxwriter') as excel_writer:
        # Создаем DataFrame
        df = pd.DataFrame(data=data)
        # Записываем в файл
        df.to_excel(excel_writer, index=False, header=False, sheet_name=sheet_name)
        
        # Получаем текущий рабочий лист и книгу
        worksheet = excel_writer.sheets[sheet_name]
        workbook = excel_writer.book
        
        # Формат для первой строки
        header_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#F4ECE5',
            'border': 1
        })

        # Форматы для остального содержимого
        style_1 = workbook.add_format({'bg_color': '#B08968', 'border': 1})
        style_2 = workbook.add_format({'bg_color': '#DDB892', 'border': 1})
        style_3 = workbook.add_format({'bg_color': '#E6CCB2', 'border': 1})
        style_4 = workbook.add_format({'bg_color': '#F4ECE5', 'border': 1})
        style_5 = workbook.add_format({'bg_color': '#B7424F', 'border': 1})
        default_style = workbook.add_format({'border': 1})

        # Определяем ширину столбцов по всей таблице
        for col_num, col_data in enumerate(zip(*data)):  # Транспонируем data, чтобы обработать по столбцам
            max_length = max([len(str(val)) for val in col_data if pd.notnull(val)], default=0)
            worksheet.set_column(col_num, col_num, max_length + 2)
        
        # Закрепляем первую строку
        worksheet.freeze_panes(1, 0)
        
        # Применяем формат к первой строке
        for col_num, cell_value in enumerate(data[0]):
            worksheet.write(0, col_num, cell_value, header_format)
        
        # Применяем цветовую палитру для остальных строк
        for row_num, row_data in enumerate(data[1:], start=1):  # Пропускаем первую строку
            first_cell_value = row_data[0] if row_data else ""
            if isinstance(first_cell_value, str):
                if re.match(r'^\d+ ', first_cell_value):  # Число и пробел
                    row_format = style_1
                elif re.match(r'^\d+\.\d+ ', first_cell_value):  # Число.число и пробел
                    row_format = style_2
                elif re.match(r'^\d+\.\d+\.\d+ ', first_cell_value):  # Число.число.число и пробел
                    row_format = style_3
                elif re.match(r'^\d+\.\d+\.\d+\.\d+ ', first_cell_value):  # Число.число.число и пробел
                    row_format = style_4
                elif (
                    re.match(r'^Корпус №\d+$', first_cell_value) or  # "Корпус №цифра"
                    re.match(r'^(СОШ|ДОУ|Пождепо|Медучреждение)', first_cell_value)  # Начинается с ключевых слов
                ):
                    row_format = style_5
                else:
                    row_format = default_style
            else:
                row_format = default_style

            # Записываем строку с применением формата
            for col_num, cell_value in enumerate(row_data):
                worksheet.write(row_num, col_num, cell_value, row_format)
    
    return filepath

make_bdds(18)
