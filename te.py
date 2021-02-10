import time
import os
from selenium import webdriver
from PIL import Image
import numpy as np
import pytesseract
from collections import defaultdict


# class DouyuError(Exception):
#     pass

# #url_douyu = 'https://web.sinsyth.com/lxapi/douyujx.x?roomid=9999'
# url_douyu = 'https://www.douyu.com/gapi/rkc/directory/mixList/2_3/1'
# try:
#     response = requests.get(url_douyu)
# except requests.RequestException:
#     raise DouyuError("Requests Error")

# if response.status_code >= 400:
#     if response.status_code == 401:
#         raise DouyuError("Unauthorized request 401.")
#     if response.status_code == 503:
#         raise DouyuError("The server is busy or you exceeded limits. Please wait 30s and try again.")
#     raise DouyuError("Failed to retrieve data: %s. URL: %s" % (response.status_code, url_douyu))


# for i in range(0,len(x['data']['rl'])):
#     print(str(i)+":"+
#           "主播名字:"+x['data']['rl'][i]['nn']+
#           "    主播标题:"+x['data']['rl'][i]['rn']+
#           "   火热度:"+str(x['data']['rl'][i]['ol'])+'\n'+
#           "主播地址:"+"https://www.douyu.com"+x['data']['rl'][i]['url'])
# status = 0 # 0 表示未开播

# temp = status
# if results['info']== "Live broadcasting has been closed":   
#     status = 0 
# elif results['info'] == 'Check-OK':
#     status = 1
# if status != temp and status == 1:
#     open_content="xg 开播了！！！"
#     print(open_content)

# a = [1,2,3,2,2]
# b = [4,5,6,4,5]
# c = [7,9,9,7,9]
# mylist=[a,b,c]
# ylist = np.array(mylist).T
# data_pd=pd.DataFrame(data=ylist)
# data_pd.to_csv('./danmu_data2.csv')

# image_path = './image'
# if not os.path.exists(image_path ):
#     os.makedirs(image_path )

    
# # Create a new cromedriver

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('window-size=1920x1080')
# chrome_options.add_argument("--start-maximized")
# # Go to www.google.com
# driver = webdriver.Chrome(executable_path=r"D:\Program\chromedriver.exe", chrome_options=chrome_options)
# driver.get("https://www.douyu.com/60937")
# time.sleep(5)
# screenshot_name = "my_screenshot_name.png"
# driver.save_screenshot(screenshot_name)

# img = Image.open('my_screenshot_name.png')
# array = np.array(img)[229:242,356:407,:]
# new_img = Image.fromarray(array)
# new_img.save('newimg.png')

# img = Image.open('newimg.jpg')
# img = img.convert('L')
# img.show()
# text = pytesseract.image_to_string(img)

# # exclude_char_list = ' .:\\|\'\"?![],()~@#$%^&*_+-={};<>/¥'
# # text = ''.join([x for x in text if x not in exclude_char_list])
# print(text)
# # print(img.size)
# #[341:407,232:273]
def get_threshold(image):
    pixel_dict = defaultdict(int)

    # 像素及该像素出现次数的字典
    rows, cols = image.size
    for i in range(rows):
        for j in range(cols):
            pixel = image.getpixel((i, j))
            pixel_dict[pixel] += 1

    count_max = max(pixel_dict.values()) # 获取像素出现出多的次数
    pixel_dict_reverse = {v:k for k,v in pixel_dict.items()}
    threshold = pixel_dict_reverse[count_max] # 获取出现次数最多的像素点

    return threshold

def get_bin_table(threshold):
    # 获取灰度转二值的映射table
    table = []
    for i in range(256):
        rate = 0.1 # 在threshold的适当范围内进行处理
        if threshold*(1-rate)<= i <= threshold*(1+rate):
            table.append(1)
        else:
            table.append(0)
    return table

img = Image.open("newimg.png")
img = img.convert('L')
#max_pixel = get_threshold(img)
table = get_bin_table(threshold=240)
out = img.point(table, '1')
out.save('./img_gray.jpg')
# text = pytesseract.image_to_string(Image.open("newimg.png"),lang="eng")
# print(text)