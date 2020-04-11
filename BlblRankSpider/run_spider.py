import sys
import os

from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists('logs'):
    os.makedirs('logs')

spider_name = 'bilibili_ranking'

execute_cmd = f'scrapy crawl {spider_name}'

print(execute_cmd)

execute(execute_cmd.split())
