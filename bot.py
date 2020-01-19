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
global longpoll
longpoll = VkLongPoll(vk)

common_dick = {
    "ПРИВЕТ": "ПРИВЕТ",
    "САФЭН": "ЭРИК",
    "ГРАДУСЫ": "ЛУЧШАЯ ГРУППА",
    "СКИНЬ ЖОПУ": "АХ ЕСЛИ БЫ Я МОГ...",
    "ДАША": "НЕ НАПИСАЛА",
    "КАИ": "ПУП ЗЕМЛИ",
    "ХЛЕБ": "КОЛБАСА",
    "КОЛБАСА": "СНАЧАЛА ХЛЕБ",
}


class Bot:
    def __init__(self):
        self.auth = False
        self.general_message = f"Мой функционал предельно прост. Я отправляю оценки и считаю баллы " \
            f"Просто напиши 'оценки'"

    @staticmethod
    def write_msg(user_id, message, rand=None):
        random_id = random.randint(10, 100000) if rand == None else rand
        vk_session.messages.send(user_id=user_id, message=message, random_id=random_id)
        print("Ответил", message)

    @staticmethod
    def get_last_bot_message(user_id):
        for message in vk_session.messages.getHistory(user_id=user_id)['items']:
            if message['from_id'] == MY_ID:
                return {"text": message['text'], "random_id": message["random_id"]}

    @staticmethod
    def get_last_user_message(user_id):
        for message in vk_session.messages.getHistory(user_id=user_id)['items']:
            if message['from_id'] != MY_ID:
                return {"text": message['text'], "random_id": message["random_id"]}

    # def register_new_user(self, event):
    #     last_bot_message = self.get_last_bot_message(event.user_id)
    #     global login, password, cookies
    #     if last_bot_message['text'] == MSG_CODES['login']:
    #         login = event.text.strip()
    #
    #         try:
    #             login = int(login)
    #             self.write_msg(event.user_id, "Здорово, теперь нам нужен ваш пароль)")
    #         except ValueError:
    #             self.write_msg(event.user_id, "Что-то не так с логином")
    #             self.write_msg(event.user_id, MSG_CODES['login'])
    #     elif last_bot_message['text'] == MSG_CODES['password']:
    #         password = event.text.upper()
    #         print("got the password", password)
    #         print("got the login", login)
    #         user_info = edu_handler.edu_auth(login, password)
    #         if user_info['name'] != "не удалость авторизоваться":
    #             name = user_info['name']
    #             cookies = user_info['cookies']
    #             self.write_msg(event.user_id, name)
    #             self.write_msg(event.user_id, MSG_CODES['confirm'])
    #         else:
    #             self.write_msg(event.user_id, user_info['name'])
    #             self.write_msg(event.user_id, MSG_CODES['login'])
    #
    #     elif last_bot_message['text'] == MSG_CODES['confirm']:
    #         if event.text.upper() == "ДА":
    #             authorization.save_user_data(login, password, event.user_id, cookies)
    #             self.write_msg(event.user_id, "Все данные успешно сохранены")
    #             self.auth = False
    #
    #         elif event.text.upper() == "НЕТ":
    #             self.write_msg(event.user_id, "В следующий раз все получится)")
    #             self.write_msg(event.user_id, MSG_CODES['login'])
    #         else:
    #             self.write_msg(event.user_id, "Так сложно было написать да/нет? Теперь заново придется")
    #             self.write_msg(event.user_id, MSG_CODES['login'])
    #
    #     else:
    #         self.write_msg(event.user_id, MSG_CODES['login'])

    def give_marks(self, event):

        base = authorization.load_data()

        if str(event.user_id) in base.keys():
            self.write_msg(event.user_id, "Вот твои оценки на сегодняшний день: ")
            data = base[str(event.user_id)]
            subjects = edu_handler.parse(data)
            message = ""
            for subject in subjects.keys():
                message += f"{subject} : {', '.join(subjects[subject] or ' ')} \n"
                marks = [int(mark) for mark in subjects[subject]]
                message += calc.main(marks) + "\n"

            self.write_msg(event.user_id, message)

        else:
            self.write_msg(event.user_id, "Судя по всему ты еще не авторизовался")
            self.register_new_user(event)

    def run(self):
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and not event.from_me:
                print(f"Получено новое сообщение от {vk_session.users.get(user_ids=event.user_id)[0]['first_name']}")
                print("Текст", event.text)

                if event.text.upper() == "ОЦЕНКИ":

                    if str(event.user_id) in authorization.load_data().keys():
                        self.give_marks(event)
                    else:
                        self.write_msg(event.user_id, "Ты ещё не авторизовался")
                        self.write_msg(event.user_id,
                                       "Введите ваш логин и пароль через запятую.\n Пример: 12345678910,ABCD")
                        self.register()

                    self.give_marks(event)

                elif event.text.upper() in common_dick.keys():
                    self.write_msg(event.user_id, common_dick[event.text.upper()].capitalize())

                else:
                    self.write_msg(event.user_id, self.general_message)

                # if self.auth:
                #     self.register_new_user(event)
                #     continue

    def register(self):
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and not event.from_me:
                print("Начало регистрации пользователя",vk_session.users.get(user_ids=event.user_id)[0]['first_name'])
                login, password = event.text.split(',')

                if not login.isdigit():
                    self.write_msg(event.user_id,
                                   "Логин должен состоять только из цифр, давайте попробуем ещё разок. Напишите "
                                   "'Оценки' ")
                    break

                try:
                    data = edu_handler.edu_auth(login, password)
                    authorization.save_user_data(login, password, event.user_id, data['cookies'])
                    self.write_msg(event.user_id, f"Здравствуйте {data['name']}")
                    break
                except AssertionError:
                    self.write_msg(event.user_id, "Не удалось авторизоваться")
                    continue
