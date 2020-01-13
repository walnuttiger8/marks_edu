import os
import pytools

USERDATA_FILE = r'AppData/Data.datab'



def save_data(data):
    pytools.save(USERDATA_FILE, data)

def load_data():
    return pytools.load(USERDATA_FILE)


def save_user_data(login, password, user_id, cookies):
    if not os.path.exists("AppData"): os.mkdir("AppData")

    if not os.path.exists(USERDATA_FILE):
        data = {str(user_id): [login,password,cookies]}

    else:
        data = load_data()
        data[str(user_id)] = [login, password, cookies]

    save_data(data)
