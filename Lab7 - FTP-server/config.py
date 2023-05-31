class Config:
    DIRECTORY = "WorkDir"
    SEPARATOR_DIR = '\\'
    COMMANDS = {
        'ls': 'showDIR',
        'dir': 'showDIR',
        'cd': 'moveToDir',
        'mkdir': 'createDIR',
        'rmdir': 'deleteDIR',
        'touch': 'createFile',
        'write': 'writeToFile',
        'cat': 'readFile',
        'rm': 'deleteFile',
        'cp': 'copyFile',
        'move': 'moveFile',
        'rename': 'renameFile',
        'pwd': 'pwd'
    }