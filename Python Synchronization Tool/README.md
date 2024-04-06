# Python Challenge

## Table of Contents

1. [Introduction](#introduction)
2. [How to Use the Tool](#how-to-use-the-tool)
3. [Tests and Results](#tests-and-results)
4. [Prerequisites](#prerequisites)
5. [Example Usage](#example-usage)

## Introduction <a id="introduction"></a>

<p align="justify">This tool is designed to synchronize two folders in a one-way approach. After the synchronization, the content of the replica folder should be modified to exactly match the content of the source folder.</p>

## How to Use the Tool <a id="how-to-use-the-tool"></a>

To use the Python Challenge tool:

Here are the required commands and their respective order for using the Python Challenge tool:

1. **Clone the Repository**: 
   ```
   git clone https://github.com/DDMateus/Python/Python-Synchronization-Tool
   ```
   This command clones the Python Challenge repository from the specified URL to your local machine.

2. **Navigate to the Directory**: 
   ```
   cd Python-Synchronization-Tool
   ```
   This command changes the current directory to the directory where the Python Challenge tool's code is located.

3. **Run the Tool**: 
   ```
   python sync_folders.py <source_path> <replica_path> <log_file_path> <sync_interval>
   ```
   This command executes the Python Challenge tool.

By following these commands in the given order, you can effectively use the Python Challenge tool.

## Tests and Results <a id="tests-and-results"></a>

### Test 1: Checksum Calculation Function

**Test Description**: Test the `calculate_checksum` function with a valid file.

Create a file named "sample.txt" and get the hash of the file through powershell.

```powershell
Get-FileHash -Path .\sample.txt -Algorithm SHA256
```

![image](https://github.com/DDMateus/Python-3/assets/88774178/e53f7ed7-a30c-4391-b86b-add3269220c9)

Execute Python script for this test:
```python
from sync_folders import calculate_checksum

# Test calculate_checksum function with a valid file
def test_calculate_checksum_with_valid_file():
    sample_file = "sample.txt"
    expected_checksum = "A591A6D40BF420404A011733CFB7B190D62C65BF0BCDA32B57B277D9AD9F146E".lower()

    # Perform the operation
    actual_checksum = calculate_checksum(sample_file)

    # Assert the result
    assert actual_checksum == expected_checksum, "actual_checksum should be equal to expected_checksum"

if __name__ == '__main__':
    test_calculate_checksum_with_valid_file()
    print("Test passed.")
```

Result:

![image](https://github.com/DDMateus/Python-3/assets/88774178/76577c42-9503-4aa4-8e0d-3b3aa6f472cb)

**Test Results**: The test passed successfully, confirming that the checksum calculation function works as expected.

### Test 2: File Synchronization

**Test Description**: Perform a synchronization between source and replica folders, checking for changes and updating accordingly.

Usage:

![image](https://github.com/DDMateus/Python-3/assets/88774178/23dba8a1-4e92-4a28-aceb-3c62be7afd29)

Create source folder: source_folder

Create file inside source folder: file

Content inside the file: "Hello World!"

Folder structure:

source_folder/

    file.txt                 

Time interval: 3600s

Result:

![image](https://github.com/DDMateus/Python-3/assets/88774178/bf3ab33c-6b7d-402b-943a-6b9944a32650)

Log file:

![image](https://github.com/DDMateus/Python-3/assets/88774178/a9d06ff0-7fc9-41d6-a00c-0b37e39f345f)

Changing schedule time to 60 seconds. After 3 minutes:

![image](https://github.com/DDMateus/Python-3/assets/88774178/ea87cf86-af01-4c71-a2b2-5cf7d464782d)

New source folder structure:

source_folder/

    file1.txt                  
    file2.txt                 
    modifiedfile.txt           
    subfolder1/
        file3.txt              
        empty_folder.txt       
    subfolder2/
        file4.txt  

Execute the script. Result:

![image](https://github.com/DDMateus/Python-3/assets/88774178/053d3479-4b6a-48de-b7dd-1a666e37f974)

![image](https://github.com/DDMateus/Python-3/assets/88774178/81c67217-a3de-4eab-aaa7-6da02a841ed1)

Delete folder "subfolder1" and file "file4.txt" and wait for the synchronization:

log file:
![image](https://github.com/DDMateus/Python-3/assets/88774178/444c0b3f-50e9-40fb-b84c-a4e74101801e)

![image](https://github.com/DDMateus/Python-3/assets/88774178/d6676132-9e0f-423c-9c6a-b5a97e448e77)

Create a new folder: newfolder@£€{[¡¡”¨+

Create a file inside the new folder: testfile@£€{[¡¡”¨+.txt

Add a folder named 'newfolder' in the replica folder to test if it is removed since it does not exist in the source folder.

Wait for synchronization:

![image](https://github.com/DDMateus/Python-3/assets/88774178/905e4ee9-4c1e-44e6-8401-ecbf95c0b50b)

Add files inside the replica folder that are not inside source folder:

![image](https://github.com/DDMateus/Python-3/assets/88774178/7c5bd7d2-329d-4fff-b1f8-3ea4c924863d)

Execute synchronization to update the replica folder with the contents of the source folder.

![image](https://github.com/DDMateus/Python-3/assets/88774178/92d08b88-4cbe-4ee4-a908-2d4a94e9528e)

log file:

![image](https://github.com/DDMateus/Python-3/assets/88774178/137fe052-09a0-4afa-a3e9-96508ac7efde)

File creation/copying/removal operations should be logged to a file and to the console output.

![image](https://github.com/DDMateus/Python-3/assets/88774178/ce0a0d82-214a-444a-a918-e4d383596f64)

log file:

![image](https://github.com/DDMateus/Python-3/assets/88774178/a3f1c688-fe70-44c0-a78e-b0eb0986032d)

Change "subfolder2" to "subfolder3" and "file1.txt" to "file4.txt":

![image](https://github.com/DDMateus/Python-3/assets/88774178/8d95727b-27f3-4ebd-aa2c-ecaf023cb28f)

log file:

![image](https://github.com/DDMateus/Python-3/assets/88774178/03bbd876-5f72-43ae-a58e-a64c57c0e191)

![image](https://github.com/DDMateus/Python-3/assets/88774178/cb9e7e1f-2cb0-4a20-83dd-527a3c69a5b3)

**Test Results**: The synchronization process successfully detected and synchronized changes between the source and replica folders, ensuring data integrity and consistency.

## Prerequisites <a id="prerequisites"></a>

Before using the Python Challenge tool, ensure that you have:

- Python installed on your system.

## Example Usage <a id="example-usage"></a>

Here's an example of how to use the Python Challenge tool from the command line:

```bash
python .\sync_folders.py source_folder replica_folder log_file 60
```
