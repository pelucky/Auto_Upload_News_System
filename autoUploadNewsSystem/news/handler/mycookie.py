# coding:UTF-8

import config
import urllib2, urllib, cookielib

"""
Name: mycookie.py
Author: pel
Date: 2015.10.12
Desc: get and set the cookies and get the check image
"""

class Mycookie:
    """My cookie"""
    def __init__(self):
        """Set the configure"""
        self.cookie_path_name = config.cookie_path_name
        self.code_url = config.code_url
        self.send_header = config.send_header
        self.image_path_name = config.image_path_name
        self.ckjar = cookielib.MozillaCookieJar(self.cookie_path_name)

    def store_cookie(self):
        self.ckjar.save(ignore_discard = True, ignore_expires = True)
        
    def set_cookie(self):
        """Get the cookie from server and save it to file"""
        req = urllib2.Request(self.code_url, headers = self.send_header)
        ckproc = urllib2.HTTPCookieProcessor(self.ckjar)
        opener = urllib2.build_opener(ckproc)
        file_head = opener.open(req)
        self.store_cookie()
        return file_head

    def get_image(self, img_head):
        """Use the cookie to get the check code image!"""
        f = open(self.image_path_name, 'wb')
        while True:
            data = img_head.read(1024*16)
            if len(data) == 0:
                break
            f.write(data)
        f.close()

    def get_cookie(self):
        """Get the cookie from the file"""
        self.ckjar.load(self.cookie_path_name, ignore_discard = True, ignore_expires = True)
        return self.ckjar
