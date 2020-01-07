# numbeo_inflation
Tool to evaluate inflation according to prices people see

# How To
1. скачать проект
2. `pip install requests`
3. запустить скрипт
4. Результат сохранится в файл `export.csv`
5. Для того чтобы было более удобно ориентироваться на название прокута можно подсматривать [СЮДА](https://www.numbeo.com/cost-of-living/historical-data?itemId=101&itemId=100&itemId=228&itemId=224&itemId=60&itemId=66&itemId=64&itemId=62&itemId=110&itemId=118&itemId=121&itemId=14&itemId=19&itemId=17&itemId=15&itemId=11&itemId=16&itemId=113&itemId=9&itemId=12&itemId=8&itemId=119&itemId=111&itemId=112&itemId=115&itemId=116&itemId=13&itemId=27&itemId=26&itemId=29&itemId=28&itemId=114&itemId=6&itemId=4&itemId=5&itemId=3&itemId=2&itemId=1&itemId=7&itemId=105&itemId=106&itemId=44&itemId=40&itemId=42&itemId=24&itemId=20&itemId=18&itemId=109&itemId=108&itemId=107&itemId=206&itemId=25&itemId=32&itemId=30&itemId=33&city_id=6146&name_city_id=&currency=RUB) или [СЮДА](https://clck.ru/LjVjn).

## Numbeo.com
Numbeo.com - сайт, где обычные люди заполняют информацию о ценах в их городе на разные сервисы и продукты. От продуктов питания, до средней зарплаты.

## Идея
На number.com можно получить историю цен по городу. (Cost of Living -> Historical Data in a City by Year). 
Данный проект позволяет выкачать данные по городу Санкт-Петербург в файл формата CSV.
Для каждого года высчитывается процент инфляции относительно предыдущего. Также для каждого типа сервиса/продукта высчитывается средняя арифметическая инфляция и взвешенная средняя арифметическая по 2 формулам. 

## Формулы взвешенных средних арифметических:
1. Каждый год вес уменьшается на 20%
2. Самый последний год вес 100. Каждый последующий уменьшается на 20.
