import sys
import os

from scrapy.cmdline import execute

sys.path.append(os.path.dirname(__file__))
print(os.path.dirname(__file__))

# execute(['scrapy', 'crawl', 'page_user'])
execute(['scrapy', 'crawl', 'page_video'])
