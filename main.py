import requests
from config import email, password
from bs4 import BeautifulSoup
import time
from openpyxl import load_workbook


def main():
    url = 'https://www.vesselfinder.com/api/is/ts/login'
    url_2 = 'https://www.vesselfinder.com/ru/user-profile'
    url_3 = 'https://www.vesselfinder.com'

    headers = {'Accept': '*/*',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64;'
                             ' x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/104.0.5112.124 '
                             'YaBrowser/22.9.3.888 Yowser/2.5 Safari/537.36'
               }
    p = {'email': email,
         'password': password,
         'rememberMe': 'true'
         }

    with requests.session() as session:
        res = session.post(url, data=p, headers=headers)
        app = session.get(url_2, headers=headers)

        print(res.text, app.text)

        count = 1
        while count < 50:
            print(f'стр - {count}')
            try:
                url = f"https://www.vesselfinder.com/vessels?page={count}"

                req = session.get(url, headers=headers)
                soup = BeautifulSoup(req.text, "html.parser")

                d = soup.find_all(class_="v1")
                for i in d:
                    i = str(i).split()[3].split('"')[1]
                    with open("SSS.txt", "a", encoding="utf-8") as file:  ### получаем список ссылок
                        file.write(i + '\n')
                count += 1
            except:
                print('problem')

        try:
            with open('SSS.txt', 'r', encoding='utf-8') as file:
                file_s = file.readlines()
                count = 1
                for i in file_s:
                    i = url_3 + i.replace('\n', '')

                    req = session.get(i, headers=headers)
                    soup = BeautifulSoup(req.text, "html.parser")

                    h_1 = soup.find(class_="title")
                    title = soup.find_all('td', class_="n3")
                    resault = soup.find_all('td', class_="v3")

                    fn = '123.xlsx'
                    wb = load_workbook(fn)
                    ws = wb['Аркуш1']
                    ws.append([h_1.text, f'{title[3].text}-{resault[3].text}', f'{title[6].text}-{resault[6].text}',
                               f'{title[8].text}-{resault[8].text}', f'{title[9].text}-{resault[9].text}'])
                    wb.save(fn)
                    wb.close()

                    print("корабль -", count)
                    count += 1
        except:
            print("error")


if __name__ == '__main__':
    main()
