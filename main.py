import requests
from bs4 import BeautifulSoup as bs
import pytools
import authorization

LOGIN = authorization.load_data()[0]
PASSWORD = authorization.load_data()[1]
URL_LOG = 'https://edu.tatar.ru/logon/'
DIARY_URL = "https://edu.tatar.ru/user/diary/term"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru,en;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Length": "40",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "edu.tatar.ru",
    "Origin": "https://edu.tatar.ru",
    "Referer": "https://edu.tatar.ru/logon/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 '
                  'YaBrowser/19.12.3.320 Yowser/2.5 Safari/537.36 ',
}

data = {
    "main_login": LOGIN,
    "main_password": PASSWORD,
}

cookies = pytools.load("cookies.data")

session = requests.Session()
session.cookies = cookies
response = session.get(DIARY_URL)
print(response.url)

