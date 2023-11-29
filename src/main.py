import base64
import os
from copy import deepcopy

from python_minifier import minify
from constants import BASE_FILES, VERSION_DETAILS

def replace_variable_in_code(code, variable_name, default_value, value):
    '''Replaces a variable in the code with a new value.'''
    return code.replace(f'{variable_name} = {default_value}', f'{variable_name} = {value}')

def replace_string_variable_in_code(code, variable_name, value):
    '''Replaces a string variable in the code with a new value.'''
    return replace_variable_in_code(code, variable_name, "''", f"'{value}'")

def replace_list_variable_in_code(code, variable_name, value):
    '''Replaces a list variable in the code with a new value.'''
    return replace_variable_in_code(code, variable_name, '[]', value)

def create_for_version(version, base_code):
    os.makedirs('output', exist_ok=True)
    version_list = version['versions']
    converter_code = replace_list_variable_in_code(base_code, 'GAME_VERSIONS', version_list)
    files = deepcopy(BASE_FILES)
    if 'exclusive_files' in version:
        files.extend(version['exclusive_files'])

    converter_code = replace_variable_in_code(converter_code, 'DELTARUNE_FILES', '[]', files)

    with open(f'output/converter-{version["name"]}.py', 'w') as output_file:
        output_file.write(minify(converter_code))

def main():
    '''Main function, creates the converter file for production from a runner.'''
    # original code that will be built for production
    converter_code = open("src/converter.py", "r").read()

    # binary will be converted and saved as a string in the script
    encoded_binary = ''

    # this runner needs to be supplied manually for the script to work
    with open('input/runner', 'rb') as binary_file:
        binary_file_data = binary_file.read()
        encoded_binary = base64.b64encode(binary_file_data).decode('utf-8')

    string_variables_to_define = {
        'RUNNER_BINARY_STRING': encoded_binary,
        'LIBRARY_LINK': 'http://nz2.archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2.20_amd64.deb',
        'LIBRARY_FILE': 'libssl1.1_1.1.1f-1ubuntu2.20_amd64.deb'
    }

    for variable_name, variable_value in string_variables_to_define.items():
        converter_code = replace_string_variable_in_code(converter_code, variable_name, variable_value)

    for version_detail in VERSION_DETAILS:
        create_for_version(version_detail, converter_code)

if __name__ == '__main__':
    main()