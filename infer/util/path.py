from os import path as osp
import platform


def format_filepath(*filepath):
    path = osp.join(*filepath)
    # Windows
    if platform.system() == 'Windows':
        return path.replace('/','\\')
    # Linux
    return path.replace('\\', '/')

