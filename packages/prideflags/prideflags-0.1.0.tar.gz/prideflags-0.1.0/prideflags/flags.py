import random
from .utils import color256

# Define all the flags and their colors
FLAGS = {
    'straight': [0, 255, 0, 255, 0],
    'gay': [196, 208, 226, 28, 20, 90],
    'bisexual': [198, 198, 97, 25, 25],
    'lesbian': [202, 209, 255, 255, 168, 161],
    'pansexual': [198, 198, 220, 220, 39, 39],
    'trans': [81, 211, 255, 211, 81],
    'nonbinary': [226, 226, 255, 255, 98, 98, 237, 237],
    'demiboy': [244, 249, 117, 255, 117, 249, 244],
    'demigirl': [244, 249, 218, 255, 218, 249, 244],
    'genderfluid': [211, 255, 128, 0, 63],
    'aromantic': [71, 149, 255, 249, 0],
    'agender': [0, 251, 255, 149, 255, 251, 0],
    'asexual': [0, 0, 242, 242, 255, 255, 54, 54],
    'graysexual': [54, 242, 255, 242, 54],
}

def print_flag(flag_name):
    """
    Print a flag with its name.
    :param flag_name: Name of the flag (key from FLAGS)
    """
    if flag_name not in FLAGS:
        raise ValueError(f"Flag '{flag_name}' not found. Use list_flags() to see available flags.")
    
    flag = FLAGS[flag_name]
    box = ' '
    width = 20
    reset = '\033[0m'

    for color in flag:
        print(f'{color256(color, "bg")}{box * width}{reset}')

def list_flags():
    """
    List all available flag names.
    """
    return list(FLAGS.keys())

def get_random_flag():
    """
    Get a random flag name from the available flags.
    """
    return random.choice(list(FLAGS.keys()))
