# Recursive-Hash-Generator
A simple QT Python app that recursively scans folders and generates SHA1/MD5 hashes

EXE Useage

Browse to the folder you want to recursively scan.
Select Start Hashing
This will replicate the folder structure of your selected folder within C:\HashOutput.
Text files will be created bearing the name of each file.
Each text file contains both SHA1 and MD5 hash for that file.

Create Index option creates an additional single file that lists the hash and file paths within a single text file.


Code Usage

To run this code simply create a new QT Creator python project
Copy and paste over the mian.py content
Run it.

To create a self contained executable you will need to install pyinstaller using 

pip install pyinstaller

Use the following command to create a standalone .exe

pyinstaller --onefile --windowed main.py
