import json
import os
import time

def read_file_and_return_lines(file_name):
    """Read a text file line by line and store non-empty lines in a list."""
    lines = []

    try:
        with open(file_name, 'r') as file:
            for line in file:
                stripped_line = line.strip()
                if stripped_line:  # Only process non-empty lines
                    lines.append(stripped_line)

        return lines

    except FileNotFoundError:
        print(f"The file '{file_name}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_all_values(obj):
    values = []
    if isinstance(obj, dict):
        for value in obj.values():
            values.extend(get_all_values(value))
    elif isinstance(obj, list):
        for item in obj:
            values.extend(get_all_values(item))
    else:
        values.append(obj)
    return values

if __name__ == "__main__":
    json_file_name = 'output.txt'