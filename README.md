# Twitter-bot
[![Build Status](https://travis-ci.org/smrmkt/twitter-bot.svg?branch=feature%2Fnoco-weather-test)](https://travis-ci.org/smrmkt/twitter-bot)
[![Coverage Status](https://coveralls.io/repos/smrmkt/twitter-bot/badge.png?branch=master)](https://coveralls.io/r/smrmkt/twitter-bot?branch=master)

## Account
### about
Noconoco bot: [https://twitter.com/noconoco_bot](https://twitter.com/noconoco_bot)

### start command
```
python bin/run_noconoco_stream.py
```

## Bot functions
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

### Japanese horse racing information

#### Description
- bot replys to a mention includes "出走予定"
- bot tells starters of a specific horse owner in this week
- horse owner name must be specified in starting bot (default is "社台レースホース")

#### Example
```
@noconoco_bot 出走予定を教えて
```

```
@hoge よくわかんないけど，01月10日のレースに
ディープインパクトが出走するみたいだしー (20:01:15)
```

### Japanese recipe information

#### Description
- bot replys to a mention includes "献立"
- recipe information is taken from []Rauten recipe](https://webservice.rakuten.co.jp/api/recipecategoryranking/)

#### Example
```
@noconoco_bot 今日の献立は何がいい？
```

```
@hoge 今日のおすすめの献立は「 ふっくらやわらかになる！ブリの照り焼き 」だしー．約30分でできるから，とっても簡単だしー． recipe.rakuten.co.jp/recipe/1440002… (12:22:57)
```

### Chat in Japanese

#### Description
- bot has a chat with you
- chat feature is constructed from NTT Docomo's [chat dialogue API](https://dev.smt.docomo.ne.jp/?p=docs.api.page&api_name=dialogue&p_name=api_reference)
