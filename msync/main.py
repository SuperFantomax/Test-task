import os
import hashlib
import logging
import argparse
import time
import shutil

def file_set(directory):
    file_set = set()
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)
            file_set.add(relative_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            relative_path = os.path.relpath(dir_path, directory)
            file_set.add(relative_path)
    return file_set

def calculate_md5(path):
    md5 = hashlib.md5()
    with open(path, 'rb') as file:
        data = file.read()
        md5.update(data)
    return md5.hexdigest()

def sync(source_path, replica_path):
    if not os.path.exists(replica_path):
        os.makedirs(replica_path)
        logging.info(f'Replica folder {replica_path} created.')
    source_set = file_set(source_path)
    replica_set = file_set(replica_path)
    
    delete_set = replica_set.difference(source_set)
    create_set = source_set.difference(replica_set)
    samedata_set = replica_set.intersection(source_set)
   
    if len(delete_set) or len(create_set) != 0 or len(samedata_set) > 0:
        logging.info("Synchronization start.")

        for item in delete_set:
            item_path = os.path.join(replica_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
                logging.info(f'File {item} from {replica_path} was deleted.')
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                logging.info(f'Directory {item} from {replica_path} was deleted.')
            
        for item in create_set:
            src_path = os.path.join(source_path, item)
            rpl_path = os.path.join(replica_path, item)
            if os.path.isdir(src_path):
                os.mkdir(rpl_path)
                logging.info(f'Directory {item} from {source_path} was added to the {replica_path}.')
        
        for item in create_set:
            src_path = os.path.join(source_path, item)
            rpl_path = os.path.join(replica_path, item)
            if os.path.isfile(src_path):
                shutil.copyfile(src_path, rpl_path)
                logging.info(f'File {item} from {source_path} was added to the {replica_path}.')
            
        for item in samedata_set:
            rpl_path = os.path.join(replica_path, item)
            src_path = os.path.join(source_path, item)
            if os.path.isfile(src_path):
                if calculate_md5(src_path) != calculate_md5(rpl_path):
                    with open(src_path, 'rb') as src_file, open(rpl_path, 'wb') as rpl_file:
                        content = src_file.read()
                        rpl_file.write(content)
                        logging.info(f'File {item} from {replica_path} has been replaced with file from {source_path}')
                                            
        logging.info("Synchronization completed.")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Synchronization of 2 folders')
    parser.add_argument('source_path', type=str, help='enter address of your source folder')
    parser.add_argument('replica_path', type=str, help='enter address of your replica folder')
    parser.add_argument('log_path', type=str, help='enter address of your log file')
    parser.add_argument('time_interval', type=float, help='enter interval for syncronization')
    
    args = parser.parse_args()

    source_path = args.source_path
    replica_path = args.replica_path
    log_path = args.log_path
    time_interval = args.time_interval
                                                   
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(log_path)
    stream_handler = logging.StreamHandler()

    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)

    while True:
        sync(source_path, replica_path)
        time.sleep(time_interval)
