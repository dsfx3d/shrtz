import string
import random

def generate_hash(size, chars=string.ascii_lowercase + string.digits + string.ascii_letters):
    '''
    generates a 'size' character long
    pseudo random string using 'chars'
    '''
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))