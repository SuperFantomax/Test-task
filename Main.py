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

def sync_of_data():
    if hashnumber_source == hashnumber_replica:
        print('There is no changes.')
    else:
        print('Upsy')
            
sync_of_data()
