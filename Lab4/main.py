import AES


def main_menu():
    print('Что необходимо сделать?')
    print('1 - зашифровать данные')
    print('2 - расшифровать данные')
    uc = int(input())
    if uc == 1:
        print('Введите данные')
        data = input()
        print('Введите ключ')
        key = input()
        encrypted = AES.encrypt(data, key)
        print('Зашифрованное сообщение:', encrypted)
    elif uc == 2:
        print('Введите данные')
        data = input()
        print('Введите ключ')
        key = input()
        decrypted = AES.decrypt(data, key)
        print('Расшифрованное сообщение:', decrypted)


if __name__ == '__main__':
    while True:
        main_menu()
