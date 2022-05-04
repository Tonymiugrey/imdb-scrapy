#!/bin/sh
while true
do
{
  cd /path/to/imdbSpider
  # Using md5 to check whether the imdb-url-list changed.
  char=$(md5sum -c conf/list/imdb-url-list.md5 2>/dev/null|grep "OK"|wc -l)

  if [ $char -eq 1 ];then
    echo "yes"
  else
    echo "begin output list csv"

    # Fetch the new list data
    python -m scrapy crawl list

    # Path of the server which store the report.
    scp data/list.csv server:path
    python bin/get_report.py -r "list"

    # Update the imdb-url-list md5
    md5sum conf/list/imdb-url-list > conf/list/imdb-url-list.md5
  fi
  sleep 10
}
done
