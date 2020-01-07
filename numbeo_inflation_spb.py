import re
import csv
import requests


class Category(object):
    def __init__(self, name, prices_by_years):
        self.name = name
        self.prices_by_years = prices_by_years
        self.inflation_dict = dict()

        self.evaluate_inflation()

    def evaluate_inflation(self):
        for year in self.years_iterator(reverse=True):
            prev_year_price = self.get_price_for_year(year-1)
            if not prev_year_price:
                break
            this_year_price = self.get_price_for_year(year)

            inflation = round(float(this_year_price) / prev_year_price * 100 - 100, 2)
            self.inflation_dict[year] = inflation

    def count_years(self):
        return len(self.prices_by_years)

    def years_iterator(self, reverse=False):
        years_ = list(self.prices_by_years.keys())
        years = list(sorted(years_, reverse=reverse))
        for year in years:
            yield year

    def get_price_for_year(self, year):
        return self.prices_by_years.get(year)

    def get_inflation_for_year(self, year):
        return self.inflation_dict.get(year)

    def inflation_arithmetic_mean(self):
        inflation_values = list(self.inflation_dict.values())
        return round(float(sum(inflation_values)) / len(inflation_values), 2)

    def inflation_weighted_arithmetic_mean(self, formula=1):
        basic_weight = 100
        if formula == 1:
            weight_reducer = lambda x: float(x)*0.8
        else:
            weight_reducer = lambda x: max(x - 20, 0)
        cur_weight = basic_weight

        weight_sum = 0
        inflation_sum = 0

        for year in self.years_iterator(reverse=True):

            inflation = self.get_inflation_for_year(year)
            if inflation is None:
                break

            inflation_sum += inflation*cur_weight
            weight_sum += cur_weight

            cur_weight = weight_reducer(cur_weight)

        return round(float(inflation_sum) / weight_sum, 2)



class CategoriesUtils(object):
    @staticmethod
    def get_max_years_count(categories):
        return max(map(lambda c: c.count_years(), categories))

        
def get_categories():

    url  = "https://www.numbeo.com/cost-of-living/historical-data?"
    url += "itemId=101&itemId=100&itemId=228&itemId=224&itemId=60&itemId=66&"
    url += "itemId=64&itemId=62&itemId=110&itemId=118&itemId=121&itemId=14&"
    url += "itemId=19&itemId=17&itemId=15&itemId=11&itemId=16&itemId=113&"
    url += "itemId=9&itemId=12&itemId=8&itemId=119&itemId=111&itemId=112&"
    url += "itemId=115&itemId=116&itemId=13&itemId=27&itemId=26&itemId=29&"
    url += "itemId=28&itemId=114&itemId=6&itemId=4&itemId=5&itemId=3&itemId=2&"
    url += "itemId=1&itemId=7&itemId=105&itemId=106&itemId=44&itemId=40&itemId=42&"
    url += "itemId=24&itemId=20&itemId=18&itemId=109&itemId=108&itemId=107&itemId=206&"
    url += "itemId=25&itemId=32&itemId=30&itemId=33&city_id=6146&name_city_id=&currency=RUB"

    resp = requests.get(url)
    text = resp.text

    categories = list()

    head_body_pairs = re.findall(r'<table[^>]*?id=\"tier_\d+\"[^>]*?>.*?<thead>(.*?)</thead>.*?<tbody>(.*?)</tbody>', text, re.S)

    for head, body in head_body_pairs:

        heads_ = re.findall(r'<div[^>]*?class[^>]*?=[^>]*?"font_in_table_headers"[^>]*?>(.*?)</div>', head, re.S)
        heads_ = list(map(lambda x: x.replace("<br/>", ""), heads_))
        heads = list(map(lambda x: x.replace("&amp;", "&"), heads_))

        body_lines = list()
        lines = re.findall(r'<tr>(.*?)</tr>', body, re.S)
        for line in lines:
            line_values_ = re.findall(r'<td[^>]*?>(.*?)</td>', line, re.S)
            line_values = list(map(lambda x: float(x) if x != "-" else x, line_values_))
            body_lines.append(line_values)

        for i in range(len(heads)):
            if i == 0:
                continue

            year_price_dict = dict()
            for body_line in body_lines:
                if body_line[i] != "-":
                    year_price_dict[int(body_line[0])] = body_line[i]

            category = Category(heads[i], year_price_dict)
            categories.append(category)

    return categories


def dump_to_csv(categories):
    lines = list()
    max_years_count = CategoriesUtils.get_max_years_count(categories)
    for i in range(2+max_years_count+1+3):
        lines.append(list())

    for category in categories:
        lines[0] += [category.name, '', '']
        lines[1] += ["year", 'price', 'inflation']

        cnt = 0
        for year in category.years_iterator(reverse=True):
            inflation_ = category.get_inflation_for_year(year)
            if not inflation_:
                inflation = ''
            else:
                inflation = "{}%".format(inflation_)
            lines[2+cnt] += [year, "{} р.".format(category.get_price_for_year(year)), inflation]
            cnt += 1
        for i in range(cnt, max_years_count):
            lines[2+i] += ['','','']

        lines[2+max_years_count+1] += ["Mean", '', '{}%'.format(category.inflation_arithmetic_mean())]
        lines[2+max_years_count+2] += ["Weighted mean -20%", '', '{}%'.format(category.inflation_weighted_arithmetic_mean(formula=1))]
        lines[2+max_years_count+3] += ["Weighted mean -20", '', '{}%'.format(category.inflation_weighted_arithmetic_mean(formula=2))]

        for i in range(2+max_years_count+1+3):
            lines[i] += ['']

    with open('export.csv', mode='w') as export_file:
        for line in lines:
            for value in line[:-1]:
                # v = '_' + str(value) + '_' if value != '' else ''
                v = str(value)
                export_file.write(v)
                export_file.write(";")
            export_file.write(v)
            export_file.write("\n")


def main():
    categories = get_categories()
    dump_to_csv(categories)

if __name__ == "__main__":
    main()
