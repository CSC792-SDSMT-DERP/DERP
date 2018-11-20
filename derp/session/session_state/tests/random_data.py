import random
import string
import os


def random_num(lower, upper):
    return random.choice(range(lower, upper))


def random_str():
    return ''.join(random.choice(
        string.ascii_letters + string.digits + " ") for _ in range(random_num(10, 20)))


def random_path(max_len):
    path = random_str()
    for i in range(max_len):
        path = os.path.join(path, random_str())
    return path
