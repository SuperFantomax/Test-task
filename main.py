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
    
source_hash = {}    
for root, dirs, files in os.walk(source_path):
    for file in files:
        file_path_source = os.path.join(root, file)
        file_hash_source = calculate_file_hash(file_path_source)
        source_hash[file_path_source] = file_hash_source

replica_hash = {}
for root, dirs, files in os.walk(replica_path):
    for file in files:
        file_path_replica = os.path.join(root, file)
        file_hash_replica = calculate_file_hash(file_path_replica)
        replica_hash[file_path_replica] = file_hash_replica
