import os

def get_abs_dir(file_name):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(script_dir, file_name)

def try_parse_float(input):
    try:
        float(input)
        return True
    except ValueError:
        return False
