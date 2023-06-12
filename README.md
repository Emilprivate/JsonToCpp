# JsonToCpp
Small Python script to convert all Json files in a directory to Cpp literal string format with a user interface. 

It provides a user-friendly GUI interface built with the Tkinter library.

## Features
### Select JSON Folder and Output Folder
The application allows you to choose the JSON folder containing the source JSON files and the output folder where the generated C++ header files will be saved.

### Conversion of JSON Data to C++ String Literal
The script converts the JSON data into a C++ string literal. It reads the JSON files from the selected JSON folder, converts the JSON data to a formatted string, and escapes special characters to be compatible with C++ string literals.

### Generate C++ Header Files
By clicking the "Generate .h File" button, the script generates C++ header files based on the JSON data. It creates a header file for each JSON file in the JSON folder, using the filename as the basis for the header file name. The generated header files contain the C++ data structures (e.g., struct, class, union, namespace) and the converted JSON data as a C++ string literal.

### Combine Header Files
The application provides an option to combine the generated header files into a single C++ header file. By selecting the "Combine Files" checkbox, the script combines all the generated header files into a single file named "combined.h". This can be useful when you want to include all the generated data structures in a single include file.

### Generate Combined Files by Directory
Another option provided is to generate combined files by directory. When selecting the "Generate Combined Files by Directory" checkbox, the script generates combined files for each directory within the output folder. It combines all the header files within each directory and saves the combined file with a name based on the directory name (e.g., "combined_directoryname.h"). This can be useful when you want to organize the generated files based on their respective directories.

### Output Terminal
The application includes an output terminal where you can see the progress and status of the file generation process. Error messages, if any, will be displayed in red, and success messages will be displayed in green.

## Getting Started
To use the C++ Header File Generator:

Ensure you have Python installed on your system.
Open the script in a Python editor or IDE, such as Visual Studio Code or PyCharm.
Make sure the required libraries (os, json, shutil, tkinter) are installed. You can install missing dependencies using pip.
Run the script. The GUI window will appear.
Select the JSON folder containing your JSON files by clicking the "Select JSON Folder" button.
Select the output folder where the generated C++ header files will be saved by clicking the "Select Output Folder" button.
Customize the settings, such as combining files and selecting the file type (struct, class, union, or namespace).
Click the "Generate .h File" button to start the generation process.
Check the output terminal for progress updates and any error or success messages.
Please note that it's important to have a good understanding of JSON and the desired C++ data structures before using this tool. Make sure the JSON data aligns with the expected C++ data structure format.
