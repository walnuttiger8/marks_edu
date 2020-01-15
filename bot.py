import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import authorization
import calc
import edu_handler

TOKEN = "224e9969bff69c02e294bbf0ec6f030a65d582f55c8e14b169f2a39a6f1a62af6990e920c91514f75a277"
MY_ID = -190819489
MSG_CODES = {
    "login": "Итак, введите свой логин еду",
    "password": "Здорово, теперь нам нужен ваш пароль)",
    "confirm": "Это вы? Да/Нет"
}

vk = vk_api.VkApi(token=TOKEN)
vk_session = vk.get_api()
longpoll = VkLongPoll(vk)


def write_msg(user_id, message, rand=None):
    random_id = random.randint(10, 100000) if rand == None else rand
    vk_session.messages.send(user_id=user_id, message=message, random_id=random_id)
    print("Ответил", message)


def get_last_bot_message(user_id):
    for message in vk_session.messages.getHistory(user_id=user_id)['items']:
        if message['from_id'] == MY_ID:
            return {"text": message['text'], "random_id": message["random_id"]}


def get_last_user_message(user_id):
    for message in vk_session.messages.getHistory(user_id=user_id)['items']:
        if message['from_id'] != MY_ID:
            return {"text": message['text'], "random_id": message["random_id"]}


def register_new_user(event):
    last_bot_message = get_last_bot_message(event.user_id)
    global login, password, cookies
    if last_bot_message['text'] == MSG_CODES['login']:
        login = event.text
        try:
            login = int(login)
            write_msg(event.user_id, "Здорово, теперь нам нужен ваш пароль)")
        except ValueError:
            write_msg(event.user_id, "Что-то не так с логином")
            write_msg(event.user_id, MSG_CODES['login'])
    elif last_bot_message['text'] == MSG_CODES['password']:
        password = event.text.upper()
        print("got the password", password)
        print("got the login", login)
        user_info = edu_handler.edu_auth(login, password)
        if user_info['name'] != "не удалость авторизоваться":
            name = user_info['name']
            cookies = user_info['cookies']
            write_msg(event.user_id, name)
            write_msg(event.user_id, MSG_CODES['confirm'])
        else:
            write_msg(event.user_id, user_info['name'])
            write_msg(event.user_id, MSG_CODES['login'])

    elif last_bot_message['text'] == MSG_CODES['confirm']:
        if event.text.upper() == "ДА":
            authorization.save_user_data(login, password, event.user_id, cookies)
            write_msg(event.user_id, "Все данные успешно сохранены")
            auth = False
        elif event.text.upper() == "НЕТ":
            write_msg(event.user_id, "В следующий раз все получится)")
            write_msg(event.user_id, MSG_CODES['login'])
        else:
            write_msg(event.user_id, "Так сложно было написать да/нет? Теперь заново придется")
            write_msg(event.user_id, MSG_CODES['login'])

    else:
        write_msg(event.user_id, MSG_CODES['login'])


def give_marks(event):
    base = authorization.load_data()

    if str(event.user_id) in base.keys():
        write_msg(event.user_id, "О, ты уже авторизован!")
        data = base[str(event.user_id)]
        subjects = edu_handler.parse(data[2])
        message = ""
        for subject in subjects.keys():
            message += f"{subject} : {''.join(subjects[subject] or ' ')} \n"
            marks = [int(mark) for mark in subjects[subject]]
            message += calc.main(marks) + "\n"

        write_msg(event.user_id, message)
    else:
        write_msg(event.user_id,"Судя по всему ты еще не авторизовался")
        register_new_user(event)


def run():
    global auth
    auth = False
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and not event.from_me:
            print(f"Получено новое сообщение от {vk_session.users.get(user_ids=event.user_id)[0]['first_name']}")
            print("Текст", event.text)

            if event.text.upper() == "АВТОРИЗАЦИЯ" and event.user_id:
                auth = True
                write_msg(event.user_id, "Итак, введите свой логин еду")
                continue

            if auth:
                register_new_user(event)


