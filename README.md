# DELTARUNE in Linux

This is a script that will convert a Windows copy of DELTARUNE to one that can be used in Linux.

# Converting your game to Liunx

To convert the game, follow these steps:

1. Download the version of DELTARUNE from Windows that you want to use.

2. Download the script for the version you want to use.

3. Run the following command to run the script:
```bash
python3 PATH_TO_SCRIPT -o PATH_TO_WINDOWS_DELTARUNE_FOLDER -n PATH_TO_SAVE_THE_GAME
```

Replace `PATH_TO_SCRIPT` with the path where you downloaded the script.

Replace `PATH_TO_WINDOWS_DELTARUNE_FOLDER` with the path for the Windows deltarune folder, or you can ommit this if you installed the game through Steam in the default directories.

Replace `PATH_TO_SAVE_THE_GAME` with the path you want to save the game, or ommit to create it in the same directory as the script.

If you aren't fully sure, you can also use the following command for help.
```bash
python3 PATH_TO_SCRIPT -h
```

# Script building

1. After downloading the code, install the packages in requirements.txt:
```bash
pip install -r requirements.txt
```
2. Create a folder `input`:
```bash
mkdir input
```
3. Add the runners needed in the input folder. They should be named like `runner_VERSION`, where version is the GMS version using `_` instead of `.` to separate. You can run the script once to know exactly what file it is asking if you are not sure. If you don't want to provide all runners, add a blank file.
4. Run the `src/main.py` file. The resulting script will be in the `output` directory.