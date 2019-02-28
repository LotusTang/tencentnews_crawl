import re


# 测试是否正则表达式匹配
text = ""
patterns = [
    r'(.*)/omn/([A-Z0-9]{16,19})',
    r'(.*)/omn\\/(\d{8})\\/(.+)\.html',
    r'(.*)/cmsn/([A-Z0-9]{16,19})',
    r'(.*)/cmsn/(\d{8})/(.+)\.html',
    r'(.*)/a/(\d{8})/(\d+)\.htm'
        ]
# 果然是需要两个反斜线，因为一个反斜线加上一个斜线的话，会被当做一个斜线处理，因为斜线也是元字符
for pattern in patterns:
    match = re.search(pattern, text)
    if match:
        print('Found Match')
        print(text[match.start():match.end()])








