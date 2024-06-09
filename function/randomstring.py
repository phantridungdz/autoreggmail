import random
import string

def randomString():
    chars = string.ascii_letters + string.digits

    # Generate a random string of length 6 to 7
    random_string_length = random.randint(6, 7)
    random_string = ''.join(random.choice(chars) for _ in range(random_string_length))

    return random_string