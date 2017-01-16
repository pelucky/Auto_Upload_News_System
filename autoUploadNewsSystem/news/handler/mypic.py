# coding:UTF-8

import config
import time, urllib2, os, re

# Post the image with poster
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from mycookie import Mycookie

"""
Name: mypic.py
Author: pel
Date: 2015.10.13
Desc: Check the image and upload image to server
"""

class Mypic:
    """My pic class"""
    def __init__(self):
        """Set the configure"""
        self.upload_img_url = config.upload_img_url
        self.upload_file_path = config.upload_file_path

    def check_image(self):
        """Check the image"""
        pass

    def upload_image(self, zfile_name):
        """Upload the image to the server"""
        # Use the Poster
        mycookie = Mycookie()
        mycookie.get_cookie()
        opener = register_openers()
        opener.add_handler(urllib2.HTTPCookieProcessor(mycookie.ckjar))

        # Upload the image and get the image's URL
        pic_dict = {}
        for pic_name in zfile_name:
            # Without delaying 10ms for every image upload, it will not success!
            time.sleep(0.01)
            datagen, headers = multipart_encode({"NewFile": open(self.upload_file_path + pic_name, "rb")})
            request_data = urllib2.Request(self.upload_img_url, datagen, headers)
            f = urllib2.urlopen(request_data)
            result = f.read()
            f.close()

            # Use '?' for the lazy fit
            pic_url_flag = "window\.parent\.OnUploadCompleted\(0\,'(.*?)'\,'"
            pic_url_result = re.findall(pic_url_flag, result)
            pic_dict[pic_name.split(".")[0]] = pic_url_result[0]      # The RE return a list
            os.remove(self.upload_file_path + pic_name)
        return pic_dict

