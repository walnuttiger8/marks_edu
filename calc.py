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

def main(marks,prefer):
    for mark in range(prefer,5+1):
        return "Тебе нужно",calc(marks.copy(),mark,prefer), mark, ", чтобы вышло",prefer-0.4

