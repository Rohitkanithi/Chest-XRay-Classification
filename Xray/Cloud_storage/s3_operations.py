import os
import sys
from Xray.exception import XrayExeption

class S3Operation:
    def sync_folder_to_s3(self, folder:str, bucket_name: str, bucket_folder_name: str)-> None:
        try:
            command: str=(
                f"aws s3 sync(folder) s3://{bucket_name}/{bucket_folder_name}"
            )
            os.system(command)
        except Exception as e:
            raise XrayExeption(e,sys)
    
    def sync_folder_from_s3(self, folder:str, bucket_name: str, bucket_folder_name: str)-> None:
        try:
            command: str=(
                f"aws s3 sync {folder} s3://{bucket_name}/{bucket_folder_name}"
            )
        except Exception as e:
            raise XrayExeption(e,sys)
        
