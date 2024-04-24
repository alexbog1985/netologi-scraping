import requests
import json
from bs4 import BeautifulSoup
from fake_headers import Headers

header = Headers(browser="chrome",
                 os="mac",
                 headers=True,
                 ).generate()

params = {'L_save_area': 'true',
          'text': '(python and django) or (python and flask)',
          'excluded_text': '',
          'area': ['1', '2'],
          'salary': '',
          'currency_code': 'USD',
          'experience': 'doesNotMatter',
          'order_by': 'publication_time',
          'search_period': '0',
           'items_on_page': '20',
          'descriptionsearch_field': 'description',
          'hhtmFrom': 'vacancy_search_filter'
          }


def get_pages(pages=2):
    div_tags_lst = []
    for page in range(pages):
        response = requests.get('https://spb.hh.ru/search/vacancy', headers=header, params=params)
        if response.status_code == 200:
            bs = BeautifulSoup(response.text, 'lxml')
            params['page'] = page
            tags = bs.find_all('div', class_='vacancy-serp-item-body') 
            if tags:
                div_tags_lst.append(tags)
        else:
            print(f'Ошибка соединения: {response.status_code}')
    return div_tags_lst


def scrap(div_tags_lst):
    res = []
    for div_tags in div_tags_lst:
        for tag in div_tags:
            link = tag.find('a', class_='bloko-link').text
            pre_salary = tag.find('span', class_='bloko-header-section-2')
            salary = pre_salary.text if pre_salary else 'Зарплата не указана'
            company = tag.find('div', class_='vacancy-serp-item__meta-info-company').text
            pre_city = tag.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
            city = pre_city.split(',')[0]
            res.append({'link': link, 'salary': salary.replace(u'\u202f', ' '), 'company': company.replace(u'\xa0', ' '), 'city': city})
    print(len(res))
    return res

def save_json(data):
    with open('vacancies.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
        data = scrap(get_pages())
        save_json(data)
