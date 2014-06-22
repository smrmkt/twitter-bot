# -*- coding: utf-8 -*-

import sys
import os.path
import json
import urllib2

script_path = os.path.dirname(__file__)
script_path = script_path if len(script_path) else '.'
sys.path.append(script_path + '/../lib')
sys.path.append(script_path + '/../lib/model')

from src.lib.model.account import Account

class NoconocoWeather:
    def __init__(self, location):
        self.__account = Account('noconoco-weather')
        self.__location = self.encode_location(location)

    def get_info(self):
        return self.__account.info()

    def post(self, message):
        self.__account.post(message)

    def get_weather_message(self):
        info = self.get_weather_info()
        message = (info['location']['city']).encode('utf-8') + 'の天気をお知らせするしー\n'
        for i in range(0, 2):
            date = (info['forecasts'][i]['dateLabel']).encode('utf-8')
            weather = (info['forecasts'][i]['telop']).encode('utf-8')
            temp = info['forecasts'][i]['temperature']['max']
            if temp is not None:
                temp = (temp['celsius']).encode('utf-8') + '度だ'
            else:
                temp = 'よくわかんない'
            message = message + date + 'の天気は「' + weather + '」で最高気温は' + temp + 'し\n'
        return message + 'そんなことより早くあたしを撫でればいいし'

    def get_weather_info(self):
        # yokohama
        url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=%s' % self.__location
        res = urllib2.urlopen(url)
        return json.loads(res.read())

    def encode_location(self, location):
        locations = {
            '与那国島' : '474020',
            '石垣島' : '474010',
            '宮古島' : '473000',
            '南大東' : '472000',
            '久米島' : '471030',
            '名護' : '471020',
            '那覇' : '471010',
            '名瀬' : '460040',
            '種子島' : '460030',
            '鹿屋' : '460020',
            '鹿児島' : '460010',
            '高千穂' : '450040',
            '都城' : '450030',
            '延岡' : '450020',
            '宮崎' : '450010',
            '佐伯' : '440040',
            '日田' : '440030',
            '中津' : '440020',
            '大分' : '440010',
            '人吉' : '430040',
            '牛深' : '430030',
            '阿蘇乙姫' : '430020',
            '熊本' : '430010',
            '福江' : '420040',
            '厳原' : '420030',
            '佐世保' : '420020',
            '長崎' : '420010',
            '伊万里' : '410020',
            '佐賀' : '410010',
            '久留米' : '400040',
            '飯塚' : '400030',
            '八幡' : '400020',
            '福岡' : '400010',
            '清水' : '390030',
            '室戸岬' : '390020',
            '高知' : '390010',
            '宇和島' : '380030',
            '新居浜' : '380020',
            '松山' : '380010',
            '高松' : '370000',
            '日和佐' : '360020',
            '徳島' : '360010',
            '萩' : '350040',
            '柳井' : '350030',
            '山口' : '350020',
            '下関' : '350010',
            '庄原' : '340020',
            '広島' : '340010',
            '津山' : '330020',
            '岡山' : '330010',
            '西郷' : '320030',
            '浜田' : '320020',
            '松江' : '320010',
            '米子' : '310020',
            '鳥取' : '310010',
            '潮岬' : '300020',
            '和歌山' : '300010',
            '風屋' : '290020',
            '奈良' : '290010',
            '豊岡' : '280020',
            '神戸' : '280010',
            '大阪' : '270000',
            '舞鶴' : '260020',
            '京都' : '260010',
            '彦根' : '250020',
            '大津' : '250010',
            '尾鷲' : '240020',
            '津' : '240010',
            '豊橋' : '230020',
            '名古屋' : '230010',
            '浜松' : '220040',
            '三島' : '220030',
            '網代' : '220020',
            '静岡' : '220010',
            '高山' : '210020',
            '岐阜' : '210010',
            '飯田' : '200030',
            '松本' : '200020',
            '長野' : '200010',
            '河口湖' : '190020',
            '甲府' : '190010',
            '敦賀' : '180020',
            '福井' : '180010',
            '輪島' : '170020',
            '金沢' : '170010',
            '伏木' : '160020',
            '富山' : '160010',
            '相川' : '150040',
            '高田' : '150030',
            '長岡' : '150020',
            '新潟' : '150010',
            '小田原' : '140020',
            '横浜' : '140010',
            '父島' : '130040',
            '八丈島' : '130030',
            '大島' : '130020',
            '東京' : '130010',
            '館山' : '120030',
            '銚子' : '120020',
            '千葉' : '120010',
            '秩父' : '110030',
            '熊谷' : '110020',
            'さいたま' : '110010',
            'みなかみ' : '100020',
            '前橋' : '100010',
            '大田原' : '90020',
            '宇都宮' : '90010',
            '土浦' : '80020',
            '水戸' : '80010',
            '若松' : '70030',
            '小名浜' : '70020',
            '福島' : '70010',
            '新庄' : '60040',
            '酒田' : '60030',
            '米沢' : '60020',
            '山形' : '60010',
            '横手' : '50020',
            '秋田' : '50010',
            '白石' : '40020',
            '仙台' : '40010',
            '大船渡' : '30030',
            '宮古' : '30020',
            '盛岡' : '30010',
            '八戸' : '20030',
            'むつ' : '20020',
            '青森' : '20010',
            '江差' : '17020',
            '函館' : '17010',
            '倶知安' : '16030',
            '岩見沢' : '16020',
            '札幌' : '16010',
            '浦河' : '15020',
            '室蘭' : '15010',
            '帯広' : '14030',
            '釧路' : '14020',
            '根室' : '14010',
            '紋別' : '13030',
            '北見' : '13020',
            '網走' : '13010',
            '留萌' : '12020',
            '旭川' : '12010',
            '稚内' : '11000'
        }
        return locations[location]