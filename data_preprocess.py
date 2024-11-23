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

def read_json_and_return_object(json_name):
    with open(json_name, 'r') as file:  # Replace 'data.json' with your file name
        data = json.load(file)

    # Now `data` is a Python dictionary
    # print(data)
    return data

def read_json_and_return_lines(json_name):
    lines = []

    with open(json_name, 'r') as file:  # Replace 'data.json' with your file name
        data = json.load(file)
    
    # print("data", data)
    lines = get_all_values(data)

    # for item in data.values():
    #     print(item)
    #     lines.append(item)
    # Now `data` is a Python dictionary
    # print(data)
    return lines

def read_json_and_combine_keyvalues(json_name):
    if not os.path.exists(json_name):
        raise FileNotFoundError(f"The file {json_name} does not exist.")
    
    formatted_list = []
    
    with open(json_name, 'r') as file:
        json_content = file.read()

    try:
        data = json.loads(json_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON: {e}")

    for entry in data:
        formatted_string = "{}, {}".format(entry['company'], entry['robot'])
        formatted_list.append(formatted_string)
    
    return formatted_list

def clean_text_list(text_list, time_repeat):
    cleaned_list = []
    for text in text_list:
        parts = text.split('.', 1)
        if len(parts) > 1:
            cleaned_list.append(parts[1].strip())
        else:
            cleaned_list.append(text.strip())  # Keep the original text if no split occurred
    
    cleaned_list.extend([' '] * (time_repeat - int((len(text_list)-1) % time_repeat)))
    return cleaned_list

def save_list_to_txt(string_list, filename):
    """
    Save a list of strings to a text file, each string on a new line.

    Parameters:
    string_list (list of str): The list of strings to save.
    filename (str): The name of the file to save the strings to.
    """
    with open(filename, 'w') as file:
        for item in string_list:
            file.write(f"{item}\n")  # Write each string followed by a newline

    print("'" + filename + "' is saved.")

def add_entry_to_json_file(json_file, date, company, robot, values):
    # Check if the file exists
    if os.path.exists(json_file):
        # Read the existing data from the JSON file
        with open(json_file, 'r') as file:
            data = json.load(file)
    else:
        # If the file does not exist, create an initial structure
        data = []

    # Create a new entry
    new_entry = {
        'date': date,
        'company': company,
        'robot': robot,
        'values': values  # Use the provided values directly
    }
    
    # Append the new entry to the data
    data.append(new_entry)

    # Write the updated data back to the JSON file
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)  # Use indent for pretty printing

def today_date():
    current_time = time.time()

    # Convert to local time tuple
    local_time = time.localtime(current_time)

    # Format the date as YYYY-MM-DD
    date = time.strftime("%Y-%m-%d", local_time)

    return date

if __name__ == "__main__":
    json_file_name = 'output.json'
    date_to_add = '2023-10-01'  # Specify the date
    company_to_add = 'CompanyA'  # Specify the company
    robot_to_add = 'Model Z'  # Specify the robot model
    values_to_add = [
        {'query': 'What is the robot model?', 'answer': 'Model Z'},
        {'query': 'What are its capabilities?', 'answer': 'High-speed navigation'}
    ]  # Specify the values as a list of dictionaries

    add_entry_to_json_file(json_file_name, date_to_add, company_to_add, robot_to_add, values_to_add)
    print(f"Added entry for {company_to_add} on {date_to_add} with robot model: '{robot_to_add}' and values: {values_to_add}")