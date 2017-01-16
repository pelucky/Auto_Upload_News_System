# coding:UTF-8

import config
import urllib2, urllib, cookielib, re, time
from mycookie import Mycookie

"""
Name: mypost.py
Author: pel
Date: 2015.10.12
Desc: Post the data to the server
"""

class Mypost:
    """My post class"""
    def __init__(self):
        """Set the configure"""
        self.mycookie = Mycookie()
        self.login_url = config.login_url
        self.login_send_header = config.login_send_header
        self.article_add_url = config.article_add_url


    def data_post(self, values, url, send_header):
        """The detail post code"""
        # Get the cookie into the urllib
        ckjar = self.mycookie.get_cookie()
        ckproc = urllib2.HTTPCookieProcessor(ckjar)
        opener = urllib2.build_opener(ckproc)
        
        # Post data and get return result
        post_data = urllib.urlencode(values)
        request_data = urllib2.Request(url, post_data, headers = send_header)
        f = opener.open(request_data)
        result = f.read()
        f.close()
        return result

    def post_login(self, username, password, code):
        """Post the login data to server"""
        values = {"ctl00$ContentPlaceHolder1$MemberName" : username,
            "ctl00$ContentPlaceHolder1$MemberPass" : password,
            "ctl00$ContentPlaceHolder1$CheckCode" : code,
            "__EVENTTARGET" : "",
            "__EVENTARGUMENT" : "",
            "__VIEWSTATE" : "/wEPDwUJNjIyMTU5NjYyZGQ=",
            "__EVENTVALIDATION" : "/wEWBQLwhorcCAKxtMbHCgKNvavEBwKCi/rDCQKM5+qlBA==",
            "ctl00$ContentPlaceHolder1$RegBtn": "登 录",
            }
        result = self.data_post(values, self.login_url, self.login_send_header)
        return result

       
    def post_upload(self, viewstate_result, eventvalidation_result, dict_input, content_title, post_content):
        """Post the upload data to server"""
        # POST the data with header and cookies
        values = {"__EVENTTARGET" : "",
        "__EVENTARGUMENT" : "",
        "__VIEWSTATE" : viewstate_result[0],                        # re return list!
        "__EVENTVALIDATION" : eventvalidation_result[0],
        "ctl00$ContentPlaceHolder1$ClassID" : dict_input["classID"],
        "ctl00$ContentPlaceHolder1$title" : content_title,
        "ctl00$ContentPlaceHolder1$Author" : dict_input["writer"],
        "ctl00$ContentPlaceHolder1$CopyFrom" : dict_input["writer"],
        "ctl00$ContentPlaceHolder1$Writer" : dict_input["writer"],
        "ctl00$ContentPlaceHolder1$Photor" : dict_input["photor"],
        "ctl00$ContentPlaceHolder1$startDate" : time.strftime("%Y-%m-%d"),
        "ctl00$ContentPlaceHolder1$endDate" : time.strftime("%Y-%m-%d"),
        "ctl00$ContentPlaceHolder1$Content" : post_content,
        "ctl00$ContentPlaceHolder1$Passer" : dict_input["passer"],
        "ctl00$ContentPlaceHolder1$Submit" : "保存",
        }
        result = self.data_post(values, self.article_add_url,self.login_send_header)
        return result

    def get_post_data(self, url, header, flag1, flag2 = None):
        """Get the column and post data"""
        request_data = urllib2.Request(url, headers = header)
        f = urllib2.urlopen(request_data)
        html = f.read()
        f.close()
        
        # RE the <option></option>
        if flag2 == None:
            match_result = re.findall(flag1, html)
            return match_result
        # RE the two value
        else:
            eventvalidation_result = re.findall(flag1, html)
            viewstate_result = re.findall(flag2, html)
            return eventvalidation_result, viewstate_result

    def check_login_result(self, result):
        """Check the result whether the result is success!"""
        success_flag = "成功登陆"
        m = re.search(success_flag, result)
        if m is not None:
            print "Login successfully!"
            # Store the auth cooie into file
            self.mycookie.store_cookie()
            
            # Get the column
            option_flag = '<option\svalue="(.*)">(.*)</option>'
            return self.get_post_data(self.article_add_url, self.login_send_header, option_flag)
        else:
            print "Login failed!"
            return False

    def check_upload_result(self, result):
        """Checkt the result whether the result is success!"""
        success_flag = "操作成功执行"
        m = re.search(success_flag, result)
        return m 
