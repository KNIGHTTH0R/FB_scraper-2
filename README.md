# FB_scraper
Web scraper targets on facebook by selenium

## 前言

Facebook API 因2018年3月的個資事件而導致關閉，因此不再像以往一樣，可以很輕易地藉由此API獲得各FB社團上的資料。而導致很多前人做好的FB爬蟲工具(如:RFacebook)掛掉。

因此，前一段時間，我朋友林正鴻找上門來求救，於是我試著寫出藉由selenium實際開啟瀏覽器的方法，獲取FB社團的原始碼。再進行原始法的剖析，整理出要用的資訊，幫助他整理出一段時間內社團內各成員的活耀度。

接著，既然工具準備好了，為何不試著再次改寫，提供給一些公民科學家團隊的社團?如:特生中心的株式會社。協助他們可以像以前一樣很輕易地獲取社團成員提供的資料。
因此，我跑去問了一下他們之前Rfacebook是抓了哪些資訊下來，然後修改程式碼中的剖析原始碼、打包資料的部分，讓他們之後能方便使用。

總之就是這樣!

## 程式碼運作流程

## 使用方法
-----
Server:
  google cloud compute engine f1 micro (os: Ubuntu 18.04.1 LTS)
  
In shell run:

sudo apt-get update<br>


### install chrome and chromedriver
** Fail to let firefox work, so I use chrome **
ref:　https://zhuanlan.zhihu.com/p/36670753

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get -f install

mkdir driver && cd driver
wget https://chromedriver.storage.googleapis.com/2.38/chromedriver_linux64.zip
sudo apt-get install unzip
unzip chromedriver_linux64.zip



## python setting ##
sudo apt-get install python3-pip<br>
pip3 install virtualenv<br>
virtualenv -p python3 scraper_env<br>
git clone https://github.com/even311379/FB_scraper/
source scraper_env/bin/activate
pip install -r FB_scraper/requirements.txt

** The response time in f1 micro is so long, it will get timeout error **
** Or page crash!! Maybe I should use a more decent server to run this script! **

### edit crontab
crontab -e
(If this is your first time to run it, it will ask you to choose a default editor. And then )
add the following script in the end of that file
00 04 * * * /home/[YOUR USER NAME]/scraper_env/bin/python /home/[YOUR USER NAME]/FB_scraper/FB_spider_Scraper.py

## 延伸應用

