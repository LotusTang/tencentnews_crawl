str = "ddwada"
try:
    str.index("123")
except ValueError:
    print("substring no found, josn格式出现问题")
else:
    print("没有问题")
finally:
    print("结束")
