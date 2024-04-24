from bs4 import BeautifulSoup
import requests
from fake_headers import Headers

header = Headers(browser="chrome",
                 os="mac",
                 headers=True,
                 ).generate()

params = {'L_save_area': 'true',
          'text': '(python and django) or (python and flask)',
          'excluded_text': '',
          'area': '1',
          'area': '2',
          'salary': '',
          'currency_code': 'USD',
          'experience': 'doesNotMatter',
          'order_by': 'relevance',
          'search_period': '0',
           'items_on_page': '20',
          'descriptionsearch_field': 'description',
          'hhtmFrom': 'vacancy_search_filter'
          }


def get_pages(pages=4):
    div_tags_lst = []
    for page in range(pages):
        response = requests.get('https://spb.hh.ru/search/vacancy', headers=header, params=params)
        if response.status_code == 200:
            bs = BeautifulSoup(response.text, 'lxml')
            params['page'] = page
            print(bs.find('h1'))
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
            link = tag.find('a', class_='bloko-link')
            salary = tag.find('span', class_='bloko-header-section-2')
            company = tag.find('div', class_='vacancy-serp-item__meta-info-company')
            print(company.text)
            print(salary.text if salary else 'Зарлата не указана')
            print(link['href'])
            res.append(tag.text)
    print(len(res))


if __name__ == '__main__':
        scrap(get_pages())
