import os
import re
import urllib
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd

import MyImportantInfo as MIF


def GetHtmlText():
    today = datetime.date.today().strftime("%Y-%m-%d")
    username = "even311379@hotmail.com"
    password = MIF.MyFB_password()

    profile = webdriver.FirefoxProfile()
    profile.set_preference("dom.webnotifications.enabled", False)  # Finally, turned off webnotifications...
    profile.update_preferences()

    driver = webdriver.Firefox(firefox_profile=profile)

    driver.get("http://www.facebook.com")

    driver.find_element_by_id("email").send_keys(username)
    driver.find_element_by_id("pass").send_keys(password)

    driver.find_element_by_id("loginbutton").click()

    # driver.get("https://www.facebook.com/groups/SpiderTw/")
    
    '''
    FB 社團  非會員一進去會被redirect 去/about
    要改以
    https://www.facebook.com/groups/SpiderTw/?ref=direct
    進入
    '''
    driver.get("https://www.facebook.com/groups/SpiderTw/?ref=direct")
    

    # 將視窗往下滑 until??

    for i in range(10):
        driver.execute_script("window.scrollTo(0, {})".format(4000 * (i + 1)))
        time.sleep(1)
        htmltext = driver.page_source

    htmltext = driver.page_source

    with open(today+'.html', 'w', encoding='utf-8') as f:
        f.write(htmltext)

    driver.close()
    return htmltext

def load_htmltext():
    today = datetime.date.today().strftime("%Y-%m-%d")
    try:
        with open(today+'.html', encoding='utf-8') as f:
            htmltext = f.read()
        return htmltext
    except:
        return None


def parse_htmltext(htmltext, start_date, end_date):

    # declare empty spaces for store target data
    post_id = []
    post_url = []
    post_person = []
    post_time = []
    post_text = []
    N_post_imgs = []
    post_imgs_urls = []
    
    # create folder to store imgs
    today = datetime.date.today().strftime("%Y-%m-%d")
    try:
        if not os.path.exists('imgs/'+today):
            os.makedirs('imgs/'+today)
    except OSError:
        print('Error: Fail to create directory: imgs/'+today)

    cstart_date = time.mktime(start_date.timetuple())
    cend_date = time.mktime(end_date.timetuple())

    # parse html to articles
    soup = BeautifulSoup(htmltext, 'html.parser')
    articles = soup.select('div[role="article"]')
    for article in articles:

        if 'post' in article['id']:
            if not re.findall('data-utime="(.*?)"', str(article)):
                print(article['id'],'_ no post time!!??')
                continue
            post_ctime = int(re.findall('data-utime="(.*?)"', str(article))[0])
            if post_ctime >= cstart_date and post_ctime <= cend_date:
                ID = re.findall('_(\d+?):',article['id'])[0]
                POSTER_NAME = BeautifulSoup(str(article), 'html.parser').select('h5')[0].select('a')[0].text
                if not re.findall('<p>(.*)</p>',str(article)):
                    print('A post contains no text is detected...')
                    continue
                POST_TEXT = re.sub('(<.*?>)' ,'' ,re.findall('<p>(.*)</p>',str(article))[0])

                post_id.append(ID)
                post_url.append('https://www.facebook.com/groups/SpiderTw/permalink/' + ID)
                post_person.append(POSTER_NAME)
                post_time.append(time.ctime(post_ctime))
                post_text.append(POST_TEXT)

                # handling pictures
                pic_regions = article.select('a[rel="theater"]')
                pic_urls = []
                if pic_regions:
                    for i, pic_region in enumerate(pic_regions):
                        try:
                            url = pic_region['data-ploi'].replace('amp;','')
                            savePic(url,'imgs/{0}/{1}_{2}.jpg'.format(today,ID,i))
                            pic_urls.append(url)
                        except Exception as e:
                            print(e)
                            print("Fail to location img url, maybe it doesn't have one?")

                    N_post_imgs.append(len(pic_urls))
                    post_imgs_urls.append(pic_urls)
                else:
                    pic_urls.append('No image')
                    N_post_imgs.append(0)
                    post_imgs_urls.append('No image urls')

    pd.DataFrame(dict(
        post_id=post_id,post_time=post_time,post_url=post_url,
        post_person=post_person,post_text=post_text,
        N_post_imgs=N_post_imgs,post_imgs_urls=post_imgs_urls),
        ).to_excel(today+'_FB_scraper_data.xlsx')

def savePic(url,name):
	if url !="":
		urllib.request.urlretrieve(url,name)

if __name__ == '__main__':
    if load_htmltext():
        htmltext = load_htmltext()
    else:
        htmltext = GetHtmlText()

    parse_htmltext(htmltext, datetime.date(2018, 11, 25), datetime.date(2018, 12, 3))



