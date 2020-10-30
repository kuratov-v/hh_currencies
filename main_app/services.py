import xml.etree.ElementTree as ET
import urllib.request

import datetime

from config.settings import CBR_URL


def get_currencies():
    val_list = []
    url = CBR_URL + 'XML_daily.asp'
    response = urllib.request.urlopen(url).read()
    tree = ET.fromstring(response)
    for t in tree:
        item = {'id': t.attrib['ID'],
                'name': t.find('./Name').text,
                'char_code': t.find('./CharCode').text}
        val_list.append(item)
    return val_list


def get_unique_code_from_iso_char_code(char_code):
    val_list = get_currencies()
    for item in val_list:
        if item['char_code'] == char_code:
            return item['id']


def get_values(date1, date2, unique_code):
    date1 = datetime.date(*[int(i) for i in date1.split('-')]).strftime('%d/%m/%Y')
    date2 = datetime.date(*[int(i) for i in date2.split('-')]).strftime('%d/%m/%Y')

    url = f'{CBR_URL}XML_dynamic.asp?date_req1={date2}&date_req2={date1}&VAL_NM_RQ={unique_code}'
    response = urllib.request.urlopen(url).read()
    tree = ET.fromstring(response)
    value1 = float(tree[0].find('./Value').text.replace(',', '.'))
    value2 = float(tree[-1].find('./Value').text.replace(',', '.'))
    return value1, value2


def get_biggest_date(date1, date2):
    _date1 = datetime.date(*[int(i) for i in date1.split('-')])
    _date2 = datetime.date(*[int(i) for i in date2.split('-')])
    return [date1, date2] if _date1 > _date2 else [date2, date1]


def get_difference(date1, date2, char_code):
    unique_code = get_unique_code_from_iso_char_code(char_code)
    date1, date2 = get_biggest_date(date1, date2)
    try:
        value1, value2 = get_values(date1, date2, unique_code)
    except IndexError:
        return {"error": 'There are no values for the given code in the specified range'}
    else:
        response = {'currency_code': char_code,
                    'date_1': date1,
                    'value_1': value1,
                    'date_2': date2,
                    'value_2': value2,
                    'difference': value1 - value2}
        return response
