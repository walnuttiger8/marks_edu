import requests
from bs4 import BeautifulSoup as bs

# LOGIN = authorization.load_data()[0]
# PASSWORD = authorization.load_data()[1]
URL_LOG = 'https://edu.tatar.ru/logon'
DIARY_URL = "https://edu.tatar.ru/user/diary/term"
COOKIE_FILE = "AppData/cookies.data"

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
tbd = ["<td>", "</td>", "просмотр", ".", "\n", "", " просмотр\n", "-"]


# data = {
#     "main_login": LOGIN,
#     "main_password": PASSWORD,
# }

# session = requests.Session()
# # session.cookies = cookies
# response = session.get(DIARY_URL)
# global soup
# soup = bs(response.content, "html.parser")
#



def edu_auth(login, password):
    session = requests.Session()
    data = {
        "main_login": login,
        "main_password": password,
    }
    response = session.post(url=URL_LOG, data=data, headers=headers)
    print(response.url)
    if response.url == URL_LOG: return {"cookies": response.cookies, "name": "не удалость авторизоваться"}
    name = parse_name(response.content)
    return {"cookies": response.cookies, "name": name}


def parse_name(content):
    soup = bs(content, "html.parser")
    table = soup.find("table")
    row = table.find("tr")
    cells = [td.text for td in row.findAll('td')]
    return cells[-1]

def parse(data):

    dick = dict()
    session = requests.Session()
    session.cookies = data[2]
    response = session.get(DIARY_URL)
    if response.url == URL_LOG:
        cookies = edu_auth(data[0],data[1])['cookies']
        session.cookies = cookies
        response = session.get((DIARY_URL))

    soup = bs(response.content, "html.parser")
    table = soup.find('table')

    rows = table.findAll('tr')[:-1]

    for row in rows[1:]: dick[row.find('td').text] = [word.text for word in row.findAll('td')[1:]]

    for i in dick: dick[i] = [word for word in dick[i] if word not in tbd]

    for i in dick:
        for j in dick[i]:
            if "." in j:
                dick[i].remove(j)

    return dick
