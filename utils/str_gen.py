import random
import string


def get_random_str(length: int = 7) -> str:
    pool = string.ascii_letters
    return "".join(random.choice(pool) for _ in range(length))
