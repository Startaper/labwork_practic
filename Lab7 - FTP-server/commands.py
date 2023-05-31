import os
import shutil

from config import Config

DIRECTORY = os.path.abspath(Config.DIRECTORY)
CURR_DIR = []


def showDIR(flags=None) -> str:
    """
    Показать директории
    """
    files = ""
    for file in os.listdir():
        files += f'{file}\n'
    return files[:-1] if files != "" else ' '


def createDIR(*names, flags=None) -> str:
    for name in names:
        path_dir, error_dir = checkDir(name, check=False)
        if error_dir != '':
            return error_dir
        os.makedirs(path_dir)
        return 'Directory created'


def deleteDIR(*names, flags=None) -> str:
    for name in names:
        path_dir, error_dir = checkDir(name)
        if error_dir != '':
            return error_dir
        if "-r" in flags:
            shutil.rmtree(path_dir, ignore_errors=False, onerror=None)
            return "Directory deleted"
        elif len(os.listdir(path_dir)) == 0:
            shutil.rmtree(path_dir, ignore_errors=False, onerror=None)
            return "Directory deleted"
        else:
            return "Directory is not empty!"


def moveToDir(directory, flags=None) -> str:
    global CURR_DIR
    new_dir, error_dir = checkDir(directory)
    if error_dir != '':
        return error_dir
    CURR_DIR = new_dir[len(DIRECTORY) + 1:].split(Config.SEPARATOR_DIR)
    os.chdir(os.path.join(DIRECTORY, *CURR_DIR))
    return 'Moved to another directory'


def createFile(name, flags=None) -> str:
    path_file, error_file = checkFile(name, check=False)
    if error_file != '':
        return error_file
    if os.path.exists(path_file):
        return "File is already exists!"
    else:
        f = open(path_file, "w")
        f.close()
        return "File created"


def writeToFile(text, name, flags=None) -> str:
    access = "w"
    if "-a" in flags:
        access = "a"
    path_file, error_file = checkFile(name)
    if error_file != '':
        return error_file
    f = open(path_file, access)
    f.write(text + "\n")
    f.close()
    return "Добавили текст в файл"


def readFile(name, flags=None) -> str:
    path_file, error_file = checkFile(name)
    if error_file != '':
        return error_file
    f = open(path_file, "r")
    res = ''
    for line in f:
        res += line.strip() + '\n'
    f.close()
    return res[:-1] if res != '' else ' '


def deleteFile(name, flags=None) -> str:
    path_file, error_file = checkFile(name)
    if error_file != '':
        return error_file
    os.remove(path_file)
    return 'File deleted'


def copyFile(name, new_dir, flags=None) -> str:
    path_file, error_file = checkFile(name)
    if error_file != '':
        return error_file
    path_dir, error_dir = checkDir(new_dir, check=False)
    if error_dir != '':
        return error_dir
    shutil.copy(path_file, path_dir)
    return 'File copied to another directory'


def moveFile(name, new_dir, flags=None) -> str:
    path_file, error_file = checkFile(name)
    if error_file != '':
        return error_file
    path_dir, error_dir = checkDir(new_dir, check=False)
    if error_dir != '':
        return error_dir
    shutil.move(path_file, path_dir)
    return 'File moved to another directory'


def renameFile(name, new_name, flags=None) -> str:
    path_file, error_file = checkFile(name)
    if error_file != '':
        return error_file
    path_dir, error_dir = checkDir(new_name, check=False)
    if error_dir != '':
        return error_dir
    os.rename(path_file, path_dir)
    return 'File renamed'


def uploadFile(name, text, flags=None) -> str:
    with open(name, "w") as file:
        file.write(text)
        file.close()
    return 'File uploaded'


def pwd(flags=None) -> str:
    return Config.DIRECTORY.split('/')[-1] + os.getcwd().split(f"{Config.DIRECTORY.split('/')[-1]}")[-1]


def checkDir(*paths, check=True) -> str:
    path = os.path.abspath(os.path.join(DIRECTORY, *CURR_DIR, *paths))
    error = ''
    if check:
        if not os.path.exists(path):
            error += "Directory is not exist!\n"
        if not os.path.isdir(path):
            error += "Path is not exist!\n"
    if DIRECTORY != path[:len(DIRECTORY)]:
        error += "Going outside the file system border!\n"
    return path, error[:-1]


def checkFile(*paths, check=True) -> str:
    path = os.path.abspath(os.path.join(DIRECTORY, *CURR_DIR, *paths))
    error = ''
    if check:
        if not os.path.exists(path):
            error += "File is not exist!\n"
        if not os.path.isfile(path):
            error += "Path is not exist!\n"
    if DIRECTORY != path[:len(DIRECTORY)]:
        error += "Going outside the file system border!\n"
    return path, error[:-1]
