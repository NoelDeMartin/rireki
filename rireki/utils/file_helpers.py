import os


def touch(path):
    separator_index = path.rindex('/')
    base_dir = path[:separator_index]

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    open(path, 'w').close()
