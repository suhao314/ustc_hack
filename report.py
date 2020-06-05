# 具有以 % 开头的注释的行需要自行酌情修改!
import re
import requests


# 改变标准输出的默认编码
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 


# 构造统一身份认证所需的数据
loginData = {
                'model':'uplogin.jsp', 
                'service':'https://weixine.ustc.edu.cn/2020/caslogin', 
                'username':'SA19000000',        # %学号
                'password':'passw0rd'           # %统一身份认证的密码
            }


# 设置 headers
headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}


# 统一身份认证的 URL
loginURL = 'https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fweixine.ustc.edu.cn%2F2020%2Fcaslogin'


# 进行统一身份认证
session = requests.Session()
resp = session.post(loginURL, loginData)


# 打开经过肥科统一身份认证后才能访问的企业微信页面(健康上报)
url = 'https://weixine.ustc.edu.cn/2020/home'
resp = session.get(url)


# 在登陆后返回的页面中查找上报所需的 _token
reg = r'<input type="hidden" name="_token" value="[a-zA-Z0-9]*">'
pattern = re.compile(reg)
result = pattern.findall(resp.content.decode('utf-8'))
reg = r'[a-zA-Z0-9]*[0-9]+[a-zA-Z0-9]*'
pattern = re.compile(reg)
_token = pattern.findall(result[0])[0]


# POST 健康上报所需的数据
reportData = {
                '_token':_token,
                'now_address':'1', 
                'gps_now_address':'',
                'now_province':'530000',      # %所在省
                'gps_province':'', 
                'now_city':'530400',          # %所在市
                'gps_city':'',
                'now_detail':'',
                'body_condition':'1',
                'body_condition_detail':'',
                'now_status':'2',
                'now_status_detail':'',
                'has_fever':'0',
                'last_touch_sars':'0',
                'last_touch_sars_date':'',
                'last_touch_sars_detail':'',
                'last_touch_hubei':'0',
                'last_touch_hubei_date':'',
                'last_touch_hubei_detail':'',
                'last_cross_hubei':'0',
                'last_cross_hubei_date':'',
                'last_cross_hubei_detail':'',
                'return_dest':'1',
                'return_detail':'',
                'other_detail':'无'
            }


# POST 
reportURL = 'https://weixine.ustc.edu.cn/2020/daliy_report'
resp = session.post(reportURL, reportData)


# 检查是否上报成功
reg = r'上报成功，最近一次上报是[\S]*请每日按时打卡 '
pattern = re.compile(reg)
result = pattern.findall(resp.content.decode('utf-8'))
if len(result)==1:
    print(result[0])
else:
    print("Oops, FAILED!")
