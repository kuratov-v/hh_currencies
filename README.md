# Тестовое задание 


### [GET] localhost:8000/api 
#### Возвращает список валют
```
{
"currencies":[
    {"id":"R01010",
     "name":"Австралийский доллар",
     "char_code":"AUD"},
    {"id":"R01020A",
     "name":"Азербайджанский манат",
     "char_code":"AZN"}
    ]
}
```

#### При указании query_params возвращает курс за первую дату, курс за вторую дату и разницу между ними.
###### date1, date2 - даты в формате (YYYY-MM-DD)
###### char_code - символьный код (EUR)
```
example localhost:8000/api?date1=2020-12-12&date2=2020-10-12&char_code=USD

Response:
{
"success":{
    "currency_code":"USD",
    "date_1":"2020-12-12",
    "value_1":77.0239,
    "date_2":"2020-10-12",
    "value_2":79.3323,
    "difference":-2.308400000000006
    }
}
```

