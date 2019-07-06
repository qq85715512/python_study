# -*- coding: utf-8 -*-
import datetime
import jsonpath
import json
from crawler.items import *

game_info_url_base = 'http://odds.500.com/index_jczq_{0}.shtml'
game_ratio_info_url_base = 'http://odds.500.com/fenxi/yazhi-{0}.shtml'


# 通过jsonpath按列来解析需要的元素
def get_val_by_xpath(json_obj, xpath_exp):
    json_grp = jsonpath(json_obj, xpath_exp)
    l = []
    for i in json_grp:
        l.append(str(i))
    return l


def get_score(rst, is_home):
    if rst is None or rst == 'VS':
        return ''
    if is_home:
        return rst.split(':')[0]
    else:
        return rst.split(':')[1]


class ToScrapeSpiderXPath(scrapy.Spider):
    def __init__(self, start_dt=datetime.date(2019, 1, 1), end_dt=datetime.date(2019, 7, 2), *args, **kwargs):
        self.start_dt = start_dt
        self.end_dt = end_dt

    name = 'FBP_500'
    allowed_domains = ['500.com']

    def start_requests(self):
        date_step = datetime.timedelta(days=1)
        while self.start_dt <= self.end_dt:
            game_info_url = game_info_url_base.format(self.start_dt)
            yield scrapy.Request(game_info_url, callback=self.parse_game_info, meta={'start_dt': self.start_dt})
            self.start_dt = self.start_dt + date_step

    def parse_game_info(self, response):
        start_dt = response.meta['start_dt']
        for tr in response.css('tbody[id="main-body"]>tr'):
            game_info_item = GameInfoItem()
            game_info_item['game_id'] = tr.css('td')[0].css('input::attr(value)').get()
            game_info_item['game_dt'] = start_dt
            game_info_item['ser_num'] = tr.css('td')[0].css(':last-child::text')[2:]
            game_info_item['game_tm'] = tr.css('td')[3].css('::text').get()[6:]
            game_info_item['league_simple_name'] = tr.css('td')[1].css(':last-child::text').get()
            game_info_item['home_team_name'] = tr.css('td')[4].css(':last-child::text').get()
            game_info_item['guest_team_name'] = tr.css('td')[6].css(':last-child::text').get()
            game_info_item['game_rst'] = tr.css('td')[5].css(':last-child::text').get()
            game_info_item['home_score'] = get_score(game_info_item['game_rst'], 1)
            game_info_item['guest_score'] = get_score(game_info_item['game_rst'], 0)
            game_info_item['home_rank'] = ''
            game_info_item['guest_rank'] = ''
            game_info_item['standard_home'] = tr.css('td')[11].css('::text').get()
            game_info_item['standard'] = tr.css('td')[12].css('::text').get()
            game_info_item['standard_guest'] = tr.css('td')[13].css('::text').get()
            game_info_item['award'] = ''
            if game_info_item['standardHome'] is not None:
                game_info_item['award'] = ' '.join([game_info_item['standardHome'], game_info_item['standard'], game_info_item['standardGuest']])
            yield game_info_item

            game_ratio_info_url = game_ratio_info_url_base.format(game_info_item['id'])
            yield scrapy.Request(game_ratio_info_url, callback=self.parse,
                                 meta={'game_id': game_info_item['game_id'],
                                       'ser_num': game_info_item['ser_num'],
                                       'game_dt': game_info_item['game_dt']})

    def parse(self, response):
        game_id = response.meta['game_id']
        game_dt = response.meta['game_dt']
        ser_num = response.meta['ser_num']
        for tr in response.css('tr[tr[xls="row"]')[:10]:
            company = tr.css('td')[1].css('::text').get()
            rati = tr.css('table')[1]
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
            game_ratio_info_item['company'] = ''
            yield game_ratio_info_item


def main():
    pass


if __name__ == '__main__':
    main()
