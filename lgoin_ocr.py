import requests
import base64

# 定义验证码识别函数，使用第三方打码平台（www.jfbym.com）
def verify():
    # 打开刚刚保存的验证码图片文件（test.png），以二进制只读方式
    with open('test.png', 'rb') as f:
        # 读取图片内容，进行base64编码，再解码为字符串（因为json需要字符串格式）
        b = base64.b64encode(f.read()).decode()
    
    # API请求地址
    url = "http://api.jfbym.com/api/YmServer/customApi"
    # 构造请求数据，包含token（用户中心的密钥）、类型（10103代表通用识别）和图片的base64数据
    data = {
        "token": "TOKEN",        # 需要替换为实际的token
        "type": "10103",          # 验证码类型，根据平台文档填写
        "image": b,
    }
    # 请求头，声明发送json数据
    _headers = {
        "Content-Type": "application/json"
    }
    # 发送POST请求，参数使用json=序列化data，并获取响应的JSON数据
    response = requests.request("POST", url, headers=_headers, json=data).json()
    # 从返回的JSON中提取识别出的验证码文本（具体路径根据平台返回结构调整）
    return response["data"]["data"]

# 模拟浏览器请求的 headers
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",  # 登录时发送表单数据
    "Origin": "http://www.woaige.net",
    "Referer": "http://www.woaige.net/login.php?jumpurl=",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0"
}

# 创建一个会话对象，用于保持cookie等会话信息
session = requests.session()
# 为会话设置统一的请求头
session.headers = headers

# 第一步：获取验证码图片
# 发送GET请求到验证码生成地址（code.php），后面的随机数用于防止缓存
res = session.get("http://www.woaige.net/code.php?0.3171868068327388")
# 将返回的图片内容写入本地文件 test.png，供后续识别使用
with open('test.png', 'wb') as w:
    w.write(res.content)

# 第二步：构造登录表单数据
data = {
    "LoginForm[username]": "username",   # 用户名，需要替换为实际账号
    "LoginForm[password]": "password",   # 密码，需要替换为实际密码
    "LoginForm[captcha]": verify(),      # 验证码，调用上面的识别函数获取
    "action": "login",                    # 可能是表单中的一个标识字段
    "submit": " 登  录 "                  # 提交按钮的显示文本（可能包含特殊空格）
}

# 第三步：发送POST请求进行登录
res = session.post("http://www.woaige.net/login.php", data=data)
# 打印登录后的响应内容（可能是登录成功或失败的页面）
print(res.text)