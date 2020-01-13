import os
import pytools

USERDATA_FILE = r'AppData/Data.datab'


def save_data():
    pytools.save(USERDATA_FILE, data)


def load_data():
    return pytools.load(USERDATA_FILE)


data = load_data()


def auth(login=None, password=None, user_id=None, new=False):
    try:
        data = load_data()
        if os.path.exists(USERDATA_FILE) and not new:
            login = data[str(user_id)][0]
            password = data[str(user_id)][1]
        else:
            save_user_data(login, password, user_id)

        return [login, password]

    except KeyboardInterrupt:
        print('Вы завершили программу')


def save_user_data(login, password, user_id):
    if not os.path.exists("AppData"): os.mkdir("AppData")
    data = load_data()
    data[str(user_id)] = [login, password]
    save_data()
