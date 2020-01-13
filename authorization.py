import os
import pytools

USERDATA_FILE = r'AppData/Data.datab'


def auth(new=False):
    try:
        if os.path.exists(USERDATA_FILE) and not new:
            data = pytools.load(USERDATA_FILE)
            login = data[0]
            password = data[1]
        else:
            if os.path.exists(USERDATA_FILE) and new: os.remove(USERDATA_FILE)

            login = str(input("Введите свой логин: "))
            password = str(input("Введите свой пароль: "))
            save_user_data(login, password)

        savedata = [login, password]
        pytools.save(USERDATA_FILE, savedata)

    except KeyboardInterrupt:
        print('Вы завершили программу')


def save_user_data(login, password):
    if not os.path.exists("AppData"):
        os.mkdir("AppData")


def load_data():
    return pytools.load(USERDATA_FILE)




