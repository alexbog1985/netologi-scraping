
from bs4 import BeautifulSoup
import requests
from fake_headers import Headers

header = Headers(browser="chrome",
                 os="win",
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


response = requests.get('https://spb.hh.ru/search/vacancy', headers=header, params=params)

soup = BeautifulSoup(response.text, 'lxml')
div_tags = soup.find_all('div', class_='serp-item serp-item_link serp-item-redesign')
res = []
for tag in div_tags:
    link = tag.find('a', class_='bloko-link')
    salary = tag.find('span', class_='bloko-text') # надо доделать!!!
    print(salary.text if '$' in salary.text else '')
    print(link['href'])
    res.append(tag.text)
print(len(res))


if __name__ == '__main__':
    pass