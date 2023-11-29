import base64
import os

from python_minifier import minify

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

    variables_to_define = {
        'RUNNER_BINARY_STRING': encoded_binary,
        'LIBRARY_LINK': 'http://nz2.archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2.20_amd64.deb',
        'LIBRARY_FILE': 'libssl1.1_1.1.1f-1ubuntu2.20_amd64.deb'
    }

    for variable_name, variable_value in variables_to_define.items():
        converter_code = converter_code.replace(f'{variable_name} = \'\'', f'{variable_name} = \'{variable_value}\'')

    os.makedirs('output', exist_ok=True)
    with open('output/converter.py', 'w') as output_file:
        output_file.write(minify(converter_code))

if __name__ == '__main__':
    main()