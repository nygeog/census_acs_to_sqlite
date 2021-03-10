import json
import os


def read_json(json_file):
    with open(json_file) as f:
        return json.load(f)


def dict_to_json(dictionary, json_file):
    with open(json_file, "w") as f:
        json.dump(dictionary, f)


def create_directory(directory_folder):
    if not os.path.exists(directory_folder):
        os.makedirs(directory_folder)


def split_list_to_chunks(split_list, n):
    return [split_list[i:i + n] for i in range(0, len(split_list), n)]
