def read_json_file(file_path):
    """Reads a JSON file and returns its contents as a dictionary."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json_file(file_path, data):
    """Writes a dictionary to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def append_to_log_file(log_file, data):
    """Appends a new entry to a log file."""
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(data + '\n')

def read_log_file(log_file):
    """Reads a log file and returns its contents as a list of lines."""
    with open(log_file, 'r', encoding='utf-8') as f:
        return f.readlines()