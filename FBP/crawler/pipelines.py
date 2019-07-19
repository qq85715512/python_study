import os
import csv
from crawler.items import *


class GameInfoPipeline(object):
    def __init__(self):
        # csv文件的位置,无需事先创建
        store_file = os.path.dirname(__file__) + '/output/game_info_tot.csv'
        # 打开(创建)文件
        self.file = open(store_file, 'a', encoding='utf8', newline='')
        # csv写法
        self.writer = csv.writer(self.file)
        self.increment_writer.writerow(('game_id', 'game_dt', 'ser_num', 'game_tm', 'league_simple_name', 'home_team_name', 'guest_team_name', 'game_rst', 'home_score', 'guest_score', 'home_rank', 'guest_rank', 'standard_home', 'standard', 'standard_guest', 'award'))

    def process_item(self, item, spider):
        print(item)
        # 判断字段值不为空再写入文件
        if isinstance(item, GameInfoItem):
            self.writer.writerow(item.values())
            return item
        elif isinstance(item, GameRatioInfoItem):
            return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()


class GameInfoPipelineIncrement(object):
    def __init__(self):
        # csv文件的位置,无需事先创建
        store_increment_file = os.path.dirname(__file__) + '/output/game_info_increment.csv'
        # 打开(创建)文件
        self.increment_file = open(store_increment_file, 'w', encoding='utf8', newline='')
        # csv写法
        self.increment_writer = csv.writer(self.increment_file)
        self.increment_writer.writerow(('game_id', 'game_dt', 'ser_num', 'game_tm', 'league_simple_name', 'home_team_name', 'guest_team_name', 'game_rst', 'home_score', 'guest_score', 'home_rank', 'guest_rank', 'standard_home', 'standard', 'standard_guest', 'award'))

    def process_item(self, item, spider):
        # 判断字段值不为空再写入文件
        if isinstance(item, GameInfoItem):
            self.increment_writer.writerow(item.values())
            return item
        elif isinstance(item, GameRatioInfoItem):
            return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.increment_file.close()


class GameInfoPipelineLTT(object):
    def __init__(self):
        # csv文件的位置,无需事先创建
        store_ltt_file = os.path.dirname(__file__) + '/output/game_info_target.csv'
        # 打开(创建)文件
        self.ltt_file = open(store_ltt_file, 'w', encoding='utf8', newline='')
        # csv写法
        self.ltt_writer = csv.writer(self.ltt_file)
        # self.ltt_writer.writerow(['比赛日期', '比赛序号', '比赛时间', '赛事类型', '主队名称', '客队名称', '比分赛果', '胜平负奖金'])

    def process_item(self, item, spider):
        # 判断字段值不为空再写入文件
        if isinstance(item, GameInfoItem):
            self.ltt_writer.writerow((item['game_dt'], item['ser_num'], item['game_tm'], item['league_simple_name'], item['home_team_name'], item['guest_team_name'], item['game_rst'], item['award']))
            return item
        elif isinstance(item, GameRatioInfoItem):
            return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.ltt_file.close()


class GameRatioInfoPipeline(object):
    def __init__(self):
        store_file = os.path.dirname(__file__) + '/output/game_ratio_info_tot.csv'
        # 打开(创建)文件
        self.file = open(store_file, 'a', encoding='utf8', newline='')
        # csv写法
        self.writer = csv.writer(self.file)
        self.increment_writer.writerow(('game_id', 'game_dt', 'ser_num', 'position_tm', 'home_ratio', 'position_ratio', 'guest_ratio', 'status', 'company'))

    def process_item(self, item, spider):
        if isinstance(item, GameInfoItem):
            return item
        elif isinstance(item, GameRatioInfoItem):
            self.writer.writerow(item.values())
            return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()


class GameRatioInfoPipelineIncrement(object):
    def __init__(self):
        store_increment_file = os.path.dirname(__file__) + '/output/game_ratio_info_increment.csv'
        # 打开(创建)文件
        self.increment_file = open(store_increment_file, 'w', encoding='utf8', newline='')
        # csv写法
        self.increment_writer = csv.writer(self.increment_file)
        self.increment_writer.writerow(('game_id', 'game_dt', 'ser_num', 'position_tm', 'home_ratio', 'position_ratio', 'guest_ratio', 'status', 'company'))

    def process_item(self, item, spider):
        if isinstance(item, GameInfoItem):
            return item
        elif isinstance(item, GameRatioInfoItem):
            self.increment_writer.writerow(item.values())
            return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.increment_file.close()


class GameRatioInfoPipelineLTT(object):
    def __init__(self):
        store_ltt_file = os.path.dirname(__file__) + '/output/game_ratio_info_target.csv'
        # 打开(创建)文件
        self.ltt_file = open(store_ltt_file, 'w', encoding='utf8', newline='')
        # csv写法
        self.ltt_writer = csv.writer(self.ltt_file)
        # self.ltt_writer.writerow(['比赛日期', '比赛序号', '盘口时间', '赔率盘口', '主水', '客水', '博彩公司名称'])

    def process_item(self, item, spider):
        if isinstance(item, GameInfoItem):
            return item
        elif isinstance(item, GameRatioInfoItem):
            self.ltt_writer.writerow((item['game_dt'], item['ser_num'], item['position_tm'], item['position_ratio'], item['home_ratio'], item['guest_ratio'], item['company']))
            return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.ltt_file.close()
