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
    file_hashes = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_file_hash(file_path)
            file_hashes[file_path] = file_hash
    return file_hashes

print(file_hashes(source_path))
print(file_hashes(replica_path))
