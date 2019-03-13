from bs4 import BeautifulSoup
import requests


respon = requests.get("https://new.qq.com/cmsn/20190307/20190307002937.html")
soup = BeautifulSoup(respon.text, features="html.parser")
# print(soup.prettify())
# print(soup.title)
# print(soup.title.name)
div_content_tags = soup.find_all('p', {'class': 'one-p'})
content_str = ""
for item in div_content_tags:
    if item.string is not None:
        content_str += item.string

print(content_str)





