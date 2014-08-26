# Twitter-bot
[![Build Status](https://travis-ci.org/smrmkt/twitter-bot.svg?branch=feature%2Fnoco-weather-test)](https://travis-ci.org/smrmkt/twitter-bot)
[![Coverage Status](https://coveralls.io/repos/smrmkt/twitter-bot/badge.png?branch=master)](https://coveralls.io/r/smrmkt/twitter-bot?branch=master)

## Account
Noconoco bot: [https://twitter.com/noconoco_bot](https://twitter.com/noconoco_bot)

### Japanese weather information
#### Description
- bot replys to a mention with majour city name in Japan
- supported cities are those in [livedoor weather API location list](http://weather.livedoor.com/forecast/rss/primary_area.xml)

#### Example
```
@noconoco_bot さいたま
```
```
@hoge さいたまの天気をお知らせするしー
今日の天気は「曇り」で最高気温はよくわかんないし
明日の天気は「曇り」で最高気温は27度だし
そんなことより早くあたしを撫でればいいし (22:30:00)
```

### Japanese stock information
#### Description
- bot replys to a mention with company name or company code in Tokyo Stock Exchange
- stock information is taken from [Yahoo! Japan finance](http://finance.yahoo.co.jp/)

#### Example 1: company name
```
@noconoco_bot ヤクルト
```
```
@hoge (株)ヤクルトの株価は5340だしー
前日終値は5320で今日の始値は5370，高値は5370，安値は5310だしー
そんなことより早くあたしを撫でればいいし (20:01:15)
```
#### Example 2: company code
```
@noconoco_bot 2267
```
```
@hoge (株)ヤクルト本社(2267)の株価は5340だしー
前日終値は5320で今日の始値は5370，高値は5370，安値は5310だしー
そんなことより早くあたしを撫でればいいし (20:01:15)
```
