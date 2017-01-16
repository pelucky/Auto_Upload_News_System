# coding:UTF-8

import config
import zipfile, os

"""
Name: myunzip.py
Author: pel
Date: 2015.10.13
Desc: Unzip the image and check the unzip file
"""

class Myunzip:
    """My unzip class"""
    def __init__(self, file_obj):
        """Set the configure"""
        self.file_obj = file_obj
        self.upload_file_path = config.upload_file_path
        self.zip_file_path = self.upload_file_path + self.file_obj.name

    def upload_file(self):
        """Upload the unzip file to the server"""
        zip_file = open(self.zip_file_path, 'wb+')
        for chunk in self.file_obj.chunks():
            zip_file.write(chunk)
        zip_file.close()

    def check_file(self):
        """Check the file is the vaild zip file"""
        return zipfile.is_zipfile(self.zip_file_path)
    
    def unzip_file(self):
        """Unzup the file"""
        zfile = zipfile.ZipFile(self.zip_file_path, 'r')
        zfile.extractall(self.upload_file_path)

    def list_file(self):
        return zipfile.ZipFile(self.zip_file_path, 'r').namelist()

    def remove_zip_file(self):
        os.remove(self.zip_file_path)

