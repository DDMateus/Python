import os
import sys
import argparse
import shutil
import time
import hashlib

# Calculate the SHA256 hash of a file
def calculate_checksum(file_path, algorithm='sha256'):
    hasher = hashlib.new(algorithm)
    with open(file_path, "rb") as file:
        while True:
            data = file.read(8192)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

# Function to log messages to console and log file
def log(message, log_file_path):
    # Log messages to console and file
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_entry = f"{timestamp} - {message}"
    print(log_entry)
    with open(log_file_path, "a") as log_file:
        log_file.write(log_entry + "\n")
        
# Synchronize the source folder with the replica folder
def sync_folders(source_path, replica_path, log_file_path):
    
    # Check if the source folder exists
    if not os.path.exists(source_path):
        print(f"Source folder '{source_path}' does not exist.")
        sys.exit(1)  # Exit the program with an error code
     
    # Create the replica folder if it doesn't exist
    if not os.path.exists(replica_path):
        os.makedirs(replica_path)
        log(f"Folder created: {replica_path}", log_file_path)
    
    # Walk through the source directory    
    for root, dirs, files in os.walk(source_path):
        for dir in dirs:
            source_dir_path  = os.path.join(root, dir)
            replica_dir_path = source_dir_path.replace(source_path, replica_path)
            
            if not os.path.exists(replica_dir_path):
                os.makedirs(replica_dir_path, exist_ok=True)
                log(f"Folder copied: {source_dir_path} -> {replica_dir_path}", log_file_path)
             
        for file in files:
            source_file_path  = os.path.join(root, file)
            replica_file_path = source_file_path.replace(source_path, replica_path)
                
            # Calculate checksums for the source and replica files
            source_checksum = calculate_checksum(source_file_path)
            if os.path.exists(replica_file_path):
                replica_checksum = calculate_checksum(replica_file_path)
                # File exists in the replica directory but the content is different
                if source_checksum != replica_checksum:
                    shutil.copy2(source_file_path, replica_file_path)
                    log(f"File modified: {source_file_path} -> {replica_file_path}", log_file_path)
                    continue # Skip this file, it's already synchronized
            else:
                replica_checksum = None

            # Check if the file exists in the replica directory
            if replica_checksum is not None and source_checksum == replica_checksum:
                # File exists in both source and replica directories and checksums match (not modified)
                continue  # Skip this file, it's already synchronized
            else:
                # File exists in the source directory but not in the replica directory
                shutil.copy2(source_file_path, replica_file_path)
                log(f"File copied: {source_file_path} -> {replica_file_path}", log_file_path)

    # Check for files in the replica directory that don't exist in the source directory
    for root, dirs, files in os.walk(replica_path):
        for file in files:
            replica_file_path  = os.path.join(root, file)
            source_file_path   = os.path.join(root.replace(replica_path, source_path), file)
            
            # Check if the file exists in the source directory
            if not os.path.exists(source_file_path):
                # File exists in the replica directory but not in the source directory
                os.remove(replica_file_path)
                log(f"File deleted: {replica_file_path}", log_file_path)    
    
        # Check for directories in the replica directory that don't exist in the source directory
        for dir in dirs:
            replica_dir_path = os.path.join(root, dir)
            source_dir_path  = os.path.join(root.replace(replica_path, source_path), dir)

            # Check if the directory exists in the source directory
            if not os.path.exists(source_dir_path):
                # Directory exists in the replica directory but not in the source directory
                shutil.rmtree(replica_dir_path)
                log(f"Folder deleted: {replica_dir_path}", log_file_path)

# Schedule synchronization at regular intervals        
def schedule_sync(source_path, replica_path, sync_interval, log_file_path):
    while True:
        sync_folders(source_path, replica_path, log_file_path)
        print("Synchronization complete.")
        time.sleep(sync_interval)
    
def main():
    parser = argparse.ArgumentParser(description="Synchronize two folders with MD5 checksums.")
    parser.add_argument("source_path", help="Path to the source folder")
    parser.add_argument("replica_path", help="Path to the replica folder")
    parser.add_argument("log_file_path", help="Path to the log file")
    parser.add_argument("sync_interval", type=int, help="Synchronization interval in seconds")
    
    args = parser.parse_args()
    
    schedule_sync(args.source_path, args.replica_path, args.sync_interval, args.log_file_path)

if __name__ == '__main__':
    main()
