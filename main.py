if __name__ == "__main__":

    import os
    import hashlib
    import logging
    import argparse

    source_path = "C:\\test\\Source"
    replica_path = "C:\\test\\Replica"

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

    print(source_set)
    print(replica_set)

   

    if source_set != replica_set:
        print("Synchronization needed.")

        for item in replica_set:
            item_path = os.path.join(replica_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                os.rmdir(item_path)

        for item in source_set:
            src_path = os.path.join(source_path, item)
            rpl_path = os.path.join(replica_path, item)
            if os.path.isfile(src_path):
                src_file = open(src_path, 'rb')
                rpl_file = open(rpl_path, 'wb')
                content = src_file.read()
                rpl_file.write(content)
            elif os.path.isdir(src_path):
                os.mkdir(rpl_path)
            
        print("Synchronization completed.")
    else:
        print("No synchronization needed. Source and replica are already synchronized.")

    def calculate_file_hash(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
        hash_object = hashlib.md5(content)
        file_hash = hash_object.hexdigest()
        return file_hash
    
