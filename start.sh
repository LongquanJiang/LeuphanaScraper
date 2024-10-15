# path to venv
# source ~/venv/bin/activate
nohup scrapy crawl news -L INFO > spider.log 2>&1 &
echo crawler started