import os
import hashlib
import logging
import argparse
import time

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

    logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

    source_set = file_set(source_path)
    replica_set = file_set(replica_path)
           
    def calculate_md5(path):
        md5 = hashlib.md5()

        if os.path.isfile(path):
            with open(path, 'rb') as file:
                while True:
                    data = file.read()
                    if not data:
                        break
                    md5.update(data)

        return md5.hexdigest()

    def calculate_subtree_md5(directory):
        md5 = hashlib.md5()

        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_md5 = calculate_md5(file_path)
                md5.update(file_md5.encode('utf-8'))

        return md5.hexdigest()

    source_hash = calculate_subtree_md5(source_path)
    replica_hash = calculate_subtree_md5(replica_path)
                
    def sync():
        delete_set = replica_set.difference(source_set)
        create_set = source_set.difference(replica_set)
        samedata_set = replica_set.intersection(source_set)

        if len(delete_set) or len(create_set) != 0:
            print("Synchronization needed.")

            for item in delete_set:
                item_path = os.path.join(replica_path, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                    logging.info(f'File {item} from {replica_path} was deleted.')
                elif os.path.isdir(item_path):
                    os.rmdir(item_path)
                    logging.info(f'Directory {item} from {replica_path} was deleted.')
                print(f'Next files was deleted: {item}')

            for item in create_set:
                src_path = os.path.join(source_path, item)
                rpl_path = os.path.join(replica_path, item)
                if os.path.isfile(src_path):
                    src_file = open(src_path, 'rb')
                    rpl_file = open(rpl_path, 'wb')
                    content = src_file.read()
                    rpl_file.write(content)
                    logging.info(f'File {item} from {source_path} was added to the {replica_path}.')
                    print(f'Next files has been created: {item}')
                elif os.path.isdir(src_path):
                    os.mkdir(rpl_path)
                    logging.info(f'Directory {item} from {source_path} was added to the {replica_path}.')
                    print(f'Next directories has been created: {item}')
            
        elif len(samedata_set) > 0 and source_hash != replica_hash:
            for item in samedata_set:
                if source_hash != replica_hash:
                    rpl_path = os.path.join(replica_path, item)
                    src_path = os.path.join(source_path, item)
                    if os.path.isfile(rpl_path):
                        os.remove(rpl_path)
                        src_file = open(src_path, 'rb')
                        rpl_file = open(rpl_path, 'wb')
                        content = src_file.read()
                        rpl_file.write(content)
                        logging.info(f'Files {item} from {replica_path} has been replaced with files from {source_path}')
                        print(f"Next files was replaced: {item}")
                                
            print("Synchronization completed.")
                  
        else:
            print("No synchronization needed. Source and replica are already synchronized.")
    
    while True:
        sync()
        time.sleep(time_interval)
