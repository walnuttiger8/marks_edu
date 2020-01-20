import json


class Keyboard:

    @staticmethod
    def get_buttons(color,*text):
        # assert len(colors) == len(text), 'Количество цветов должно совпадать количеству сообщений'
        buttons = list()
        for label in text:
            buttons.append({
                'action': {
                    'type': "text",
                    'label': label
                },
                "color": color
                })
        if len(buttons) > 1:

            return buttons
        else:

            return [buttons[0]]


    @staticmethod
    def get_keyboard(one_time=False, buttons=[]):
        keyboard = {
            "one_time": one_time,
            "buttons": buttons
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False, ).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard
