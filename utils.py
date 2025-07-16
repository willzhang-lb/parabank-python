import json
import os
import random
import string


def generate_username(prefix="user", length=6):
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return f"{prefix}_{suffix}"

def dump_to_json(file_name, key: str, value: str):
    # Load the JSON file
    json_file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(json_file_path, 'r') as file:
        member_info = json.load(file)

    # Generate a random username and add it to the dictionary

    member_info[key] = value

    # Write the updated dictionary back to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(member_info, file, indent=4)


def load_json_file_info(file_name: str):
    # Load the JSON file
    json_file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(json_file_path, 'r') as file:
        member_info = json.load(file)

    return member_info


def get_html_tag_of_node(locator) -> str:
    """
    Get the HTML tag of the node specified by the selector.
    :return: The HTML tag name of the node.
    """
    element_handle = locator
    if element_handle:
        return element_handle.evaluate("node => node.tagName")
    else:
        raise ValueError(f"No element found")