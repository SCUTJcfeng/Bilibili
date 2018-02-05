from selenium import webdriver
import pymysql,time
from selenium.webdriver.support import expected_conditions
import random
m = "https://space.bilibili.com/"
'''
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.resourceTimeout"] = 30
dcap["phantomjs.page.settings.loadImages"] = False
driver = webdriver.PhantomJS(desired_capabilities =dcap)
'''

chromeOptions = webdriver.ChromeOptions()
#chromeOptions.add_argument('--proxy-server=http://116.52.232.22:9999')
prefs = {"profile.managed_default_content_settings.images":2}
chromeOptions.add_experimental_option("prefs",prefs)
chromeOptions.add_argument('--user-agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
driver = webdriver.Chrome(chrome_options = chromeOptions)
db = pymysql.connect(host='localhost',user='root',password='root',database='userinfo',charset='utf8')

'''
with db.cursor() as cursor:
            cursor.execute("select max(id) from bilibili")
            if cursor._rows[0][0] != None:
                tu = (cursor._rows[0])
                id = tu[0]
'''
id= 2500000
uid = ''
name = ''
gender = ''
title = ''
content = ''
lv = ''
follow = ''
fan = ''
play = ''
regTime = ''
birthday = ''
location = ''


user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

def RandomUA():
    chromeOptions.add_argument('--user-agent=' + random.choice(user_agent_list))
    driver = webdriver.Chrome(chrome_options = chromeOptions)


while True:
    try:
        id += 1
        with db.cursor() as cursor:
            cursor.execute("select id from bilibili where id = %d limit 1" % id)
            if  cursor.rowcount == 1:
                print("ID" + str(id) + "数据库已存在")
                continue
        url = m +str(id)
        #RandomUA()
        alert =  expected_conditions.alert_is_present().__call__(driver)
        if alert:
            alert.accept()
            #driver.switch_to_alert().accept()
            #driver.refresh()
            #time.sleep(2)
            #if expected_conditions.alert_is_present(driver):
            #    driver.switch_to_alert().accept()
            #    continue
        driver.delete_all_cookies()
        driver.get(url)
        time.sleep(1.3)
        uid = driver.find_element_by_xpath('//div[@class="item uid"]/span[2]').text
        name = driver.find_element_by_xpath("//*[@id='h-name']").text
        gender = driver.find_element_by_xpath("//*[@id='h-gender']").get_attribute("class")
        gender = gender.replace("icon gender","")
        gender = gender.replace(" ","")
        title = driver.find_element_by_xpath("//div[@class='h-basic-spacing']/div").text
        title = title.replace('\\',"\\\\")
        title = title.replace("'","\\'")

        content = driver.find_element_by_xpath('//*[@id="i-ann-display"]').text
        content = content.replace('\\',"\\\\")
        content = content.replace("'","\\'")

        lv = driver.find_element_by_xpath("//div[@class='h-basic']/div/a[1]").get_attribute("lvl")
        follow = driver.find_element_by_xpath("//*[@id='n-gz']").text
        fan = driver.find_element_by_xpath('//*[@id="n-fs"]').text
        try:
            play = driver.find_element_by_xpath('//*[@id="n-bf"]').text
        except:
            play = ""
        regTime = driver.find_element_by_xpath('//div[@class="item regtime"]/span[2]').text;#'//*[@id=\"page-index\"]/div[2]/div[6]/div[2]/div/div/div[1]/div[2]/span[2]'"
        birthday = driver.find_element_by_xpath('//div[@class="item birthday"]/span[2]').text
        location = driver.find_element_by_xpath('//div[@class="item geo"]/span[2]').text;
        data = (id,uid,name,gender,title,content,lv,follow,fan,play,regTime,birthday,location)
        sql = "insert into bilibili (id,uid,name,gender,title,content,lv,follow,fan,play,regTime,birthday,location) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % data
        with db.cursor() as cursor:
            cursor.execute(sql)
            db.commit()
            print("ID" + str(id) + "已添加进数据库")
            #driver.quit()
    except Exception as e:
        try:
            uid = ''
            name = ''
            gender = ''
            title = ''
            content = ''
            lv = ''
            follow = ''
            fan = ''
            play = ''
            regTime = ''
            birthday = ''
            location = ''
            data = (id,uid,name,gender,title,content,lv,follow,fan,play,regTime,birthday,location)
            sql = "insert into bilibili (id,uid,name,gender,title,content,lv,follow,fan,play,regTime,birthday,location) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % data
            with db.cursor() as cursor:
                cursor.execute(sql)
                db.commit()
                print("空" + str(id) + "添加到数据库")
        except Exception as e:
            pass
        #driver.quit()
        continue
        

