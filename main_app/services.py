import xml.etree.ElementTree as ET
import urllib.request

import datetime

from django.core.exceptions import ObjectDoesNotExist

from config.settings import CBR_URL
from .models import Currency


def get_currencies():
    if not Currency.objects.all():
        url = CBR_URL + 'XML_daily.asp'
        response = urllib.request.urlopen(url).read()
        tree = ET.fromstring(response)
        for t in tree:
            Currency.objects.create(id=t.attrib['ID'],
                                    name=t.find('./Name').text,
                                    char_code=t.find('./CharCode').text)
    return Currency.objects.all()


def get_values(date1, date2, unique_code):
    date1 = date1.strftime('%d/%m/%Y')
    date2 = date2.strftime('%d/%m/%Y')

    url = f'{CBR_URL}XML_dynamic.asp?date_req1={date1}&date_req2={date2}&VAL_NM_RQ={unique_code}'
    response = urllib.request.urlopen(url).read()
    tree = ET.fromstring(response)
    value1 = float(tree[0].find('./Value').text.replace(',', '.'))
    value2 = float(tree[-1].find('./Value').text.replace(',', '.'))
    return value1, value2


def validation_date(date1, date2):
    date1 = datetime.date(*[int(i) for i in date1.split('-')])
    date2 = datetime.date(*[int(i) for i in date2.split('-')])
    return [date1, date2] if date1 < date2 else [date2, date1]


def get_difference(date1, date2, char_code):
    char_code = char_code.upper()
    if not date1 or not date2 or not char_code:
        return {"error": "Fields must not be empty"}

    try:
        date1, date2 = validation_date(date1, date2)
    except ValueError:
        return {"error": "Date validation error"}

    try:
        unique_code = Currency.objects.get(char_code=char_code).id
    except ObjectDoesNotExist:
        return {"error": 'No currency with this code'}

    try:
        value1, value2 = get_values(date1, date2, unique_code)
    except IndexError:
        return {"error": 'There are no values for the given code in the specified range'}
    else:
        return {'currency_code': char_code,
                'date_1': date1,
                'value_1': value1,
                'date_2': date2,
                'value_2': value2,
                'difference': value2 - value1}
