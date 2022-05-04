# execute the spiders to fetch new and favourite data
python -m scrapy crawl new
python -m scrapy crawl favourite

# transport the data to server
scp data/new.csv data/favourite.csv server_path

# send the report
python3.8 bin/get_report.py -r "favourite-new"