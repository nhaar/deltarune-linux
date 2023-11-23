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

    converter_code = converter_code.replace('b64decode("")', f'b64decode("{encoded_binary}")')

    os.makedirs('output', exist_ok=True)
    with open('output/converter.py', 'w') as output_file:
        output_file.write(minify(converter_code))

if __name__ == '__main__':
    main()