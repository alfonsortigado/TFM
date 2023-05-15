
"""
Created on Thursday April 13 2023

@author: Alfonso Ortigado-López.

"""

print('\n===========================================================================')
print('\n Starting the program to change the internal name of mae files to their representative pose')
print('===========================================================================')

# Import some libraries
import os
import re

# Input to define the path to the folder with .mae files
folder_path = input("""Define the path to the folder with .mae files:  """).strip()

for file in os.listdir(folder_path):
    if file.endswith(".mae"):
        # Get the filename without the extension.
        filename = os.path.splitext(file)[0]

        # Open the file and read all lines in a list
        with open(os.path.join(folder_path, file), "r") as f:
            lines = f.readlines()
            
            # Scroll through each line of the file
            for line_num, line in enumerate(lines):
                # Search for row where bigings the inf. about name compounds
                match = re.match(r":::", line)
                
                if match:
                    line_number = line_num 
                    break # exit loop after first match
        
        # Change line to the file title
        lines[line_number + 1] = filename + "\n"
        lines[line_number + 2] =  "\"\"\n"
        
        # Write the updated lines to the file
        with open(os.path.join(folder_path, file), "w") as f:
            f.writelines(lines)
    
        print(f'{file} has been modified at lines {line_number} and {line_number + 1}')

print('\n===========================================================================')
print(f'The changes have been made in the directory:\n --> {folder_path} .')
print('===========================================================================')
