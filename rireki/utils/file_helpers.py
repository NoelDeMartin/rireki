import os


def touch(path):
    directory_name = os.path.dirname(path)

    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    open(path, 'w').close()


def file_put_contents(path, contents):
    touch(path)

    with open(path, 'w') as file:
        file.write(contents)


def file_get_contents(path):
    if not os.path.exists(path):
        return None

    with open(path, 'r') as file:
        return file.read()


def file_get_name(path):
    return file_get_parts(path)['name']


def file_get_extension(path):
    return file_get_parts(path)['extension']


def file_get_parts(path):
    parts = {}

    parts['folder_path'] = os.path.dirname(path)

    basename = os.path.basename(path)
    extension_index = basename.find('.')

    if extension_index == -1:
        parts['name'] = basename
        parts['extension'] = ''
    else:
        parts['name'] = basename[:extension_index]
        parts['extension'] = basename[extension_index+1:]

    return parts
