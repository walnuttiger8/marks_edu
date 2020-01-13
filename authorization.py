import os
import pytools

USERDATA_FILE = r'AppData/Data.datab'



def save_data(data):
    pytools.save(USERDATA_FILE, data)

def load_data():
    return pytools.load(USERDATA_FILE)



# def auth(login=None, password=None, user_id=None, cookies = None, new=False):
#     try:
#         data = load_data()
#         if os.path.exists(USERDATA_FILE) and not new:
#             login = data[str(user_id)][0]
#             password = data[str(user_id)][1]
#             cookies = data[str(user_id)][2]
#         else:
#             save_user_data(login, password, user_id,cookies)
#
#         return [login, password,cookies]
#
#     except KeyboardInterrupt:
#         print('Вы завершили программу')


def save_user_data(login, password, user_id, cookies):
    if not os.path.exists("AppData"): os.mkdir("AppData")

    if not os.path.exists(USERDATA_FILE):
        data = {str(user_id): [login,password,cookies]}

    else:
        data = load_data()
        data[str(user_id)] = [login, password, cookies]

    save_data(data)

# db = load_data()
# print(db)