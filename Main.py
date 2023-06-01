import os
import shutil

source_path = "C:\\test\\Source"
replica_path = "C:\\test\\Replica"

def copy_job():
    shutil.copytree(source_path, replica_path, dirs_exist_ok=True)


copy_job()