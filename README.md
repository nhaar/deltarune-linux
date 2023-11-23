# DELTARUNE in Linux

This is a script that will convert a Windows copy of deltarune to one that can be used in Linux.

# Utilization

First, download the version of DELTARUNE from Windows you want to use. Then, install the proper version of the script for the version you want. After that, you can run the script using the command:

```bash
python3 PATH_TO_SCRIPT PATH_TO_DELTARUNE_FOLDER
```

This command will modify all the deltarune files within the folder.

# Script building

1. After downloading the code, install the packages in requirements.txt
2. Create a folder `input` in the project and add the file `runner`, corresponding to the Linux runner you want to include
3. Run `src/main.py`. The resulting script will be in the `output` directory.