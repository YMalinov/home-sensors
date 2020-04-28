import os

def get_abs_path(file_name):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(script_dir, file_name)

def read_line_from(path):
    with open(get_abs_path(path), 'r') as file:
        return file.readline().strip()

def print_to_file(data, path):
    print(data)
    with open(get_abs_path(path), 'w') as file:
        print(data, file=file)

def round_num_dict(input_dict):
    return {
        k:v if isinstance(v, str) else round(v, 2) \
            for (k, v) in input_dict.items()
    }

def avg(arr):
    return sum(arr) / len(arr)
