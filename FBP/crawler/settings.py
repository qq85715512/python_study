# -*- coding: utf-8 -*-

# Scrapy settings for test_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'FBP'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

ITEM_PIPELINES = {
    'crawler.pipelines.GameInfoPipeline': 10,
    # 'crawler.pipelines.GameInfoPipelineIncrement': 20,
    # 'crawler.pipelines.GameInfoPipelineLTT': 30,
    'crawler.pipelines.GameRatioInfoPipeline': 40,
    # 'crawler.pipelines.GameRatioInfoPipelineIncrement': 50,
    # 'crawler.pipelines.GameRatioInfoPipelineLTT': 60,
}

LOG_LEVEL = 'ERROR'
LOG_FILE = 'log/log.txt'
# FEED_URI = 'D:\\python_study\\qtw.csv'
# FEED_FORMAT = 'csv'
# FEED_EXPORTERS = {
#     'csv': 'crawler.itemcsvexporter.GameInfoExporter',
#     'csv': 'crawler.itemcsvexporter.GameRatioInfoExporter'
# }
# GAME_INFO_FIELDS_TO_EXPORT = [
#     'game_id',
#     'game_dt',
#     'ser_num',
#     'game_tm',
#     'league_simple_name',
#     'home_team_name',
#     'guest_team_name',
#     'game_rst',
#     'award',
#     'home_score',
#     'guest_score',
#     'home_rank',
#     'guest_rank',
#     'standard_home',
#     'standard',
#     'standard_guest',
#     'company'
# ]
#
# GAME_RATIO_INFO_FIELDS_TO_EXPORT = [
#     'game_id',
#     'home_ratio',
#     'position_ratio',
#     'guest_ratio',
#     'position_tm',
#     'status'
# ]
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'test_scrapy (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'test_scrapy.middlewares.TestScrapySpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'test_scrapy.middlewares.TestScrapyDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'test_scrapy.pipelines.TestScrapyPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
