# imdb-scrapy
I build this imdb-scrapy project to crawl some format imdb data basing on the scrapy framework, and the result report
will be sent to specific email automatically.


<center>
        <img src="pic/scrapy_logo.png" width=80%>
</center>

## 1. Background
This project is designed to statisfy the need for crawling imdb websites data automatically, such as the *Upcoming Releases*,
*Most Popular Movies*, *Custom Movies Urls List* and so on.

Websites:
1. [imdb-Upcoming Releases for United States](https://www.imdb.com/calendar/)
2. [imdb-Most Popular Movies](https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm)


## 2. Install
``` shell
cd /Path/To/imdb-scrapy
# start the watch serve
sh spy.sh
# auto deploy
crontab -e
# imdb scrapy
0 8 * * * cd /Path/To/imdbSpider;/bin/sh /Path/To/run.sh > /Path/To/imdbSpider/log/crontab-log.txt
```

## 3. Usage
There are three main requirements for the imdb-scrapy project：
1. Auto crawling the favourite or new imdb data at the specific date.
2. Auto crawling the imdb movie data on the imdb-url-list.
4. Send the report of result to the email of user.

### 3.1 Crawl the favourite and new imdb data
To satisfy the need of crawling favourite and new imdb data, the user only need to focus on the ```run.sh```.

Users need to modify the ```run.sh``` based on specified requirements.
``` shell
## run.sh ##
# execute the "new" and "favourite" crawling
python -m scrapy crawl new
python -m scrapy crawl favourite

# transport the report
scp data/new.csv data/favourite.csv Serve:Path

# Send the report to user by email
To be continued
```

```crontab``` is used to run the code at the specified time.
The example code sets the 8 o'clock as the specified time, which can be modified by ```crontab -e```。
```shell
# imdb-scrapy crontab profile
0 8 * * * cd /home/apps/wj/stream-media-pump/imdbSpider;/bin/sh /home/apps/wj/stream-media-pump/imdbSpider/run.sh > /home/apps/wj/stream-media-pump/imdbSpider/crontab-log.txt
```

### 3.2 Crawl the imdb-url-list data automatically
User only need to focus on using ```scp``` to update specific imdb-url-list file to user's server.

The imdb-url-list file format is as follows：
```text
https://www.imdb.com/title/tt3032476/
https://www.imdb.com/title/tt9663764/
https://www.imdb.com/title/tt9419884/
https://www.imdb.com/title/tt12412888/
https://www.imdb.com/title/tt7286456/
https://www.imdb.com/title/tt3794354/
https://www.imdb.com/title/tt4123430/
https://www.imdb.com/title/tt1695843/
```
scp上传指令
```
# scp上传代码
scp [path to imdb-url-list] user@server-ip:server-path-to-project

# 样例
scp /Users/Mars/imdb-scray/imdb-url-list mars@server-ip:server-path-to-project
```

### 3.3 Email
To be continued...


## 4. Scrapy Framework
<center>
        <img src="pic/spider_structure.png", width=80%>
</center>
There are three spiders，which are "list"，"favourite" and "new".


## TO DO LIST
- [x] Build The Basic Project (22.04.22 ~ 22.04.24)
- [x] Write The Project README (22.04.22 ~ 22.04.24)
- [x] Expand The Project (22.04.22 ~ 22.04.28)
- [x] Perfect The *imdb-scrapy*  Repositories (22.04.22 ~ 22.05.04)
- [ ] Format The Output Data Saving Path(22.05.04~)

## Conference
[1. Mars' Blog](https://wjmars98.github.io/)

[2. 初窥Scrapy](https://scrapy-chs.readthedocs.io/zh_CN/0.24/intro/overview.html)

[3. imdb官网](https://www.imdb.com/)
