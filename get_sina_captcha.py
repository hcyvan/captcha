import os
import time
import requests

url = 'https://login.sina.com.cn/cgi/pin.php?r=54589434&s=0&p=tc-d221e148ca6446b8ee0af43e78aabbe1a64d'


def get_sina_captcha(dir='sina'):
    response = requests.get(url)
    img = response.content
    with open(os.path.join(dir, str(int(time.time() * 1000)) + '.png'), 'wb') as f:
        f.write(img)


if __name__ == '__main__':
    for i in range(100):
        print(i)
        get_sina_captcha()
