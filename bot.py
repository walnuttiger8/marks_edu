import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import edu_handler

TOKEN = "224e9969bff69c02e294bbf0ec6f030a65d582f55c8e14b169f2a39a6f1a62af6990e920c91514f75a277"
MY_ID = -190819489
MSG_CODES = {
    "login": "Итак, введите свой логин еду",
    "password": "Здорово, теперь нам нужен ваш пароль)",
}

vk = vk_api.VkApi(token=TOKEN)
vk_session = vk.get_api()
longpoll = VkLongPoll(vk)


def write_msg(user_id, message, rand=None):
    random_id = random.randint(10, 100000) if rand == None else rand
    vk_session.messages.send(user_id=user_id, message=message, random_id=random_id)

def get_last_bot_message(user_id):
    for message in vk_session.messages.getHistory(user_id=user_id)['items']:
        if message['from_id'] == MY_ID:
            return {"text":message['text'],"random_id":message["random_id"]}

def get_last_user_message(user_id):
    for message in vk_session.messages.getHistory(user_id=user_id)['items']:
        if message['from_id'] != MY_ID:
            return {"text":message['text'],"random_id":message["random_id"]}


def main():
    global auth
    auth = False
    for event in longpoll.listen():
        print("listening")
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and not event.from_me:

            print(f"Получено новое сообщение от {vk_session.users.get(user_ids=event.user_id)[0]['first_name']}")
            print("Текст",event.text)

            
            print("first auth",auth)

            if event.text == "авторизация":

                auth = True
                write_msg(event.user_id, "Итак, введите свой логин еду")
                print("second auth", auth)
                continue



            if auth:
                print("Я в цикле аутх")
                last_bot_message = get_last_bot_message(event.user_id)
                if last_bot_message['text'] == MSG_CODES['login']:
                    login = event.text
                    try:
                        login = int(login)
                        # print("got the login",login)
                        write_msg(event.user_id,"Здорово, теперь нам нужен ваш пароль)")
                    except ValueError:
                        write_msg(event.user_id,"Что-то не так с логином")
                        write_msg(event.user_id, "Итак, введите свой логин еду")
                elif last_bot_message['text'] == MSG_CODES['password']:
                    password = event.text.upper()
                    print("got the password",password)
                    print("got the login", login)
                    write_msg(event.user_id, edu_handler.edu_auth(login, password))

                else:
                    write_msg(event.user_id,"Что-то пошло не так, снова введите логин")





    print('stopped listening')


main()
