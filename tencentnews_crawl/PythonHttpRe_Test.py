import requests


# make a simple get request
r = requests.get("https://api.github.com/events")
# and make a simple post request
r2 = requests.post('https://httpbin.org/post', data={'key': 'value'})
# 其他的请求比如 PUT、DELETE、HEAD、OPTIONS
# r3 = requests.put('https://httpbin.org/put', data={'key':'value'})
# r4 = requests.delete('https://httpbin.org/delete')
# r5 = requests.head('https://httpbin.org/get')
# r6 = requests.options('https://httpbin.org/get')
print(r.text)
print(r.content)
print(type(r.text))






