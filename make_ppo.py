import os
import pandas as pd
from transliterate import translit
import math
from connect_db import sql
import re

#Класс для подсчета коэффициентов
class season_k:
    def __init__(self, mounth, koef, cnt):
        self.cnt = cnt + 1
        self.mounth = mounth
        self.koef = koef

def create_tabel_ppo(id_pr, prov_create):
    '''
    Жилые
    '''
    #Берем данные по названию проекта
    n_t = sql.take_name_pr(id_pr)
    name_table = translit(n_t, language_code='ru', reversed=True)
    sht_name = []

    #Вытаксиваем данные с объектов строительства по проекту
    obj_str_ = sql.take_obj_for_ppo(id_pr=id_pr)
    obj_str = []
    patt = r".*Корпус.*"
    for i in range(len(obj_str_)):
        match_obj = re.match(patt, obj_str_[i].nazv)
        if match_obj:
            obj_str.append(obj_str_[i])

    arr_ppo = []
    for i in range(len(obj_str)):
        arr_ppo.append(cout_ppo(obj_str[i].prod_pl, obj_str[i].stoim, obj_str[i].prod, obj_str[i].m_st, obj_str[i].kv_cnt, obj_str[i].yr_st, obj_str[i].d_ip, obj_str[i].d_rassr, obj_str[i].d_full, obj_str[i].vsnos_r, obj_str[i].sr_pl_rassr, id_obj=obj_str[i].id_, prov_table=True))
        sht_name.append("Квартиры " + obj_str[i].nazv)

    '''
    Коммерческие помещения
    '''
    patt = r".*Коммерческие помещения.*"
    for i in range(len(obj_str)):
        sost_obj = sql.take_sost_obj_ppo(obj_str[i].id_)
        for el in sost_obj:
            match_sost = re.match(patt, el.nazv)
            if match_sost:
                arr_ppo.append(el.prod_pl, el.stoim, obj_str[i].prod, obj_str[i].m_st, el.cnt, obj_str[i].yr_st, el.dol_ip, el.dol_rass, el.full_pl, el.vsn_r, el.sr_pl_rassr, el.id_obj, False)
                sht_name.append("Коммерческие помещения " + obj_str[i].nazv)

    if prov_create:
        filepath = create_empty_excel(filename=('ppo_' + name_table + '.xlsx'), data=arr_ppo, sheet_name = sht_name)

#Создаем файлик для вноса данных 
def create_empty_excel(data: list, filename: str, sheet_name):
    if not os.path.exists('excel_files'):
        os.makedirs('excel_files')
    
    filepath = os.path.join('excel_files', filename)
    with pd.ExcelWriter(filepath, engine='xlsxwriter') as excel_writer:
        for i in range(len(data)):
            df = pd.DataFrame(data=data[i])
            # Записываем данные в Excel без индекса и с нужным именем листа
            df.to_excel(excel_writer, index=False, header=False, sheet_name=sheet_name[i])
            
            # Получаем доступ к текущему рабочему листу
            worksheet = excel_writer.sheets[sheet_name[i]]
            workbook = excel_writer.book

            # Устанавливаем ширину столбцов на основе максимальной длины текста в каждом столбце
            for idx, col in enumerate(df.columns):
                max_length = max(df[col].astype(str).map(len).max(), len(str(col))) + 2
                worksheet.set_column(idx, idx, max_length)

            # Формат для сетки (черные границы)
            border_format = workbook.add_format({'border': 1, 'border_color': '#000000'})
            
            # Применяем сетку для указанных диапазонов
            worksheet.conditional_format(0, 0, 4, 1, {'type': 'no_blanks', 'format': border_format})  
            worksheet.conditional_format(6, 0, 12, 1, {'type': 'no_blanks', 'format': border_format}) 
            worksheet.conditional_format(14, 0, len(df) + 14, len(df.columns) - 1, {'type': 'no_blanks', 'format': border_format})

            # Форматы для цветного выделения
            first_cell_format = workbook.add_format({'bg_color': '#FFA07A', 'bold': True})    # Цвет для первой ячейки
            second_range_format = workbook.add_format({'bg_color': '#87CEEB', 'bold': True})  # Цвет для второго диапазона
            summary_format = workbook.add_format({'bg_color': '#98FB98', 'bold': True})       # Цвет для строки с "Итого поступления"
            
            # Применение цветного выделения
            # 1. Выделение 1-й ячейки в первом столбце
            worksheet.conditional_format(0, 0, 0, 0, {'type': 'cell', 'criteria': 'not equal to', 'value': '""', 'format': first_cell_format})
            
            # 2. Выделение диапазонов
            worksheet.conditional_format(1, 0, 4, 0, {'type': 'cell', 'criteria': 'not equal to', 'value': '""', 'format': second_range_format})   # С 2 по 5 строку 1 столбца
            worksheet.conditional_format(6, 0, 12, 0, {'type': 'cell', 'criteria': 'not equal to', 'value': '""', 'format': second_range_format})  # С 7 по 13 строку 1 столбца
            
            # 3. Применение формата "Итого поступления" без повторной записи данных
            for row_num in range(len(df)):
                if str(df.iloc[row_num, 0]).startswith("Итого поступления"):
                    # Применение стиля ко всем ячейкам строки с "Итого поступления" в первом столбце
                    for col_num in range(len(df.columns)):
                        worksheet.write(row_num, col_num, df.iloc[row_num, col_num], summary_format)  # Записываем значение с форматом
    return filepath

# Считаем ППО
def cout_ppo(ploshad, st_m, prod, mounth_start, cnt_kv, year, _pr_ipot, _pr_rassr, _pr_full, _pr_rassr_vznos, sr_plat_rassr, id_obj, prov_table):
    # Проценты
    pr_ipot = _pr_ipot/100
    pr_rassr = _pr_rassr/100
    pr_full = _pr_full/100
    pr_rassr_vznos = _pr_rassr_vznos/100

    virochka = ploshad * st_m
    sr_st_kv = math.ceil(virochka/cnt_kv)
    vir_per_m = float(virochka) * 0.01 #Добавить продажи в первый месяц
    ddu = [0] * prod
    koefs = make_koef()
    ind_m = 0
    for i in range(len(koefs)):
        if koefs[i].mounth == mounth_start:
            ddu[0] = round(koefs[i].koef * vir_per_m)
            if i != 11:
                ind_m = i + 1

    proc_y = [round(100/math.ceil(prod/12), 2)] * math.ceil(prod/12)
    proc_y[0] += 100 - sum(proc_y)
    
    #Считаем продажи
    prod_years = []
    for i in range(len(proc_y)):
        prod_years.append(float(virochka) * (proc_y[i] / 100)) # Добавить продажи по годам

    prod_posl_m = prod_years[len(prod_years) - 1] * 0.005

    #Средние продажи
    sr_prod = []
    for i in range(len(prod_years)):
        if i == 0:
            sr_prod.append(round((prod_years[0] - vir_per_m) / 11))
        elif i == (len(prod_years) - 1):
            sr_prod.append(round((prod_years[len(prod_years) - 1] - prod_posl_m) / 11))
        else:
            sr_prod.append(round(prod_years[i] / 12))

    # Считаем ДДУ
    cnt = 0
    for i in range(1, prod):
        if i == (prod - 1):
            ddu[i] = round(koefs[ind_m].koef * prod_posl_m) #ДДУ тоже добавить
        else:
            ddu[i] = round(koefs[ind_m].koef * sr_prod[cnt])
        if (i / 11) == 0:
            cnt += 1
        if ind_m == 11:
            ind_m = 0
        else:
            ind_m += 1

    # Считаем денюжки и долги
    money = []
    dolg = []
    ddu_rassr = []
    for i in range(len(ddu)):
        money.append(round(ddu[i]*pr_ipot+ddu[i]*pr_full+ddu[i]*pr_rassr*pr_rassr_vznos)) #И это добавить
        dolg.append(round(ddu[i]-money[i])) #И это добавить
        ddu_rassr.append(round(dolg[i]/(sr_st_kv * pr_rassr_vznos), 2)) #И это добавить

    #Создаем таблицу для вычислений
    table_ppo = [0] * prod
    for i in range(prod):
        table_ppo[i] = [0] * prod

    cnt = 12
    for i in range(prod):
        summa = 0
        for j in range(1, prod):
            if j == cnt:
                table_ppo[i][j] = round(dolg[i] - summa, 3)
                break
            elif j > i:
                table_ppo[i][j] = round(ddu_rassr[i] * sr_plat_rassr, 3)
            summa += table_ppo[i][j]    
        if cnt < (prod - 1):
            cnt += 1
    
    #Ищем месяц, который нужен
    arr = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    ind_m = 0
    for i in range(1, len(arr)):
        if arr[i] == mounth_start:
            ind_m = i

    #Создаем таблицу для экселя (До правок)
    ppo = [0] * (prod + 2)
    for i in range(prod + 2):
        ppo[i] = [0] * (prod + 1)

    ppo[0][0] = '$'
    for j in range(1, prod+1):
        ppo[0][j] = money[j-1]

    for i in range(1, prod+2):
        if i == (prod+1):
            ppo[i][0] = 'Итого поступления $'
        else:
            ppo[i][0] = arr[ind_m]
        for j in range(1, prod+1):
            if i == (prod + 1):
                ppo[i][j] += money[j-1]
            else:
                ppo[i][j] = table_ppo[i-1][j-1]
                ppo[prod + 1][j] += table_ppo[i-1][j-1] 
        if ind_m == 11:
            ind_m = 0
        else:
            ind_m += 1

    #Создаем таблицу в эксель (итоговую)
    t_ppo = []
    array = ['Изменяемые параметры']
    for i in range(len(ppo[0]) - 1):
        array.append("")
    t_ppo.append(array)
    array = ['Срок строительства', prod]
    array2 = ['Площадь', ploshad]
    array3 = ['Средняя цена за кв.м.', st_m]
    array4 = ['Выручка, т.р.', virochka]
    array5 = ['', '']
    array6 = ['Кол-во квартир в доме', cnt_kv]
    array7 = ['Средняя стоимость квартиры', sr_st_kv]    
    array8 = ['Средний ежем. платеж по расср.', sr_plat_rassr]
    array9 = ['Доля договоров по ипотеке', str(_pr_ipot) + '%']
    array10 = ['Доля договоров с рассрочкой платежа', str(_pr_rassr) + '%']
    array11 = [r'100% оплата', str(_pr_full) + '%']
    array12 = ['Первоначальный взнос по рассрочке', str(_pr_rassr_vznos) + '%']
    for i in range(len(t_ppo[0]) - 2):
        array.append("")
        array2.append("")
        array3.append("")
        array4.append("")
        array5.append("")
        array6.append("")
        array7.append("")
        array8.append("")
        array9.append("")
        array10.append("")
        array11.append("")
        array12.append("")
    t_ppo.append(array)
    t_ppo.append(array2)
    t_ppo.append(array3)
    t_ppo.append(array4)
    t_ppo.append(array5)
    t_ppo.append(array6)
    t_ppo.append(array7)
    t_ppo.append(array8)
    t_ppo.append(array9)
    t_ppo.append(array10)
    t_ppo.append(array11)
    t_ppo.append(array12)
    t_ppo.append(array5)             

    shapka_mnt = ['']
    shapka_yr = ['']
    shapka_koefs = ['']
    arr = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    ind_m = 0
    for i in range(1, len(arr)):          # Шапка по времени таблицы
        if mounth_start == arr[i]:
            ind_m = i
            break
    for i in range(prod):
        shapka_mnt.append(arr[ind_m])
        shapka_yr.append(year)
        shapka_koefs.append(koefs[ind_m].koef)
        if ind_m == 11:
            ind_m = 0
            year += 1
        else:
            ind_m += 1
    t_ppo.append(shapka_yr)
    t_ppo.append(shapka_mnt)
    t_ppo.append(shapka_koefs)

    # Добавляем данные в ППО
    if prov_table:
        len_ = len(ppo)
        sql.prov_PPO(id_obj=id_obj)
        for i in range(1, len(ppo[len_-1])):
            sql.input_ppo(id_obj=id_obj, yr=shapka_yr[i], mnt=shapka_mnt[i], dohod=ppo[len_-1][i])
    else:
        len_ = len(ppo)
        sql.prov_s_PPO(id_obj)
        for i in range(1, len(ppo[len_-1])):
            sql.input_ppo_sost(id_s_obj=id_obj, yr=shapka_yr[i], mnt=shapka_mnt[i], dohod=ppo[len_-1][i])

    arr = []
    arr.append('ДДУ') # Считаем ДДУ
    for j in range(1, prod+1):
        arr.append(ddu[j-1])
    t_ppo.append(arr)

    arr = []
    arr.append('$') # Считаем деньги
    for j in range(1, prod+1):
        arr.append(money[j-1])
    t_ppo.append(arr)

    arr = []
    arr.append('Долг') # Считаем долг
    for j in range(1, prod+1):
        arr.append(dolg[j-1])
    t_ppo.append(arr)

    arr = []
    arr.append('ДДУ с рассрочкой') # Считаем ДДУ с рассрочкой
    for j in range(1, prod+1):
        arr.append(ddu_rassr[j-1])
    t_ppo.append(arr)

    for i in range(1, len(ppo)): #Добавляем таблицу ППО
        arr = []
        for j in range(len(ppo[i])):
            arr.append(ppo[i][j])
        t_ppo.append(arr)

    # Вывод ППО для теста
    for i in range(len(t_ppo)):
        print(t_ppo[i])

    return t_ppo

#Подсчет коэффициентов
def make_koef():
    arr = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    k = [0.89, 0.98, 1.01, 0.99, 0.93, 0.73, 0.76, 1.03, 1.07, 1.05, 1.28, 1.28]
    koefs =[]
    for i in range(len(arr)):
        s_k = season_k(mounth=arr[i], koef=k[i], cnt=i)
        koefs.append(s_k)
    return koefs

