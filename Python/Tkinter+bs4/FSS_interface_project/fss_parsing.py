from urllib.request import urlopen
# from urllib.parse import urlparse
import wget
from bs4 import BeautifulSoup
import re
from urllib.error import HTTPError, URLError


class ParsingFss:
    def version_in_file(self):
        try:
            with open("fss.version", 'r+') as file_version:
                fss_version = file_version.readlines()
                return fss_version[0]
        except FileNotFoundError:
            with open("fss.version", "w+") as file_version:
                file_version.write("06.04.2022")
            return self.version_in_file()

    def check_version_fss(self, version):
        try:
            html = urlopen('https://lk.fss.ru/ers.html')
            soup = BeautifulSoup(html, 'html.parser')
        except HTTPError as e:
            return (False, f'Ошибка загрузки страницы, страница не существует.\n{e}')
        except URLError as e:
            return (False, f'Не корректная ссылка или нет интернета {e}')
        except Exception as ex:
            return (False, f'Возникала ошибка при загрузке страницы\n{ex}')

        try:
            link_div = soup.find('div', {'id': 'cabinets-inner-next'}).find('div')
            # print(link_div)
            last_version = version
            now_version = link_div.get_text()[-10:]
            v32, v64 = [x.attrs['href'][1:] for x in link_div.find_all('a', href=re.compile('^(/)(.)*(.exe)'))]
        except AttributeError as e:
            return (False, f'Не найден селектор. Проверьте структуру страницы!\n{e}')

        if last_version != now_version:
            return (True, f'Новая версия от {now_version}', v32, v64, now_version)
        else:
            return (True, 'Новой версии нет!', v32, v64, now_version)

    def downoading_fss_32(self, directory, x32):
        x32 = f"https://lk.fss.ru/{x32}"
        wget.download(x32, directory)

    def downoading_fss_64(self, directory, x64):
        x64 = f"https://lk.fss.ru/{x64}"
        wget.download(x64, directory)

    def change_version_in_file(self, version):
        with open("fss.version", "w+") as file_version:
            file_version.write(version)
