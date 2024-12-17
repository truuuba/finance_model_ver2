import os
import pandas as pd
from transliterate import translit
from connect_db import sql

""" сортировка вставками """
def insertion_sort(unsorted):
    n = len(unsorted)
    # итерация по неотсортированным массивам
    for i in range(1, n):
        # получаем значение элемента
        val = unsorted[i] 
        # записываем в hole индекс i
        hole = i
        # проходим по массиву в обратную сторону, пока не найдём элемент больше текущего
        while hole > 0 and unsorted[hole - 1].id_ > val.id_: 
            # переставляем элементы местами , чтобы получить правильную позицию
            unsorted[hole] = unsorted[hole - 1]
            # делаем шаг назад
            hole -= 1
        # вставляем значение на верную позицию
        unsorted[hole] = val 

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
    #Общие статьи
    obsh_st = sql._take_obsh_stati_(id_pr)

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
    
    #Берем статьи по уровням - сначала в общих
    obsh_arr_st1 = []
    obsh_arr_st2 = []
    obsh_arr_st3 = []
    obsh_arr_st4 = []
    prov_st4 = []
    for el in arr_BDDS_obsh:
        elem4 = sql.found_st_4_ur(el.id_st4)
        for e in elem4:
            if not (e.code in prov_st4):
                obsh_arr_st4.append(e)
                prov_st4.append(e.code)
    prov_st3 = []
    for el in obsh_arr_st4:
        elem3 = sql.found_st_3_ur(el.id_)
        if not (elem3.code in prov_st3):
            obsh_arr_st3.append(elem3)
            prov_st3.append(elem3.code)
    prov_st2 = []
    for el in obsh_arr_st3:
        elem2 = sql.found_st_2_ur(el.id_)
        for e in elem2:
            if not (e.code in prov_st2):
                obsh_arr_st2.append(e)
                prov_st2.append(e.code)
    prov_st1 = []
    for el in obsh_arr_st2:
        elem1 = sql.found_st_1_ur(el.id_)
        for e in elem1:
            if not (e.code in prov_st1):
                obsh_arr_st1.append(e)
                prov_st1.append(e.code)

    #Надо отсортировать массив по возрастанию на основе айдишников
    insertion_sort(obsh_arr_st1)
    insertion_sort(obsh_arr_st2)
    insertion_sort(obsh_arr_st3)
    insertion_sort(obsh_arr_st4)
    
    #Пойдем по объектам строительства - тут все статьи в одной куче
    obj_arr_st1 = []
    obj_arr_st2 = []
    obj_arr_st3 = []
    obj_arr_st4 = []
    prov_st4 = []
    for el in arr_BDDS_obj:
        elem4 = sql.found_st_4_ur(el.id_st4)
        for e in elem4:
            if not (e.code in prov_st4):
                obj_arr_st4.append(e)
                prov_st4.append(e.code)
    prov_st3 = []
    for el in obj_arr_st4:
        elem3 = sql.found_st_3_ur(el.id_)
        if not (elem3.code in prov_st3):
            obj_arr_st3.append(elem3)
            prov_st3.append(elem3.code)
    prov_st2 = []
    for el in obj_arr_st3:
        elem2 = sql.found_st_2_ur(el.id_)
        for e in elem2:
            if not(e.code in prov_st2):
                obj_arr_st2.append(e)
                prov_st2.append(e.code) 
    prov_st1 = []
    for el in obj_arr_st2:
        elem1 = sql.found_st_1_ur(el.id_)
        for e in elem2:
            if not(e.code in prov_st1):
                obj_arr_st1.append(e)
                prov_st1.append(e.code)  

    #Еще посортируем объекты строительства
    insertion_sort(obj_arr_st1)
    insertion_sort(obj_arr_st2)
    insertion_sort(obj_arr_st3)
    insertion_sort(obj_arr_st4)

    #Начинаем формировать таблицу БДДС - до первого столкновения с объектами строительства
    bdds_res = [] 
    bdds_res.append(shapka)
    #Проходимся по общим статьям
    for el in obsh_arr_st1:
        #Проверяем айди по статам до объектов
        if el.id_ == 1 or el.id_ == 2 or el.id_ == 3:
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
                                                    if el4.param == "поступление":
                                                        elem_st4[i] += float(element.ds)
                                                        elem_st3[i] += float(element.ds)
                                                        elem_st2[i] += float(element.ds)
                                                        elem_st1[i] += float(element.ds)
                                                    else:
                                                        elem_st4[i] -= float(element.ds)
                                                        elem_st3[i] -= float(element.ds)
                                                        elem_st2[i] -= float(element.ds)
                                                        elem_st1[i] -= float(element.ds)
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
                            elem_st3 = [el3.code + " " + el3.code]
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
                                        if el4.id_ == element.id_st4:
                                            #Цикл по всей продолжительности проекта
                                            for i, time in enumerate(shapka):
                                                temp = element.mnt + " " + str(element.yr)
                                                #Проверка по времени расходов
                                                if time == temp:
                                                    if el4.param == "поступление":
                                                        elem_st4[i] += float(element.ds)
                                                        elem_st3[i] += float(element.ds)
                                                        elem_st2[i] += float(element.ds)
                                                        elem_st1[i] += float(element.ds)
                                                    else:
                                                        elem_st4[i] -= float(element.ds)
                                                        elem_st3[i] -= float(element.ds)
                                                        elem_st2[i] -= float(element.ds)
                                                        elem_st1[i] -= float(element.ds)
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
    
    #Начинаем проход по общим статьям, которые идут после объектов строительства
    

    for el in obsh_arr_st1:
        #Проверяем айди по статам до объектов
        if el.id_ == 5 or el.id_ == 6 or el.id_ == 7:
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
                                                    if el4.param == "поступление":
                                                        elem_st4[i] += float(element.ds)
                                                        elem_st3[i] += float(element.ds)
                                                        elem_st2[i] += float(element.ds)
                                                        elem_st1[i] += float(element.ds)
                                                    else:
                                                        elem_st4[i] -= float(element.ds)
                                                        elem_st3[i] -= float(element.ds)
                                                        elem_st2[i] -= float(element.ds)
                                                        elem_st1[i] -= float(element.ds)
                                                    break
                                    ARR_elems_4.append(elem_st4) #Добавление данных по всему третьему уровню
                            Arr_elems_3.append(elem_st3) #Добавление данных по 3 статье
                            Arr_elems_4.append(ARR_elems_4) #Добавление 4 статьи по каждой статье третьего уровня
                arr_elems_2.append(elem_st2)
                arr_elems_3.append(Arr_elems_3)
                arr_elems_4.append(Arr_elems_4)
            #Добавляем данные по каждой статье
            bdds_res.append(elem_st1)
            print(elem_st1)
            for i in range(len(arr_elems_2)):
                bdds_res.append(arr_elems_2[i])
                print(arr_elems_2[i])
                for j in range(len(arr_elems_3[i])):
                    bdds_res.append(arr_elems_3[i][j])
                    print(arr_elems_3[i][j])
                    for k in range(len(arr_elems_4[i][j])):
                        bdds_res.append(arr_elems_4[i][j][k])
                        print(arr_elems_4[i][j][k])

    #Переходим к финансовым организациям - пункт 8.1
    fin_organisation = sql.take_fin_org(id_pr)
    stat_fin_org = []
    #Ищем статьи по 4 уровню в фин.орг
    finorg_arr_st4 = sql.take_st_for_finorg()
    #Добавляем статьи 3 уровня в фин.орг
    prov_st3 = []
    finorg_arr_st3 = []
    for el in finorg_arr_st4:
        elem = sql.found_st_3_ur(el.id_)
        if not (elem.code in prov_st3):
            finorg_arr_st3.append(elem)
            prov_st3.append(elem.code)
    #Добавляем все данные БДДС по финансовым организациям этого проекта
    for el in fin_organisation:
        elem = sql.take_stat_fin_org(el.id_)
        for element in elem:
            stat_fin_org.append(element)
    
    #Переходим на статью 8.5 - по организациям исключениям
    stat_obj_iskl = []
    for el in object_str:
        elem = sql.take_BDDS_obj_iskl(el.id_)
        for element in elem:
            stat_obj_iskl.append(element)
    stat_obj_iskl_3ur = sql.take_3_ur_for_85()
    stat_obj_iskl_4ur = sql.take_4_ur_for_85()

    #Начинаем собирать 8 статью 
    arr_elems_1 = ['8 Финансовая деятельность'] #ID = 8
    arr_fin_org = []
    arr_elems_2 = []
    arr_elems_3 = []
    arr_elems_4 = []
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
                                    if el4.param == "поступление":
                                        elem_st4[i] += float(elem.ds)
                                        elem_st3[i] += float(elem.ds)
                                        elem_st2[i] += float(elem.ds)
                                        arr_elems_1[i] += float(elem.ds)
                                    else:
                                        elem_st4[i] -= float(elem.ds)
                                        elem_st3[i] -= float(elem.ds)
                                        elem_st2[i] -= float(elem.ds)
                                        arr_elems_1[i] -= float(elem.ds)
                                    break
                    ARR_elems_4.append(elem_st4)
            Arr_elems_3.append(elem_st3)
            Arr_elems_4.append(ARR_elems_4)
        arr_fin_org.append(elem_obj)    
    arr_elems_2.append(elem_st2)
    arr_elems_3.append(Arr_elems_3)
    arr_elems_4.append(Arr_elems_4)

    #Идем по общим в 8 (8.2, 8.3, 8.4)
    arr8_obsh_st2 = sql.take_arr8_obsh_st2()
    arr8_obsh_st3 = sql.take_arr8_obsh_st3()
    arr8_obsh_st4 = []
    for el in arr8_obsh_st3:
        element = sql.take_st_ur_4(el.id_)
        for elem in element:
            arr8_obsh_st4.append(elem)
    arr_bdds_obsh_iskl = sql.take_bdds_obsh_iskl(id_pr)
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
                        for element in arr_bdds_obsh_iskl:
                            if el4.id_ == element.id_st4:
                                #Цикл по всей продолжительности проекта
                                for i, time in enumerate(shapka):
                                    temp = element.mnt + " " + str(element.yr)
                                    #Проверка по времени расходов
                                    if time == temp:
                                        if el4.param == "поступление":
                                            elem_st4[i] += float(element.ds)
                                            elem_st3[i] += float(element.ds)
                                            elem_st2[i] += float(element.ds)
                                            arr_elems_1[i] += float(element.ds)
                                        else:
                                            elem_st4[i] -= float(element.ds)
                                            elem_st3[i] -= float(element.ds)
                                            elem_st2[i] -= float(element.ds)
                                            arr_elems_1[i] -= float(element.ds)
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
                    for el_ in stat_obj_iskl:
                        if el_.id_o == el.id_ and el_.id_st4 == el4.id_:
                            for i, time in enumerate(shapka):
                                temp = el_.mnt + " " + str(el_.yr)
                                #Проверка по времени расходов
                                if time == temp:
                                    if el4.param == "поступление":
                                        elem_st4[i] += float(el_.ds)
                                        elem_st3[i] += float(el_.ds)
                                        elem_st2[i] += float(el_.ds)
                                        arr_elems_1[i] += float(el_.ds)
                                    else:
                                        elem_st4[i] -= float(el_.ds)
                                        elem_st3[i] -= float(el_.ds)
                                        elem_st2[i] -= float(el_.ds)
                                        arr_elems_1[i] -= float(el_.ds)
                                    break
                    ARR_elems_4.append(elem_st4)
            Arr_elems_3.append(elem_st3)
            Arr_elems_4.append(ARR_elems_4)
        arr_obj_.append(elem_obj_)
    arr_elems_2.append(elem_st2)
    arr_elems_3.append(Arr_elems_3)
    arr_elems_4.append(Arr_elems_4)    

    #Сборка в итоговую таблицу блядской 8 статьи
    bdds_res.append(arr_elems_1)
    for i in range(len(arr_elems_2)):
        bdds_res.append(arr_elems_2[i])
        if i == 0:
            for j in range(len(fin_organisation)):
                bdds_res.append(fin_organisation[j])
                for k in range(len(arr_elems_3[i])):
                    bdds_res.append(arr_elems_3[i][k])
                    for l in range(len(arr_elems_4[i][k])):
                        bdds_res.append(arr_elems_4[i][k][l])
        elif i == (len(arr_elems_2) - 1):
            for j in range(len(arr_obj_)):
                bdds_res.append(arr_obj_[j])
                for k in range(len(arr_elems_3[i])):
                    bdds_res.append(arr_elems_3[i][k])
                    for l in range(len(fin_organisation)):
                        bdds_res.append(arr_elems_4[i][k][l])
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
    stat_obj_iskl_2ur = sql.take_2_ur_for_9()
    stat_obj_iskl_3ur = sql.take_3_ur_for_9()
    stat_obj_iskl_4ur = sql.take_4_ur_for_9()
    #Все данные по проектам 9 пункте по объектам исключения
    datas_obj_iskl = []
    for el in object_str:
        data_iskl_ = sql.take_data_obj_iskl_9(el.id_)
        for elem in data_iskl_:
            datas_obj_iskl.append(elem)

    #Идем по всему 9ому пункту
    for el_ in object_str:
        elem_obj_ = [el_.nazv]
        Arr2 = []
        Arr3 = []
        Arr4 = []
        for i in range(prod):
            elem_obj_.append(0)
        for el2 in stat_obj_iskl_2ur:
            Arr_elems_3 = []
            Arr_elems_4 = []
            elem_st2 = [el2.code + " " + el2.nazv]
            for i in range(prod):
                elem_st2.append(0)
            for el3 in stat_obj_iskl_3ur:
                if el3.id_st == el2.id_:
                    ARR_elems_4 = []
                    elem_st3 = [el3.code + " " + el3.nazv]
                    for i in range(prod):
                        elem_st3.append(0)
                    for el4 in stat_obj_iskl_4ur:
                        if el4.id_st == el3.id_:
                            elem_st4 = [el4.code + " " + el4.nazv]
                            for i in range(prod):
                                elem_st4.append(0)
                            for elem in datas_obj_iskl:
                                if elem.id_st4 == el4.id_:
                                    for i, time in enumerate(shapka):
                                        temp = elem.mnt + " " + str(elem.yr)
                                        #Проверка по времени расходов
                                        if time == temp:
                                            if el4.param == "поступление":
                                                elem_st4[i] += float(elem.ds)
                                                elem_st3[i] += float(elem.ds)
                                                elem_st2[i] += float(elem.ds)
                                                arr_elems_1[i] += float(elem.ds)
                                            else:
                                                elem_st4[i] -= float(elem.ds)
                                                elem_st3[i] -= float(elem.ds)
                                                elem_st2[i] -= float(elem.ds)
                                                arr_elems_1[i] -= float(elem.ds)
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
    iskl_arr_st1 = sql.take_obsh_iskl_last_1()
    iskl_arr_st2 = sql.take_obsh_iskl_last_2()
    iskl_arr_st3 = sql.take_obsh_iskl_last_3()
    iskl_arr_st4 = sql.take_obsh_iskl_last_4()
    data_iskl_obsh_ = sql.BDDS_data_obsh_iskl(id_pr)

    #Идем по статьям для 10, 11, 12, 13, 14, 15, 16
    arr_elems_1 = []
    arr_elems_2 = []
    arr_elems_3 = []
    arr_elems_4 = []
    for el1 in iskl_arr_st1:
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
                                                if el4.param == "поступление":
                                                    elem_st4[i] += float(element.ds)
                                                    elem_st3[i] += float(element.ds)
                                                    elem_st2[i] += float(element.ds)
                                                    elem_st1[i] += float(element.ds)
                                                else:
                                                    elem_st4[i] -= float(element.ds)
                                                    elem_st3[i] -= float(element.ds)
                                                    elem_st2[i] -= float(element.ds)
                                                    elem_st1[i] -= float(element.ds)
                                                break
                                Arr_elements_4.append(elem_st4)
                        ARR_elems_3.append(elem_st3)
                        ARR_elems_4.append(Arr_elements_4)
                Arr_elems_2.append(elem_st2)
                Arr_elems_3.append(ARR_elems_3)
                Arr_elems_4.append(ARR_elems_4)
        for el2 in iskl_arr_st2:
            if el1.id_ == el2.id_st:
                ARR_elems_3 = []
                ARR_elems_4 = []
                elem_st2 = [el2.code + " " + el2.nazv]
                for i in range(prod):
                    elem_st2.append(0)
                for el3 in iskl_arr_st3:
                    if el3.id_st == el2.id_:
                        Arr_elements_4 = []
                        elem_st3 = [el3.code + " " + el3.nazv]
                        for i in range(prod):
                            elem_st3.append(0)
                        for el4 in iskl_arr_st4:
                            if el4.id_st == el3.id_:
                                elem_st4 = [el4.code + " " + el4.nazv]
                                for i in range(prod):
                                    elem_st4.append(0)
                                for element in data_iskl_obsh_:
                                    if el4.id_ == element.id_st4:
                                        for i, time in enumerate(shapka):
                                            temp = element.mnt + " " + str(element.yr)
                                            #Проверка по времени расходов
                                            if time == temp:
                                                if el4.param == "поступление":
                                                    elem_st4[i] += float(element.ds)
                                                    elem_st3[i] += float(element.ds)
                                                    elem_st2[i] += float(element.ds)
                                                    elem_st1[i] += float(element.ds)
                                                else:
                                                    elem_st4[i] -= float(element.ds)
                                                    elem_st3[i] -= float(element.ds)
                                                    elem_st2[i] -= float(element.ds)
                                                    elem_st1[i] -= float(element.ds)
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

    '''
    for i in range(len(bdds_res)):
        print(bdds_res[i])
    '''

make_bdds(17)
