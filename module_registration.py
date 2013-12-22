#coding=utf-8
import time, sys, getpass
import hack_validation
import urllib2, urllib, cookielib 


# Constant.
SITEURL = 'http://222.30.32.10'
VCURL = 'http://222.30.32.10/ValidateCode'
LOGINURL = 'http://222.30.32.10/stdloginAction.do'
ALREURL = 'http://222.30.32.10/xsxk/selectedAction.do'
MIANURL = 'http://222.30.32.10/xsxk/selectMianInitAction.do'
RMURL = 'http://222.30.32.10/xsxk/swichAction.do'
EXITURL = 'http://222.30.32.10/exitAction.do'

header_site = {
        'Host': '222.30.32.10', 
        'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8', 
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', 
        'Connection': 'keep-alive', 
        'Accept-Encoding': 'gzip,deflate,sdch', 
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4'
        }

header_vc = {
        'Host': '222.30.32.10', 
        'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8', 
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', 
        'Refferer': 'http://222.30.32.10', 
        'Connection': 'keep-alive', 
        'Accept-Encoding': 'gzip,deflate,sdch', 
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4'
        }

header_mian = {
        'Host': '222.30.32.10', 
        'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8', 
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', 
        'Refferer': 'http://222.30.32.10/xsxk/sub_xsxk.jsp', 
        'Connection': 'keep-alive', 
        'Accept-Encoding': 'gzip,deflate,sdch', 
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4'
        }

header_login_origin = {
        'Host': '222.30.32.10', 
        'Content-Length': '100', 
        'Cache-Control': 'max-age=0', 
        'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8', 
        'Origin': 'http://222.30.32.10', 
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', 
        'Connection': 'keep-alive', 
        'Content-Type': 'application/x-www-form-urlencoded', 
        'Refferer': 'http://222.30.32.10', 
        'Accept-Encoding': 'gzip,deflate,sdch', 
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4'
        }

header_login = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', 
        }

header_rm = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', 
        'Referer': 'http://222.30.32.10/xsxk/selectMianInitAction.do'
        }

header_exit = {
        'Host': '222.30.32.10', 
        'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8', 
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', 
        'Refferer': 'http://222.30.32.10/stdleft.jsp', 
        'Connection': 'keep-alive', 
        'Accept-Encoding': 'gzip,deflate,sdch', 
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4'
        }


#Get username and password
print 'User_name:', 
user_name = raw_input()
user_pwd = getpass.getpass('Password: ')


#Set cookie
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)


# Get the main site.
req = urllib2.Request(SITEURL, headers = header_site)
h = urllib2.urlopen(req)


# Get the validation code pic saved as 'vcpic', and hack it.
while True:
    vcpic = open('vcpic', 'w')

    req = urllib2.Request(VCURL, headers = header_vc)
    vcpic.write(urllib2.urlopen(req).read())

    vcpic.close()
    vc_code = hack_validation.get_validation_code('vcpic')
    if vc_code: 
        break


# Try to login.
post_data_login = {
        'operation': '', 
        'usercode_text': user_name, 
        'userpwd_text': user_pwd, 
        'checkcode_text': vc_code, 
        'submittype': '确 认'.decode('utf-8').encode('gbk')
        }
post_data_login = urllib.urlencode(post_data_login)

req = urllib2.Request(
        LOGINURL, 
        post_data_login, 
        header_login
        )
h = urllib2.urlopen(req)


# Check whether login is successful.
ok = '管理'
html = h.read().decode('gbk').encode('utf-8')
if html.find(ok) < 0:
    print 'Login error, please try again.'
    exit()



# Login is successful, then go to the xsxk main page.
req = urllib2.Request(
        MIANURL, 
        headers = header_mian
        )
h = urllib2.urlopen(req)

print '\nLogin is successful.\n'
print 'Welcome,', 
ok = '姓名'
html = h.read().decode('gbk').encode('utf-8')
i = html.find(ok)
stdname = html[i + 29: i + 38]
print stdname + '\n'


# Prepare to register the module.
print 'Enter at most 4 modules, sperated by a spcace:'
print 'For example, "0000 0001 9999 0003" or "0000 9999"\n'
print 'Now, enter:', 

xkxh = ['', '', '', '']
xkxhip = raw_input().split()
print '\nModule:', 
print ' '.join(xkxhip)
print 'In processing', 

i = 0
for x in xkxhip:
    xkxh[i] = x
    i += 1
    if i > 3: 
        break

post_data_rm = {
        'operation': 'xuanke', 
        'index': '', 
        'xkxh1': xkxh[0], 
        'xkxh2': xkxh[1], 
        'xkxh3': xkxh[2], 
        'xkxh4': xkxh[3], 
        'courseindex': ''
        }
post_data_rm = urllib.urlencode(post_data_rm)

req = urllib2.Request(
        RMURL, 
        post_data_rm, 
        header_rm
        )

'''
Start to register the module.
Sleep(5.1) is stable.
'''
bad = 1
while bad:
    print '.', 
    sys.stdout.flush()
    h = urllib2.urlopen(req)
    html = h.read().decode('gbk').encode('utf-8')
    if html.find('#333399') < 0:
        bad = 0
    time.sleep(5.1)


# Get the course that have been already registered.
#h = urllib2.urlopen(ALREURL)
#print h.read().decode('gbk').encode('utf-8')


# Exit.
req = urllib2.Request(EXITURL, headers = header_exit)
h = urllib2.urlopen(req)
