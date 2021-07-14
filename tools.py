import random
import string


def generate_id(existing_ids=None, length=8):
    if existing_ids is None:
        existing_ids = []
    rand_string = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
    while rand_string in existing_ids:
        rand_string = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
    return rand_string
