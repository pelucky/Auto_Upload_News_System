# coding:UTF-8
from django.shortcuts import render
from handler import config
from handler.mycookie import Mycookie
from handler.mypost import Mypost
from handler.myunzip import Myunzip
from handler.mypic import Mypic
import re
# Create your views here.

"""
Author: pel
Date: 2015.09.23
Desc: view.py and get in the login page!
"""

# Avoid the unicode error!
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def index(request):
    """Get the Login page."""
    return render(request, 'news/index.html')

def login(request):
    """Store the code image cookies and login"""
    errors = ""
    if request.method == 'POST':
        mypost = Mypost()
        username = request.POST.get("username")
        password = request.POST.get("password")
        code = request.POST.get("code")
        result = mypost.post_login(username, password, code)
        config.match_result = mypost.check_login_result(result)
        if config.match_result:
            # Set the default input into the textbox
            default_dict = config.default_input_dict
            default_dict["match_result"] = config.match_result
            return render(request, 'news/upload.html', default_dict)
        # The error password or username or code
        else:
            errors = "用户名或密码或验证码输入错误！"
            return render(request, 'news/login.html', {"errors" : errors, "username" : username, "code": code})
    else:
        mycookie = Mycookie()
        image_head = mycookie.set_cookie()
        mycookie.get_image(image_head)
        return render(request, 'news/login.html', {"errors": errors, "username" : "", "code": ""})
    
def upload(request):
    """To upload file"""
    errors = ""
    dict_input = {}
    if request.method == 'POST':
        # Get the post data
        dict_input["bigPicWidth"] = request.POST.get("bigPicWidth")
        dict_input["bigPicHeight"] = request.POST.get("bigPicHeight")
        dict_input["picWidth"] = request.POST.get("picWidth")
        dict_input["picHeight"] = request.POST.get("picHeight")
        dict_input["classID"] = request.POST.get("classID")
        dict_input["writer"] = request.POST.get("writer")
        dict_input["photor"] = request.POST.get("photor")
        dict_input["passer"] = request.POST.get("passer")
        dict_input["content"] = request.POST.get("content")
        # Change the content \r\n to br or javascript will not read mulit line
        dict_input["content_br"] = dict_input["content"].replace("\r\n","<br>")
        file_obj = request.FILES.get("upload_file", None)           # Note request.FILES.get() wirte right
        
        # Make sure the file is not empty
        if file_obj:
            # Unzip and remove the file
            myunzip = Myunzip(file_obj)
            myunzip.upload_file()
            # Make sure the file is zip
            if myunzip.check_file():
                myunzip.unzip_file()
                zfile_name = myunzip.list_file()
                myunzip.remove_zip_file()

                # Make sure the pic file is right, not xxx/1.jpg
                if True:
                    # Check the image size
                    if True:
                        # Check the image name in the content
                        if True:
                            # Use the cookies to get two values
                            mypost = Mypost()
                            eventvalidation_flag = 'id="__EVENTVALIDATION"\svalue="(.*)"\s/>'
                            viewstate_flag = 'id="__VIEWSTATE"\svalue="(.*)"\s/>'
                            (eventvalidation_result, viewstate_result) = mypost.get_post_data(mypost.article_add_url, mypost.login_send_header, eventvalidation_flag, viewstate_flag)

                            # Upload the image to the server
                            mypic = Mypic()
                            pic_dict = mypic.upload_image(zfile_name)

                            # =============================Create the css style=============================
                            line_list = dict_input["content"].splitlines()
                            # Cut the title
                            content_title = line_list[0]
                            
                            post_content = ""
                            # Read the next line
                            for line_index in xrange(1, len(line_list)):
                                lstriped_line = line_list[line_index].lstrip()
                                pic_count = 0
                                if lstriped_line:
                                    # The pic and word start
                                    m = re.findall("(\d+)/\s*(\S+)", lstriped_line)     # The two pic
                                    n = re.findall("(\d+)/$", lstriped_line)            # The big one pic
                                    # The two pic
                                    if m:
                                        # It begins with digital and it comes with pic!
                                        post_content += '<tr>'
                                        for pic_index in xrange(len(m)):
                                            post_content += '<td><img alt="" width="' + str(dict_input["picWidth"]) + '" height="' + str(dict_input["picHeight"]) + '" src="' + pic_dict[m[pic_index][0]] + '" /></td>'
                                        post_content += '</tr><tr>'
                                        for pic_index in xrange(len(m)):
                                            post_content += '<td style="text-align: center"><span style="font-family: 仿宋_GB2312; font-size: 16pt; mso-hansi-font-family: Dotum; mso-bidi-font-family: "Times New Roman"; mso-font-kerning: 1.0pt; mso-ansi-language: EN-US; mso-fareast-language: ZH-CN; mso-bidi-language: AR-SA">' + m[pic_index][1] + '</span></td>'
                                        post_content += '</tr>'
                                     # The big one pic
                                    elif n:
                                        # It is a big pic!
                                        post_content += '<p style="text-align: center"><img alt="" width="' + str(dict_input["bigPicWidth"]) + '" height="' + str(dict_input["bigPicHeight"]) + '" src="' + pic_dict[n[0]] + '" /></p>'                   
                                    else:
                                        # The table start
                                        if re.search("^//", lstriped_line):
                                            post_content += '<table border="1" cellspacing="1" cellpadding="1" width="200" align="center"><tbody>'
                                        # The table end
                                        elif re.search("^##", lstriped_line):
                                            post_content += '</tbody></table>'
                                        # A new paragraph
                                        else:
                                            post_content += '<p align="left" style="text-align:left;text-indent:28.0pt; mso-char-indent-count:2.0;line-height:28.0pt;mso-line-height-rule:exactly" class="MsoNormal"><span style="font-size:14.0pt;font-family:宋体;mso-ascii-font-family:Calibri; mso-ascii-theme-font:minor-latin;mso-fareast-font-family:宋体;mso-fareast-theme-font: minor-fareast;mso-hansi-font-family:Calibri;mso-hansi-theme-font:minor-latin">    ' + lstriped_line + "</span></p>"
                            # ===============================End=====================================

                            result = mypost.post_upload(viewstate_result, eventvalidation_result, dict_input, content_title, post_content)
                            if mypost.check_upload_result(result):
                                print "Upload successfully!"
                                return render(request, 'news/result.html')
                            # The upload is wrong, maybe some reason!
                            else:
                                print "Upload failed!"
                        # The image is not the right size
                        else:
                            pass
                    # The image is not in content
                    else:
                        pass
                # The unzip file is xxx/1.jpg not ./1.jpg
                else:
                    pass
            # The Zip file is invalid!
            else:
                # Delete invalid file
                myunzip.remove_zip_file()
                dict_input["errors"] = "压缩文件错误，请确保为zip格式压缩包！"
                dict_input["match_result"] = config.match_result
                return render(request, 'news/upload.html', dict_input)
        # The unzip file is not upload
        else:
            dict_input["errors"] = "请上传zip格式压缩包！"
            dict_input["match_result"] = config.match_result
            print dict_input["content"]
            return render(request, 'news/upload.html', dict_input)
    # Get the page
    else:
        errors = "非法请求！请先登录再上传新闻！"
        return render(request, 'news/login.html', {"errors" : errors, "username" : "", "code": ""})
        
def result(request):
    """For display the result!"""
    return render(request, 'news/result.html')
