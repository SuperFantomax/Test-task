import os
import hashlib
import logging
import argparse

source_path = "C:\\test\\Source"
replica_path = "C:\\test\\Replica"

def calculate_file_hash(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
        hash_object = hashlib.md5(content)
        file_hash = hash_object.hexdigest()
        return file_hash
    
def file_hashes(directory):
    file_hashes = set()
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)
            file_hashes.add(relative_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            relative_path = os.path.relpath(dir_path)
            file_hashes.add(relative_path)
    return file_hashes

print(file_hashes(source_path))
print(file_hashes(replica_path))
