# 网站登录自动化脚本 (www.woaige.net)

## 简介
这是一个使用 Python 自动登录 `www.woaige.net` 的脚本。  
它通过 `requests` 模拟浏览器请求，先获取验证码图片，然后调用第三方打码平台 [jfbym.com](http://www.jfbym.com) 识别验证码，最后提交登录表单完成登录。

## 环境要求
- Python 3.x
- `requests` 库

## 安装依赖
```bash
pip install requests
