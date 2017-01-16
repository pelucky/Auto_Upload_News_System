# coding:UTF-8

"""
Name: config.py
Author: pel
Date: 2015.10.12
Desc: This file is system config!
"""
import os

# Set the cookie and file location
hostIP = "18.18.96.6"
file_path = os.getcwd() + "/news"
static_file_path = file_path + "/static/news/"
cookie_name = "cookies.txt"
image_name = "code_img.jpg"
cookie_path_name = os.path.join(static_file_path, cookie_name)
image_path_name = os.path.join(static_file_path, image_name)
code_url = 'http://' + hostIP + '/tools/verifyimagepage.aspx'       # image Code url
send_header = { 
        "Host" : hostIP,
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language" : "zh-CN,zh;q=0.8",
        "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36",
        "Referer" : "http://" + hostIP + "/user/login.aspx",
        "Connection" : "keep-alive",
        "Origin" : "http://" + hostIP,
        "Content-Type" : "application/x-www-form-urlencoded",
        "Cache-Control" : "max-age=0",
        }

# Set the login and upload config
login_url = 'http://' + hostIP + '/user/login.aspx'
login_send_header = {
    "Host" : hostIP,
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language" : "zh-CN,zh;q=0.8",
    "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36",
    "Referer" : "http://" + hostIP + "/user/login.aspx",
    "Connection" : "keep-alive",
    "Origin" : "http://" + hostIP,
    "Content-Type" : "application/x-www-form-urlencoded",
    }
article_add_url = 'http://' + hostIP + '/user/articleadd.aspx'
upload_file_path = file_path + "/upload/news/"
upload_img_url = 'http://' + hostIP + '/FCKeditor/editor/filemanager/connectors/aspx/upload.aspx?Type=Image'

# Upload the default value
default_input_dict = {
    "bigPicWidth" : "510",
    "bigPicHeight" : "376",
    "picWidth" : "310",
    "picHeight" : "233",
    "classID" : "1",
    "writer" : "作训股 涂聪",
    "photor" : "作训股 涂聪",
    "passer" : "金幕生 参谋长",
}
# Get the column
match_result = {}
