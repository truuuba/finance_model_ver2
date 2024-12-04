from connect_db import sql
from transliterate import translit
import os
import pandas as pd
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

def create_tabel_bdr(id_pr):
    #Берем данные по названию проекта
    n_t = sql.take_name_pr(id_pr)
    name_table = translit(n_t, language_code='ru', reversed=True)

    #Время старта строительства
    mnt_start = sql.take_mnt_start(id_pr) 
    yr_start = sql.take_yr_start(id_pr)

    #Вытаскиваем объекты строительства
    object_str = sql.take_obj_for_ppo(id_pr)

    #Информация по продолжительности от ГПР
    prod = sql.take_prod_proj(id_pr)
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

    '''
    Вытаскиваем общие статьи 1,2,3,5
    '''
    #Поиск общих статей
    obsh_st = sql._take_obsh_stati_(id_pr)
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
        if BDR_obsh != False:
            arr_BDR_obsh.append(BDR_obsh)
        #Вытащить данные по расходам в BDR_iskl
        BDR_iskl = sql.take_BDR_iskl(id_obsh=el.id_)
        if BDR_iskl != False:
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

    bdr_res = [] #итоговая таблица
    bdr_res.append(shapka)
    #Начинаем собирать массивы под общие статьи
    for el in arr_st_1:
        #Проверка под общие статы
        if el.id_ == 1 or el.id_ == 2 or el.id_ == 3 or el.id_ == 5:
            #Массивы для сортировки
            arr_elems_2 = []
            arr_elems_3 = []
            elem_st1 = [el.code + ' ' + el.nazv]
            for i in range(prod):
                elem_st1.append(0)
            for el2 in arr_st_2:
                #Проверка подходящей статьи на втором уровне
                if el2.id_st == el.id_:
                    Arr_elems_3 = []
                    #Создание массива по 2 статье
                    elem_st2 = [el2.code + ' ' + el2.nazv]
                    for i in range(prod):
                        elem_st2.append(0)
                    for el3 in arr_st_3:
                        #Проверка подходящей статьи на третьем уровне
                        if el3.id_st == el2.id_:
                            #Создание массива по 3 статье
                            elem_st3 = [el3.code + ' ' + el3.nazv]
                            for i in range(prod):
                                elem_st3.append(0)
                            for elem in obsh_st:
                                #Проверка на общие статьи
                                if el3.id_ == elem.id_o:
                                    for e in arr_BDR_obsh:
                                        for element in e:
                                            #Проверка на БДР и общих статей
                                            if element.id_st == elem.id_:
                                                #Цикл по всей продолжительности проекта
                                                for i, time in enumerate(shapka):
                                                    temp = element.mnt + " " + str(element.yr)
                                                    #Проверка по времени расходов
                                                    if time == temp:
                                                        elem_st3[i] = float(element.plan_ds)
                                                        elem_st2[i] += float(element.plan_ds)
                                                        elem_st1[i] += float(element.plan_ds)
                            Arr_elems_3.append(elem_st3) #Данные по 2 конкретной статье
                    arr_elems_2.append(elem_st2) #Массив 2 статей
                    arr_elems_3.append(Arr_elems_3) #Массив 3 статей внутри вторых
            bdr_res.append(elem_st1)
            for i in range(len(arr_elems_2)):
                bdr_res.append(arr_elems_2[i])
                for j in range(len(arr_elems_3[i])):
                    bdr_res.append(arr_elems_3[i][j])

    '''
    Разбираем объекты строительства
    '''
    #Вытаскиваем статьи по объектам
    obj_stati = []
    #Статьи БДР
    BDR_obj_stati = []
    for el in object_str:
        objects_stati = sql.take_obj_stati(id_obj=el.id_)
        obj_stati.append(objects_stati)
        BDR_obj = []
        for el in objects_stati:
            elem = sql.take_data_BDR_obj_t(id_st_obj=el.id_)
            BDR_obj.append(elem)
        BDR_obj_stati.append(BDR_obj)
    #Статьи по уровням в объектах
    arr_obj_2st = sql.take_list_obj()
    arr_obj_3st = []
    for el in arr_obj_2st:
        elem = sql.take_list_st_3(el.id_)
        arr_obj_3st.append(elem) 

    arr = ['4 Объекты строительства']
    for i in range(prod):
        arr.append(0)
    bdr_res.append(arr)

    #Проходим по объектам строительства
    for i, el in enumerate(object_str):
        arr_obj = [el.nazv]
        for j in range(prod):
            arr_obj.append(0)
        #Массивы для сортировки
        arr_elems_2 = []
        arr_elems_3 = []
        #Проходимся по статьям 2 уровня
        for el2 in arr_obj_2st:
            Arr_elems_3 = []
            #Создание массива по 2 статье
            elem_st2 = [el2.code + ' ' + el2.nazv]
            for j in range(prod):
                elem_st2.append(0)
            for e in arr_obj_3st:
                for el3 in e:
                    if el2.id_ == el3.id_st:
                        #Создание массива по 3 статье
                        elem_st3 = [el3.code + ' ' + el3.nazv]
                        for j in range(prod):
                            elem_st3.append(0)
                        #статьи объектов 
                        for elem in obj_stati[i]:
                            #Проверка статей объектов
                            if elem.id_o == el3.id_:
                                for elements in BDR_obj_stati[i]:
                                    for element in elements:
                                        #Проверка по статьям БДР
                                        if element.id_st == elem.id_:
                                            #Цикл по всей продолжительности проекта
                                            for j, time in enumerate(shapka):
                                                temp = element.mnt + " " + str(element.yr)
                                                #Проверка по времени расходов
                                                if time == temp:
                                                    elem_st3[j] = round(float(element.plan_ds), 2)
                                                    elem_st2[j] += round(float(element.plan_ds), 2)
                        Arr_elems_3.append(elem_st3) #Данные по 2 конкретной статье                            
            arr_elems_2.append(elem_st2) #Массив 2 статей
            arr_elems_3.append(Arr_elems_3) #Массив 3 статей внутри вторых
        bdr_res.append(arr_obj)
        for i in range(len(arr_elems_2)):
            bdr_res.append(arr_elems_2[i])
            for j in range(len(arr_elems_3[i])):
                bdr_res.append(arr_elems_3[i][j])

    #Начинаем считать поступления
    arr = ['Поступления']
    for i in range(prod):
        arr.append(0)
    bdr_res.append(arr)
    pattern = r".*Корпус.*"
    #Выделяем доходы по каждому объекту строительства
    for el in object_str:
        match_obj = re.match(pattern, el.nazv)
        if match_obj:
            arr_nazv = [el.nazv]
            #Название объекта
            for i in range(prod):
                arr_nazv.append(0)
            #Разбираемся с жилыми
            mass_PPO_obj = sql.take_data_PPO(el.id_) 
            arr_jil = [el.nazv + ' Квартиры']
            for i in range(prod):
                arr_jil.append(0)
            for elem in mass_PPO_obj:
                temp = elem.mnt + " " + str(elem.yr)
                for i in range(1, len(shapka)): 
                    if temp == shapka[i]:
                        arr_nazv[i] += round(float(elem.dohod), 2)
                        arr_jil[i] += round(float(elem.dohod), 2)
            #Смотрим составляющие
            patt = r".*Коммерческие помещения.*"
            arr_s_obj = sql.take_sost_obj_ppo(el.id_)
            arrs_sost_obj = []
            for elem in arr_s_obj:
                arr_kom = [el.nazv + " " + elem.nazv]
                for i in range(prod):
                    arr_kom.append(0)
                match_sost_obj = re.match(patt, elem.nazv)
                #Если коммерческие помещения
                if match_sost_obj:
                    arr_s_PPO = sql.take_PPO_sost(elem.id_)
                    for element in arr_s_PPO:
                        temp = element.mnt + " " + str(element.yr)
                        for i in range(len(shapka)):
                            if temp == shapka[i]:
                                arr_kom[i] += round(float(element.dohod), 2)
                                arr_nazv[i] += round(float(element.dohod), 2)
                #Если машиноместа или кладовые помещения
                else:
                    #Начинаем красиво искать момент, с которого начинаются продажи
                    st = 0
                    temp = el.m_st + " " + str(el.yr_st)
                    for i in range(1, len(shapka)):
                        if temp == shapka[i]:
                            st = i
                            break
                    #Полноценно начинаем заниматься вводом данных
                    sum_sost = elem.cnt * elem.stoim
                    a = float(sum_sost)/(prod - st)
                    for i in range(st, len(shapka)):
                        arr_kom[i] += round(a, 2)
                        arr_nazv[i] += round(a, 2)
                arrs_sost_obj.append(arr_kom)
            bdr_res.append(arr_nazv)
            bdr_res.append(arr_jil)
            for i in range(len(arrs_sost_obj)):
                bdr_res.append(arrs_sost_obj[i])

    '''
    Разбираем исключения в общих статьях
    '''
    for el in arr_st_1:
        #Проверка под общие статы
        if el.id_ == 6 or el.id_ == 7 or el.id_ == 10 or el.id_ == 11 or el.id_ == 12 or el.id_ == 13 or el.id_ == 14 or el.id_ == 15:
            #Массивы для сортировки
            arr_elems_2 = []
            arr_elems_3 = []
            elem_st1 = [el.code + ' ' + el.nazv]
            for i in range(prod):
                elem_st1.append(0)
            for el2 in arr_st_2:
                #Проверка подходящей статьи на втором уровне
                if el2.id_st == el.id_:
                    Arr_elems_3 = []
                    #Создание массива по 2 статье
                    elem_st2 = [el2.code + ' ' + el2.nazv]
                    for i in range(prod):
                        elem_st2.append(0)
                    for el3 in arr_st_3:
                        #Проверка подходящей статьи на третьем уровне
                        if el3.id_st == el2.id_:
                            #Создание массива по 3 статье
                            elem_st3 = [el3.code + ' ' + el3.nazv]
                            for i in range(prod):
                                elem_st3.append(0)
                            for elem in obsh_st:
                                #Проверка на общие статьи
                                if el3.id_ == elem.id_o:
                                    for element in arr_BDR_iskl:
                                        #Проверка на БДР и общих статей
                                        if element.id_st == elem.id_:
                                            #Цикл по всей продолжительности проекта
                                            for i in range(len(shapka)-1):
                                                a = float(element.ds)/prod
                                                elem_st3[i+1] = round(a, 2)
                                                elem_st2[i+1] += round(a, 2)
                                                elem_st1[i+1] += round(a, 2)
                            Arr_elems_3.append(elem_st3) #Данные по 2 конкретной статье
                    arr_elems_2.append(elem_st2) #Массив 2 статей
                    arr_elems_3.append(Arr_elems_3) #Массив 3 статей внутри вторых
            bdr_res.append(elem_st1)
            for i in range(len(arr_elems_2)):
                bdr_res.append(arr_elems_2[i])
                for j in range(len(arr_elems_3[i])):
                    bdr_res.append(arr_elems_3[i][j])

    #Добавляем общий подсчет
    bdr_result = []
    #Чуток меняем шапку
    new_shapka = [bdr_res[0][0], 'Итого']
    for i in range(1, len(bdr_res[0])):
        new_shapka.append(bdr_res[0][i])
    bdr_result.append(new_shapka)
    #Меняем остальную табличку
    for i in range(1, len(bdr_res)):
        arr = [bdr_res[i][0]]
        arr.append(0)
        for j in range(1, len(bdr_res[i])):
            arr[1] += bdr_res[i][j]
            arr.append(bdr_res[i][j])
        bdr_result.append(arr)

    #Меняем нули 
    for i in range(1, len(bdr_result)):
        for j in range(1, len(bdr_result[i])):
            if bdr_result[i][j] == 0:
                bdr_result[i][j] = ''

    #Создаем файл
    filepath = create_empty_excel(bdr_result, "bdr_" + name_table + ".xlsx", "Таблица БДР")

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
            'bg_color': '#E3EADE',
            'border': 1
        })
        
        # Форматы для остального содержимого
        style_1 = workbook.add_format({'bg_color': '#84A98C', 'border': 1})
        style_2 = workbook.add_format({'bg_color': '#B9C8B7', 'border': 1})
        style_3 = workbook.add_format({'bg_color': '#E3EADE', 'border': 1})
        style_4 = workbook.add_format({'bg_color': '#9A8C98', 'border': 1})
        style_5 = workbook.add_format({'bg_color': '#C9ADA7', 'border': 1})
        style_6 = workbook.add_format({'bg_color': '#F2E9E4', 'border': 1})
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
                elif first_cell_value.strip() == "Поступления":  # "Поступления"
                    row_format = style_4
                elif (
                    re.match(r'^Корпус №\d+$', first_cell_value) or  # "Корпус №цифра"
                    re.match(r'^(СОШ|ДОУ|Пождепо|Медучреждение)', first_cell_value)  # Начинается с ключевых слов
                ):
                    row_format = style_5
                elif re.match(r'^Корпус №\d+ ', first_cell_value):  # Корпус №цифра-пробел
                    row_format = style_6
                else:
                    row_format = default_style
            else:
                row_format = default_style

            # Записываем строку с применением формата
            for col_num, cell_value in enumerate(row_data):
                worksheet.write(row_num, col_num, cell_value, row_format)
    
    return filepath

#https://coolors.co/4a4e69-726d81-9a8c98-b29da0-c9ada7-d4bcb7-decbc6-e8dad5-f2e9e4
#https://coolors.co/e3eade-d7ded2-cad2c5-b9c8b7-a7bea9-9fb9a2-96b49b-84a98c-6b917e-52796f
