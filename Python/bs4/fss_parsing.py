from urllib.request import urlopen
# from urllib.parse import urlparse
import wget
from bs4 import BeautifulSoup
import re
from urllib.error import HTTPError, URLError


def down_rep(v32, v64):
    # x32 = 'https://lk.fss.ru/' + v32
    x64 = 'https://lk.fss.ru/' + v64
    print('Загрузка версии 64:')
    wget.download(x64, f'/Users/Оператор/Desktop/АРМ МСР/{v64}')
    # print('\nЗагрузка версии 32:')
    # wget.download(x32, f'/Users/Оператор/Desktop/АРМ МСР/{v32}')


def vs_version(last, now):
    if last != now:
        print(f'Вышла новая версия от {now_version}')
        downloading = input('Хотите скачать? (д/н)\n')
        if downloading == 'д':
            down_rep(v32, v64)
            print(input('Загрузка прошла успешно!\n--Нажмите Enter--'))
    else:
        print('Новой версии нет')


try:
    html = urlopen('https://lk.fss.ru/ers.html')  # .read().decode('utf-8')
    # try_parser = '{}://{}'.format(urlparse('https://lk.fss.ru/ers.html').scheme,
    #                               urlparse('https://lk.fss.ru/ers.html').netloc)
    # print(try_parser)

    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
except HTTPError as e:
    print('Ошибка загрузки страницы, страница не существует.')
    print(f'{e}')
except URLError as e:
    print(f'Не корректная ссылка {e}')
except Exception as ex:
    print(f'Возникала ошибка при загрузке страницы\n{ex}')

try:
    link_div = soup.find('div', {'id': 'cabinets-inner-next'}).find('div')
    # print(link_div)
    LAST_VERSION = '06.04.2022'
    now_version = link_div.get_text()[-10:]
    v32, v64 = [x.attrs['href'][1:] for x in link_div.find_all('a', href=re.compile('^(/)(.)*(.exe)'))]
    vs_version(LAST_VERSION, now_version)
except AttributeError:
    print('Не найден селектор. Проверьте структуру страницы!')
except NameError:
    pass
