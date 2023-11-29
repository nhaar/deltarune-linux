import base64
import os
import shutil
import subprocess
import argparse

# List of supported game versions, will be supplied by the generator
GAME_VERSIONS = []

# Using plural or not
version_noun = 'versions' if len(GAME_VERSIONS) > 1 else 'version'

# Listing in English
version_string = ''
if len(GAME_VERSIONS) == 1:
    version_string = GAME_VERSIONS[0]
else:
    version_string = f"{', '.join(GAME_VERSIONS[:-1])}, and {GAME_VERSIONS[-1]}"

# CLI information

parser = argparse.ArgumentParser(description=f'Converts the game to a Linux-compatible version. Works for Deltarune Steam {version_noun} {version_string}.')

parser.add_argument('-o', '--original_game_path', type=str, help='Path to the game directory, if not given it will use the default Steam directory')
parser.add_argument('-n', '--new_game_path', type=str, help='Path to the new game directory, if not given it will be created in the script\'s directory')

args = parser.parse_args()

# The string will be supplied by the generator
RUNNER_BINARY_STRING = ''
RUNNER_BINARY = base64.b64decode(RUNNER_BINARY_STRING)

# Steam folder name
DELTARUNE_NAME = 'DELTARUNEdemo'

# Path to the directory where the game is located
DELTARUNE_PATH = args.original_game_path if args.original_game_path else os.path.expanduser(f'~/.steam/steam/steamapps/common/{DELTARUNE_NAME}')

if (not os.path.isdir(DELTARUNE_PATH)):
    if (args.original_game_path):
        print(f'The game directory {args.original_game_path} was not found.')
    else:
        print('The game directory was not found. Please supply it as an argument or make sure the game is installed.')
    subprocess.run(['python3', os.path.realpath(__file__), '-h'])
    exit()

# Path where the new game will be created
NEW_DELTARUNE_PATH = args.new_game_path if args.new_game_path else os.path.join(os.getcwd(), DELTARUNE_NAME)

# File that will be copied, converting to lower case because of case-insensitive filesystems
# This is empty and will be supplied by the generator
DELTARUNE_FILES = []

assets_path = os.path.join(NEW_DELTARUNE_PATH, 'assets')

for file in DELTARUNE_FILES:
    file_path = os.path.join(DELTARUNE_PATH, file)
    if (os.path.isfile(file_path)):
        new_file_path = os.path.join(assets_path, file.lower())
        file_directory = os.path.dirname(new_file_path)
        if not os.path.isdir(file_directory):
            os.makedirs(file_directory)

        shutil.copy(file_path, new_file_path)
    else:
        print('Game file not found:', file_path)
        print('Make sure you have the correct game version installed and that you have supplied the correct game directory and try again.')
        exit()

# Rename it so it works on Linux
os.rename(os.path.join(assets_path, 'data.win'), os.path.join(assets_path, 'game.unx'))

# Create Linux executable
runner_path = os.path.join(NEW_DELTARUNE_PATH, "runner")
with open(runner_path, "wb") as f:
    f.write(RUNNER_BINARY)

# Give executable perms
subprocess.run(['chmod', '+rwx', runner_path])

# Download needed library
LIBRARY_LINK = ''
LIBRARY_FILE = ''
subprocess.run(['wget', LIBRARY_LINK])
subprocess.run(['sudo', 'dpkg', '-i', LIBRARY_FILE])

# Remove library after installing
os.remove(os.path.join(os.getcwd(), LIBRARY_FILE))