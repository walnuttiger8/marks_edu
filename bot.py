import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import authorization
import calc
import edu_handler
from keyboard import Keyboard

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
    "ПРИВЕТ": "Привет",
    "САФЭН": "Эрик",
    "ГРАДУСЫ": "Лучшая группа",
    "СКИНЬ ЖОПУ": "Ах если бы я мог...",
    "ДАША": "Не написала",
    "КАИ": "ПУП ЗЕМЛИ",
    "ХЛЕБ": "Колбаса",
    "КОЛБАСА": "Сначала хлеб",
}


class Bot:
    def __init__(self):
        # self.general_message = f"Мой функционал предельно прост. Я отправляю оценки и считаю баллы " \
        #     f"Просто напиши 'оценки'"
        self.general_message = "Если у тебя нет клавиатуры, просто напиши 'комманды'"
        self.base = authorization.load_data()
        assert isinstance(self.base, dict), "Неверный тип базы данных"
        self.COMMANDS = {
            "ОЦЕНКИ":       self.give_marks,
            "ПРИВЕТ":       self.common,
            "САФЭН":        self.common,
            "ГРАДУСЫ":      self.common,
            "СКИНЬ ЖОПУ":   self.common,
            "ДАША":         self.common,
            "КАИ":          self.common,
            "ХЛЕБ":         self.common,
            "КОЛБАСА":      self.common,
        }

    @staticmethod
    def write_msg(user_id, *messages, keyboard_type=None):
        """
        Отправляет сообщения из поля messages пользователю

        :param user_id: id пользователя вконтакте
        :param messages: str
        :param keyboard_type: str принимает параметр 'reg' если нужно отправить клавиатуру для регистрации
        """
        buttons = list()

        if keyboard_type == 'reg':
            buttons.append(Keyboard.get_buttons('negative', 'Отмена'))
        else:
            buttons.append(Keyboard.get_buttons('positive', 'Оценки'))

        keyboard = Keyboard.get_keyboard(False, buttons)
        for message in messages:
            random_id = random.randint(10, 100000)
            vk_session.messages.send(user_id=user_id, message=message, random_id=random_id, keyboard=keyboard)
            print("Ответил", message)

    @staticmethod
    def get_last_bot_message(user_id):
        """
        Возвращает последнее сообщение от бота

        :param user_id: id пользователя вконтакте
        :return:dict Словарь {'text' = текст сообщения, 'random_id' = id сообщения}
        """
        for message in vk_session.messages.getHistory(user_id=user_id)['items']:
            if message['from_id'] == MY_ID:
                return {"text": message['text'], "random_id": message["random_id"]}

    @staticmethod
    def get_last_user_message(user_id):
        """
            Возвращает последнее сообщение от пользователя

            :param user_id: id пользователя вконтакте
            :return:dict Словарь {'text' = текст сообщения, 'random_id' = id сообщения}
                """
        for message in vk_session.messages.getHistory(user_id=user_id)['items']:
            if message['from_id'] != MY_ID:
                return {"text": message['text'], "random_id": message["random_id"]}

    @staticmethod
    def get_table(subjects):
        """
            Форматирование оценок

            :param subjects: dict словарь {"Предмет" : список оценок}
            :return: возврщает отформатированную строку с оценками
        """
        message = ""
        for subject in subjects.keys():
            message += f"{subject} : {', '.join(subjects[subject] or ' ')} \n"
            marks = [int(mark) for mark in subjects[subject]]
            message += calc.main(marks) + "\n"

        return message

    def common(self, event):
        """

        Пишет сообщение пользователю из словаря типичных ответов

        """
        self.write_msg(event.user_id, common_dick[event.text.upper()])

    def give_marks(self, event):
        """

        Выводит пользователю его текущие оценки

        :param event: event obect
        """
        base = authorization.load_data()

        if str(event.user_id) in base.keys():

            data = base[str(event.user_id)]
            subjects = edu_handler.parse(data)
            message = self.get_table(subjects)

            self.write_msg(event.user_id, "Вот твои оценки на сегодняшний день: ", message)

        else:
            self.write_msg(
                event.user_id,
                "Ты ещё не авторизовался", "Введите ваш логин и пароль через "
                                           "запятую.\n Пример: 12345678910,ABCD",
                keyboard_type='reg')
            self.register()

    def run(self):
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and not event.from_me:
                print(f"Получено новое сообщение от {vk_session.users.get(user_ids=event.user_id)[0]['first_name']}")
                print("Текст", event.text)

                if event.text.upper() in self.COMMANDS:
                    function = self.COMMANDS[event.text.upper()]
                    function(event)

                else:
                    self.write_msg(event.user_id, self.general_message)

    def register(self):
        """

        Запускает процесс регистрации с собственным прослушиванием сообщений
        """
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and not event.from_me:
                print("Начало регистрации пользователя", vk_session.users.get(user_ids=event.user_id)[0]['first_name'])
                if event.text.upper() == 'ОТМЕНА':
                    break
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
