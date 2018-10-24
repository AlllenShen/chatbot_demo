import urllib.request
import json
import re
import urllib.error
import time
import datetime
from bs4 import BeautifulSoup
import urllib.error
import random

from spider.models import get_session, PM, Weather


class Crawler:
    def __init__(self):
        headers = ("User-Agent",
                   "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36")
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
        with open('city.json', 'r', encoding='utf-8') as f:
            self.city = json.load(f)
        self.session = get_session()

    @staticmethod
    def get_PM25(city):
        try:
            url = "http://pm25.in/" + city
            # print("城市：{}".format(city))
            data = urllib.request.urlopen(url).read().decode("utf-8")

            data_time = '<div class="live_data_time">\s{1,}<p>数据更新时间：(.*?)</p>' # .encode('utf-8')
            data_time = re.compile(data_time, re.S).findall(data)
            data_time = datetime.datetime.strptime(data_time[0], '%Y-%m-%d %H:%M:%S')
            # print(data_time)

            data_pm25 = '<div class="span1">\s{1,}<div class="value">\n\s{1,}(.*?)\s{1,}</div>' # .encode('utf-8')
            pm25list = re.compile(data_pm25, re.S).findall(data)

            data_o3 = '<div class="span1">\s{1,}<div class ="value">\n\s{1,}(.*?)\s{1,}</div>' # .encode('utf-8')
            o3list = re.compile(data_o3, re.S).findall(data)

            pm25list.append(o3list[0])
            # print("AQI指数，PM2.5，PM10，CO，NO2，SO2，O3：（单位：μg/m3，CO为mg/m3）")
            # print(pm25list)

            # 获得其他三项当前天气信息
            url = 'https://www.tianqi.com/{}/'.format(city)
            data = urllib.request.urlopen(url).read().decode("utf-8")
            soup = BeautifulSoup(data, 'html.parser')
            li_shidu = soup.find('dd', attrs={'class': 'shidu'}).find_all('b')
            pm_list = {
                "AQI": pm25list[0] + "μg/m3",
                "PM25": pm25list[1] + "μg/m3",
                "PM10": pm25list[2] + "μg/m3",
                "CO": pm25list[3] + "mg/m3",
                "NO2": pm25list[4] + "μg/m3",
                "SO2": pm25list[5] + "μg/m3",
                "O3": pm25list[6] + "μg/m3",
                "humidity": li_shidu[0].string.split("：")[1],
                "wind": li_shidu[1].string.split("：")[1].split()[0],
                "wind_level": li_shidu[1].string.split("：")[1].split()[1],
                "ultra_ray": li_shidu[2].string.split("：")[1],
                "date": data_time
            }
            # print(pm_list)
            return pm_list
        except urllib.error.URLError as e:
            print("出现URL ERROR！一分钟后重试……")
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
            time.sleep(60)
            # get_PM25(city)
        # except Exception as e:
        #     print(e)
        #     time.sleep(5)

    @staticmethod
    def get_Weather(city):
        try:
            weatherlist = []
            url = 'https://www.tianqi.com/{}/'.format(city)
            data = urllib.request.urlopen(url).read().decode("utf-8")
            soup = BeautifulSoup(data, 'html.parser')

            li_date = soup.find('ul', attrs={'class': 'week'}).find_all('li')
            li_weather = soup.find('ul', attrs={'class': 'txt txt2'}).find_all('li')
            li_temp = soup.find('div', attrs={'class': 'zxt_shuju'}).find('ul').find_all('li')

            for i in range(len(li_weather)):
                slot = [
                    {
                        'date': Crawler.handle_time_str(li_date[i].find('b').string),
                        'week': li_date[i].find('span').string,
                        'weather': li_weather[i].string,
                        'high_temp': int(li_temp[i].find('span').string),
                        'low_temp': int(li_temp[i].find('b').string),
                    }
                ]
                weatherlist.append(slot)
            return weatherlist

        except urllib.error.URLError as e:
            print("出现URL ERROR！一分钟后重试……")
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
            time.sleep(60)
            # get_Weather(city)
        # except Exception as e:
        #     print("Exception：" + str(e))
        #     # time.sleep(10)

    @staticmethod
    def handle_time_str(time_str):
        """
        x月x日 -> datetime
        :param time_str:
        :return: datetime.datetime
        """
        time_str = time_str.replace('月', '-').replace('日', '')
        return datetime.datetime.strptime(time_str, '%m-%d').replace(datetime.datetime.now().year)

    def update(self, limit=None):
        """
        更新数据
        :return:
        """
        limit = len(self.city) if not limit or limit > len(self.city) else limit
        for i in self.city[:limit]:
            print('爬取: {}'.format(i['name']))
            res = self.get_PM25(i['pinyin'].lower())
            self.insert('pm', i, res)
            res = self.get_Weather(i['pinyin'].lower())
            for day in res:
                self.insert('weather', i, day[0])

            rest_time = random.randint(2, 4)
            print("rest {}s...".format(rest_time))
            time.sleep(rest_time)

    def insert(self, data_type, city, data):
        """
        插入PM2.5、weather数据
        data字段和数据库字段重合，插入较为简便
        :param data_type: insert类型 'pm' 'weather'
        :param city: city字典
        :param data:
        :return:
        """
        if data_type == 'pm':
            new = PM()
            model = PM
        elif data_type == 'weather':
            new = Weather()
            model = Weather
        else:
            raise ValueError('invalid param {}'.format(data_type))
        # 查重
        if self.session.query(model).filter_by(date=data['date'], city=city['name']).first():
            print('重复数据 {} - {}: {}'.format(city['name'], data['date'].strftime("%Y-%m-%d"), data))
            return

        new.city = city['name']
        for i in data:
            new.__setattr__(i, data[i])
        self.session.add(new)
        self.session.commit()

    def test(self):
        self.update(10)


if __name__ == '__main__':
    crawler = Crawler()
    crawler.test()