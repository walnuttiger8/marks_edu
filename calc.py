import math


def str_foramat(count):
    if count == 1:
        return "оценка"
    elif count in range(2, 5):
        return "оценки"
    elif count in range(5, 10):
        return "оценок"
    else:
        return ""


def mean(array):
    if len(array) < 1: return []
    array = [int(i) for i in array]
    return round(sum(array) / len(array), 2)


def calc(marks, iter, prefer):
    count = 0
    middle = mean(marks)
    while middle <= prefer - 0.4:
        marks.append(iter)
        count += 1
        middle = mean(marks)
    return {'count': count, 'mean': mean(marks)}


def main(marks):
    if len(marks) < 1: return ""
    middle = mean(marks)
    last = middle // 1
    last = middle - last
    last = last * 10

    if math.floor(last) in range(0, 6):
        prefer = math.floor(middle) + 1
    else:
        prefer = math.ceil(middle) + 1

    if mean(marks) >= 4.6: return "Оценки не нужны"
    message = "Нужно: \n"

    for mark in range(prefer, 5 + 1):
        result = calc(marks.copy(), mark, prefer)
        message += " ".join(
            [str(result['count']), str_foramat(result['count']), '"' + str(mark) + '"', "для балла", str(result['mean'])]) + "\n"

    if mean(marks) > 2:
        m = marks.copy()
        m.append(2)
        message += f'Если получишь 2, балл опустится до {mean(m)} \n'

    return message
