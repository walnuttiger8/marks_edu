import math
def mean(array):
    return round(sum(array) / len(array),2)

def calc(marks,iter,prefer):
    count = 0
    middle = mean(marks)
    while middle <= prefer - 0.4:
        marks.append(iter)
        count += 1
        middle = mean(marks)
    return count

def main(marks):
    if len(marks) < 1: return ""
    middle = mean(marks)
    last = middle//1
    last = middle - last
    last = last*10


    if last in range(0,6):
        prefer = math.floor(middle) + 1
    else:
        prefer = math.ceil(middle) + 1

    if mean(marks) >= 4.6: return "Оценки не нужны"
    message = ""

    for mark in range(prefer,5+1):
        message += " ".join(["Нужно",str(calc(marks.copy(),mark,prefer)), str(mark)+'-к', "для балла",str(prefer-0.4)]) + "\n"

    return message
