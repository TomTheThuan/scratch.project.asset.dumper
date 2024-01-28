import shutil, json, zipfile, os

PROJECT_JSON = ''
PROJECT_DIR = ''
REMOVE_LIST = []
LOGLEVEL = 0

def debug(info, level: str):
    info = str(info)
    
    match level:
        case 'log':
            print('\033[32m', '[Log]    ', info, '\033[0m')
        case 'info':
            print('\033[34m', '[Info]   ', info, '\033[0m')
        case 'error':
            print('\033[31m', '[Error]  ', info, '\033[0m')
        case 'warn':
            print('\033[33m', '[Warn]   ', info, '\033[0m')
        case _:
            print(info)
    

def unpack_Sb3_File(path):
    # globalize PROJECT_JSON and PROJECT_DIR
    global PROJECT_DIR
    global PROJECT_JSON

    # Change name from .sb3 to .zip
    filePath = path.split('.sb3')
    # debug(filePath, 'log')
    newZippedFile = filePath
    newZippedFile[len(newZippedFile) - 1] = '.zip'
    # debug(newZippedFile, 'log')
    newZippedFile = ''.join(newZippedFile)
    # debug(newZippedFile, 'log')

    dir = filePath
    dir[len(dir) - 1] = '\\'
    # debug(dir, 'log')
    dir = ''.join(dir)
    # debug(dir, 'log')

    PROJECT_JSON = dir + 'project.json'
    PROJECT_DIR = dir

    if os.path.exists(PROJECT_DIR) and os.path.exists(PROJECT_JSON):
        debug('Your project already unpacked, skip unpacking', 'info')
        return

    shutil.move(path, newZippedFile)
    # debug('Change file name from ' + path + ' to ' + newZippedFile, 'info')
    # debug(newZippedFile + ' will extract to ' + dir, 'info')
    debug('Your project is extracting to ' + PROJECT_DIR, 'info')
    zipfile.ZipFile(newZippedFile).extractall(dir)
    shutil.move(newZippedFile, path)
    debug('Extract to' + PROJECT_DIR + ' success', 'info')



def read_targets_info(target):
    debug('Target name: ' + target['name'], 'info')
    for costume in target['costumes']:
        debug(' / Costume name: ' + costume['name'], 'info')
        debug(' \\ Costume id:   ' + costume['assetId'], 'info')
    
    for sound in target['sounds']:
        debug(' / Sound name:   ' + sound['name'], 'info')
        debug(' \\ Soune id:     ' + sound['assetId'], 'info')


def rearrange_target_assets(target):
    global REMOVE_LIST

    targetName = target['name']
    os.mkdir(PROJECT_DIR + targetName + '\\')
    debug('Dumping ' + targetName + ' ...', 'info')

    for costume in target['costumes']:
        shutil.copy(PROJECT_DIR + costume['md5ext'], PROJECT_DIR + targetName + '\\' + costume['name'] + '.' + costume['dataFormat'])
        REMOVE_LIST.append(PROJECT_DIR + costume['md5ext'])

    for sound in target['sounds']:
        shutil.copy(PROJECT_DIR + sound['md5ext'], PROJECT_DIR + targetName + '\\' + sound['name'] + '.' + sound['dataFormat'])
        REMOVE_LIST.append(PROJECT_DIR + sound['md5ext'])


def clean_up():
    global REMOVE_LIST

    for file in REMOVE_LIST:
        if os.path.exists(file):
            os.remove(file)
    
    debug('Clean up success!' , 'info')
    

def main(file):
    unpack_Sb3_File(file)
    with open(PROJECT_JSON, encoding='utf-8') as f:
        projectData = json.load(f)
    # debug(projectData, 'log')
    # debug(projectData['targets'][0], 'log')
    for target in projectData['targets']:
        # read_targets_info(target)
        rearrange_target_assets(target)
    clean_up()

if __name__ == '__main__':
    sb3Path = input("\033[32mPath of the file: \033[0m")
    main(sb3Path)