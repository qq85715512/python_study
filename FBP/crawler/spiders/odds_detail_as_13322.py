# -*- coding: utf-8 -*-
import datetime
import jsonpath
import json
from crawler.items import *

game_info_url_base = 'https://live.13322.com/lotteryScore/list?getExtra=2&lang=zh&date={0}'
# 有效公司编号
# 3  皇冠
# 31 Wellbet
# 44 ISN
# 51 澳门
#
game_ratio_info_url_base = 'https://odds.13322.com/toDetailNew?companys=3&thirdmhId={0}&matchId={0}&flag=2&dateTime={1}'


# 通过jsonpath按列来解析需要的元素
def get_val_by_xpath(json_obj, xpath_exp):
    json_grp = jsonpath(json_obj, xpath_exp)
    l = []
    for i in json_grp:
        l.append(str(i))
    return l


class ToScrapeSpiderXPath(scrapy.Spider):
    def __init__(self, start_dt=datetime.date(2019, 1, 1), end_dt=datetime.date(2019, 7, 2), *args, **kwargs):
        self.start_dt = start_dt
        self.end_dt = end_dt

    name = 'FBP'
    allowed_domains = ['13322.com']

    def start_requests(self):
        date_step = datetime.timedelta(days=1)
        while self.start_dt <= self.end_dt:
            game_info_url = game_info_url_base.format(self.start_dt)
            yield scrapy.Request(game_info_url, callback=self.parse_game_info, meta={'start_dt': self.start_dt})
            self.start_dt = self.start_dt + date_step

    def parse_game_info(self, response):
        start_dt = response.meta['start_dt']
        json_str = json.loads(response.body)
        for match in json_str['matches']:
            game_info_item = GameInfoItem()
            game_info_item['game_id'] = match['id']
            game_info_item['game_dt'] = start_dt
            game_info_item['ser_num'] = match['serNum'][2:]
            game_info_item['game_tm'] = match['time'][11:]
            game_info_item['league_simple_name'] = match['leagueSimpName']
            game_info_item['home_team_name'] = match['hoTeamName']
            game_info_item['guest_team_name'] = match['guTeamName']
            game_info_item['game_rst'] = '-'.join([str(match['hoScore']), str(match['guScore'])])
            game_info_item['home_score'] = match['hoScore']
            game_info_item['guest_score'] = match['guScore']
            game_info_item['home_rank'] = match['hoRank']
            game_info_item['guest_rank'] = match['guRank']
            game_info_item['standard_home'] = match['standardHome']
            game_info_item['standard'] = match['standard']
            game_info_item['standard_guest'] = match['standardGuest']
            game_info_item['award'] = ''
            if match['standardHome'] is not None:
                game_info_item['award'] = ' '.join([match['standardHome'], match['standard'], match['standardGuest']])
            yield game_info_item

            game_ratio_info_url = game_ratio_info_url_base.format(match['id'], start_dt)
            yield scrapy.Request(game_ratio_info_url, callback=self.parse,
                                 meta={'game_id': game_info_item['game_id'],
                                       'ser_num': game_info_item['ser_num'],
                                       'game_dt': game_info_item['game_dt']})

    def parse(self, response):
        game_id = response.meta['game_id']
        game_dt = response.meta['game_dt']
        ser_num = response.meta['ser_num']
        for tr in response.css('tbody.tb_bar>tr[style="display: "]'):
            ratio = tr.css('td::text').getall()
            if ratio[-1].strip() not in ('早', '初盘', '即') or ratio[2].strip() == '封':
                continue
            game_ratio_info_item = GameRatioInfoItem()
            home_ratio = ratio[0].strip()
            position_ratio = ratio[1].strip()
            guest_ratio = ratio[2].strip()
            position_tm = ratio[3].strip()
            status = ratio[4].strip()
            game_ratio_info_item['game_id'] = game_id
            game_ratio_info_item['game_dt'] = game_dt
            game_ratio_info_item['ser_num'] = ser_num
            game_ratio_info_item['position_tm'] = position_tm
            game_ratio_info_item['home_ratio'] = home_ratio
            game_ratio_info_item['position_ratio'] = position_ratio
            game_ratio_info_item['guest_ratio'] = guest_ratio
            game_ratio_info_item['status'] = status
            game_ratio_info_item['company'] = '皇冠'
            yield game_ratio_info_item


def main():
    pass


if __name__ == '__main__':
    main()
