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
