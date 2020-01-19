import os

import pytools

USERDATA_FILE = r'AppData/Data.datab'


def save_data(data):
    pytools.save(USERDATA_FILE, data)


def load_data(path: str = USERDATA_FILE):
    """
    Возвращает файл базы {vk_id = [login,password,cookies]} по указанному пути

    :param path: Путь до файла собственной базы
    :return: объект базы данных default: Словарь [vk_id] = [login,password,cookies]
    """
    return pytools.load(path)


def save_user_data(login: int, password: str, user_id, cookies):
    """

    :param login: Логин от электронного дневника (int)
    :param password: Пароль от электронного дневника (str)
    :param user_id: id пользователя вконтакте (str)
    :param cookies: объект класса cookieJar, получается из метода edu_auth()
    """
    if not os.path.exists("AppData"): os.mkdir("AppData")

    if not os.path.exists(USERDATA_FILE):
        data = {str(user_id): [login, password, cookies]}

    else:
        data = load_data()
        data[str(user_id)] = [login, password, cookies]

    save_data(data)
