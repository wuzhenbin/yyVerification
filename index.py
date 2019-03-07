

# 'Google Chrome' --remote-debugging-port=9222 --user-data-dir="/Users/chenpin/Downloads/package/seleium"

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

from PIL import Image
import time, random
from chaojiying import Chaojiying
from io import BytesIO

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# 题目类型 坐标多选,返回1~4个坐标,如:x1,y1|x2,y2|x3,y3
CHAOJIYING_KIND = 9004

class YYVerification: 
    def __init__(self):
        self.url = 'https://aq.yy.com/p/reg/account.do?appid=&url=&fromadv=udbclsd_r' 
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)
        self.chaojiying = Chaojiying()
        # self.driver.get(self.url)

    def get_screenshot(self):
        screenshot = self.driver.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_points(self, captcha_result):
        """
        解析识别结果
        :param captcha_result: 识别结果
        :return: 转化后的结果
        """
        groups = captcha_result.get('pic_str').split('|')
        locations = [[int(number) for number in item.split(',')] for item in groups]
        return locations

    def get_img_element(self):
        """
        获取验证图片对象
        :return: 图片对象
        """
        element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pw_main')))
        return element

    def touch_click_words(self, locations):
        """
        点击验证图片
        :param locations: 点击位置
        :return: None
        """

        for location in locations:
            print(location)
            ActionChains(self.driver).move_to_element_with_offset(self.get_img_element(), location[0]/2, location[1]/2).click().perform()
            time.sleep(1)


    def main(self):
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//iframe')))
        i = self.driver.find_element_by_xpath('//iframe')
        url_1 = i.get_attribute('src')
        self.driver.get(url_1)

        # time.sleep(1)

        # 保存整张网页
        screenshot = self.get_screenshot()
        screenshot.save('yy.png')
        time.sleep(1)

        # 剪切图片
        captcha = self.get_img_element()

        left = captcha.location['x']
        top = captcha.location['y']
        right = captcha.location['x'] + captcha.size['width']
        bottom = captcha.location['y'] + captcha.size['height']

        im = Image.open('yy.png')
        im = im.crop((left*2, top*2, right*2, bottom*2))
        # im.show()

        # 识别验证码
        bytes_array = BytesIO()
        im.save(bytes_array, format('PNG'))
        result = self.chaojiying.PostPic(bytes_array.getvalue(), CHAOJIYING_KIND)
        # print(result)
        locations = self.get_points(result)
        self.touch_click_words(locations)

if __name__ == '__main__':
    yy = YYVerification()
    yy.main()



