#!/bin/bash
#scrapy crawl alexandalexa_burberry -o log/alexandalexa_burberry.json --logfile log/alexandalexa_burberry.log
list="alexandalexa_burberry alexandalexa_gender alexandalexa"
#list="alexandalexa"
rm -rf log
mkdir -p log
for name in $list ; do 
    echo $name
    mkdir -p log/$name
    scrapy crawl ${name} -o log/${name}/data.csv --logfile log/${name}/data.log
done
#scrapy crawl alexandalexa_burberry -o log/alexandalexa_burberry.csv --logfile log/alexandalexa_burberry.log
#scrapy crawl alexandalexa_gender -o log/alexandalexa_gender.csv --logfile log/alexandalexa_gender.log
