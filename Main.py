import os
import hashlib
import pickle
import logging
import argparse

source_path = "C:\\test\\Source"
replica_path = "C:\\test\\Replica"

list_original = os.listdir(source_path)
list_replica = os.listdir(replica_path)

def hash_calculation(list):
    binary = pickle.dumps(list)
    hash_list = hashlib.md5(binary)
    return hash_list.hexdigest()

hashnumber_source = hash_calculation(list_original)
hashnumber_replica = hash_calculation(list_replica)


if hashnumber_source != hashnumber_replica:
    print("Synchronization needed.")

    for item in list_replica:
        item_path = os.path.join(replica_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            os.rmdir(item_path)

    for item in list_original:
        src_path = os.path.join(source_path, item)
        rpl_path = os.path.join(replica_path, item)
        if os.path.isfile(src_path):
            with open(src_path, 'rb') as src_file, open(rpl_path, 'wb') as rpl_file:
                content = src_file.read()
                rpl_file.write(content)
        elif os.path.isdir(src_path):
            os.mkdir(rpl_path)
            
    print("Synchronization completed.")
else:
    print("No synchronization needed. Source and replica directories are already synchronized.")
