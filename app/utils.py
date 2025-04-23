import random
import uuid


def random_num():
    return random.randint(10000, 99999)

def uuid_generate():
    return uuid.uuid4()