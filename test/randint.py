from random import randint


def play():
    random_int = randint(0, 100)

    while True:
        input_num = int(input("请输入数字："))

        if input_num == random_int:
            print("猜对了~ 数字为：{}".format(random_int))
            break

        elif input_num > random_int:
            print("数字太大，再小点~")
            continue

        elif input_num < random_int:
            print("数字太小，再大点~")
            continue


if __name__ == '__main__':
    play()