import os
import socket


def main():
    """
    Точка входа клиент
    """
    host = str(input("Enter host: "))
    while True:
        try:
            PORT = input("Enter port: ")
            assert PORT.isdigit()
            PORT = int(PORT)
            assert 1024 < PORT < 65535
            break
        except AssertionError:
            print("Port must be digit in range(1024, 65535)")

    if host == "" or host is None:
        host = "localhost"

    client(host, PORT)


def client(host: str, PORT: int):
    """
    Настройка и старт клиента

    Args:
        HOST (str): Хост сервера
        PORT (int): Порт сервера, 9090 по умолчанию
    """
    while True:
        request = str(input('--> ')).strip()
        if request == "":
            continue
        sock = socket.socket()
        sock.connect((host, PORT))

        if 'upl' in request:
            request = uploadFile(request)
        sock.send(request.encode('utf-8'))

        response = sock.recv(1024).decode('utf-8')
        if response == 'exit':
            print("Shutdown the system")
            sock.close()
            break

        if 'dnl' in request:
            if len(request) == 2:
                downloadFile(request.split()[1], response)
            else:
                print(response)
        else:
            print(response)

        sock.close()


errors = [
    "Directory is not exist!",
    "Path is not exist!",
    "Going outside the file system border!"
]


def downloadFile(name, response):
    no_errors = True
    for error in errors:
        if error in response:
            print(error)
            no_errors = False
    if no_errors:
        with open(name, "w") as file:
            file.write(response)
            file.close()
        print('File downloaded')


def uploadFile(request) -> str:
    text = ""
    path = os.path.abspath(os.path.join(os.getcwd(), request.split()[1]))
    if not os.path.exists(path):
        print("File is not exist!")
    if not os.path.isfile(path):
        print("Path is not exist!")
    else:
        file = open(path, "r")
        for line in file:
            text += line
        file.close()
    return request + " \"" + text + "\""


if __name__ == '__main__':
    main()
