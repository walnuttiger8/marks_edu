import os
import pickle


def save(file: str, object: object):
    """

    :param file: name of the file what would be used to save object
    :param object: object which you want to save
    """
    with open(file, "wb") as f:
        pickle.dump(object, f)


def load(file: str) -> object:
    """

    :param file: name of the file which ypu want use
    :return: object
    """
    with open(file, "rb") as f:
        return pickle.load(f)


def audio_convert(file: str, new_file: str, type: str):
    """

    :param file: name of the file to convert
    :param new_file: name of the new file
    :param type: format of the new file
    """
    cwd = os.getcwd()  # CurrentWorkingDir
    file = cwd + os.sep + file
    new_file: str = cwd + os.sep + new_file + "." + type
    command: str = f'ffmpeg -i {file} -f {type} {new_file}'
    os.system(command)
    return new_file
