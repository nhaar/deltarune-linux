import base64
import os
from copy import deepcopy
from typing import Callable, Any

from python_minifier import minify
from constants import BASE_FILES, VERSION_DETAILS

def main():
    '''Main function, creates the converter scripts for all supported versions.'''
    
    # original code that will be built for production
    converter_code = open("src/converter.py", "r").read()

    converter_code = replace_multiple_variables_in_code(converter_code, {
        'LIBRARY_LINK': 'http://nz2.archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2.20_amd64.deb',
        'LIBRARY_FILE': 'libssl1.1_1.1.1f-1ubuntu2.20_amd64.deb'
    }, replace_string_variable_in_code)

    # Directory where the scripts will be saved
    os.makedirs('output', exist_ok=True)

    for version_detail in VERSION_DETAILS:
        create_for_version(version_detail, converter_code)

def replace_variable_in_code(code: str, variable_name: str, old_value, value) -> str:
    '''
    Replaces a variable in pytho code with a new value.
    
    Args:
        code (str): The code to replace the variable in.
        variable_name (str): The name of the variable to replace.
        old_value (any): The old value of the variable.
        value (any): The new value of the variable.

    Returns:
        str: The code with the variable replaced.
    '''
    return code.replace(f'{variable_name} = {old_value}', f'{variable_name} = {value}')

def replace_string_variable_in_code(code: str, variable_name: str, value: str) -> str:
    '''
    Replaces a string variable in the code declared with an empty string with a new string value.

    Args:
        code (str): The code to replace the variable in.
        variable_name (str): The name of the variable to replace.
        value (str): The new value of the variable.

    Returns:
        str: The code with the variable replaced.
    '''
    return replace_variable_in_code(code, variable_name, "''", f"'{value}'")

def replace_list_variable_in_code(code: str, variable_name: str, value: list) -> str:
    '''
    Replaces a list variable declared with an empty list in the code with a new value.
    
    Args:
        code (str): The code to replace the variable in.
        variable_name (str): The name of the variable to replace.
        value (list): The new value of the variable.

    Returns:
        str: The code with the variable replaced.
    '''
    return replace_variable_in_code(code, variable_name, '[]', value)

def replace_multiple_variables_in_code(code: str, variables_to_define: dict, replace_function: Callable[[str, str, Any], str]) -> str:
    '''
    Apply a variable replacing function to multiple variables in the code.

    Args:
        code (str): The code to replace the variables in.
        variables_to_define (dict): A dictionary with the variables to replace and their new values.
        replace_function (function): The function to use to replace the variables.
    '''
    for variable_name, variable_value in variables_to_define.items():
        code = replace_function(code, variable_name, variable_value)

    return code

def create_for_version(version, base_code):
    '''
    Creates the converter scripts for a dictionary with the version details.

    Args:
        version (dict): The dictionary with the version details.
        base_code (str): The base code for the converter.
    '''
    files = deepcopy(BASE_FILES)
    if 'exclusive_files' in version:
        files.extend(version['exclusive_files'])

    converter_code = replace_multiple_variables_in_code(base_code, {
        'GAME_VERSIONS': version['versions'],
        'DELTARUNE_FILES': files
    }, replace_list_variable_in_code)

    # binary will be converted and saved as a string in the script
    # the runners need to be supplied manually before building for the script to work
    # if you don't to include a specific runner, you can just leave an empty file with the same required name
    with open(f'input/runner_{version["gms_version"].replace(".", "_")}', 'rb') as binary_file:
        binary_file_data = binary_file.read()
        encoded_binary = base64.b64encode(binary_file_data).decode('utf-8')
        converter_code = replace_string_variable_in_code(converter_code, 'RUNNER_BINARY_STRING', encoded_binary)

    with open(f'output/converter-{version["name"]}.py', 'w') as output_file:
        output_file.write(minify(converter_code))

if __name__ == '__main__':
    main()