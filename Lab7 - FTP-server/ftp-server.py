from socket import socket

from commands import *
from config import Config as cfg


class Parse:
    def __init__(self):
        os.chdir(DIRECTORY)
        self.cmd = {}
        self.cur_dir = []
        self.command = ""

    def read_console(self, request):
        self.cur_dir = (cfg.DIRECTORY.split(
            '/')[-1] + os.getcwd().split(f"{cfg.DIRECTORY.split('/')[-1]}")[-1])
        self.command = request
        res_args = []
        res_cmd, *args = self.command.split(" ", 1)
        res_flags = {}
        if len(args) > 0:
            args = args[0]
            if args.count("\"") % 2 != 0:
                raise TypeError
            q = False
            for item in args.split("\""):
                if q:
                    res_args.append(item)
                else:
                    for arg in item.split():
                        if arg[0] == "-":
                            res_flags.add(arg)
                        else:
                            res_args.append(arg)
                q = not q
        self.cmd = {"command": res_cmd,
                    "arguments": res_args, "flags": res_flags}

    def execute(self) -> str:
        """Ввод команд

        Returns:
            str: сообщение об ошибке или результат выполнения команды
        """
        try:
            return eval(f'{cfg.COMMANDS[self.cmd["command"]]}')(*self.cmd["arguments"], flags=self.cmd["flags"])
        except KeyError or NameError:
            return "Command does not exist!"
        except TypeError:
            return "Incorrect number of parameters passed!"
        except FileNotFoundError:
            return "File or directory does not exist!"
        except FileExistsError:
            return "Directory is already exists!"


def server(HOST: str, PORT: int):
    """
    Настройка и старт сервера

    Args:
        HOST (str): Хост сервера
        PORT (int): Порт сервера, 9090 по умолчанию
    """
    sock = socket()
    sock.bind((HOST, PORT))
    print(f"Server started with port: {PORT}")
    sock.listen()

    file_manager = Parse()
    while True:
        conn, _ = sock.accept()

        request = conn.recv(1024).decode('utf-8')
        if request == "exit":
            conn.send("exit".encode('utf-8'))
            break
        print(request)

        file_manager.read_console(request)
        response = file_manager.execute()
        conn.send(response.encode('utf-8'))

    conn.close()


def main():
    """
    Точка входа для сервера
    """
    HOST = str(input("Enter host: "))
    try:
        PORT = input("Enter port: ")
        assert PORT.isdigit()
        PORT = int(PORT)
        assert 0 < PORT < 65535
    except AssertionError:
        PORT = 9090

    if HOST == "" or HOST is None:
        HOST = "localhost"
    try:
        server(HOST, PORT)
    except OSError:
        print(f"Port: {PORT} already in use")
        while True:
            try:
                PORT += 1
                server(HOST, PORT)
                break
            except OSError:
                pass


if __name__ == '__main__':
    main()
