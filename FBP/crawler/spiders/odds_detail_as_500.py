# -*- coding: utf-8 -*-
import datetime
from crawler.items import GameInfoItem, GameRatioInfoItem
import scrapy
import re

game_info_url_base = 'http://odds.500.com/index_jczq_{0}.shtml'
game_ratio_info_url_base = 'http://odds.500.com/fenxi/yazhi-{0}.shtml'

weekday_map = {'周一': 0, '周二': 1, '周三': 2, '周四': 3, '周五': 4, '周六': 5, '周日': 6}


def get_score(rst, is_home):
    if rst is None or rst == 'VS':
        return ''
    if is_home:
        return rst.split(':')[0]
    else:
        return rst.split(':')[1]


class ToScrapeSpiderXPath(scrapy.Spider):
    def __init__(self, start_dt=None, end_dt=None, *args, **kwargs):
        # self.headers = {
        #     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #     'Accept-Encoding': 'gzip, deflate',
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        # }
        if start_dt is None and end_dt is None:
            start_dt = datetime.date.today()
            end_dt = datetime.date.today()
        else:
            start_dt = datetime.datetime.strptime(start_dt, '%Y-%M-%d').date()
            end_dt = datetime.datetime.strptime(end_dt, '%Y-%M-%d').date()
        self.start_dt = start_dt
        self.end_dt = end_dt

    name = 'FBP_500'
    allowed_domains = ['500.com']

    def start_requests(self):
        date_step = datetime.timedelta(days=1)
        while self.start_dt >= self.end_dt:
            game_info_url = game_info_url_base.format(self.start_dt)
            yield scrapy.Request(game_info_url, callback=self.parse_game_info, meta={'start_dt': self.start_dt})
            self.start_dt = self.start_dt - date_step

    def parse_game_info(self, response):
        print(response)
        start_dt = response.meta['start_dt']
        for tr in response.css('tbody[id="main-tbody"]>tr[data-cid="3"]'):
            weekday = tr.css('td')[0].css(':last-child::text').get()[:2]
            if start_dt.weekday() != weekday_map[weekday]:
                continue
            game_info_item = GameInfoItem()
            game_info_item['game_id'] = tr.css('td')[0].css('input::attr(value)').get()
            game_info_item['game_dt'] = start_dt
            game_info_item['ser_num'] = tr.css('td')[0].css(':last-child::text').get()[2:]
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
            if game_info_item['standard_home'] is not None:
                game_info_item['award'] = ' '.join([game_info_item['standard_home'], game_info_item['standard'], game_info_item['standard_guest']])
            yield game_info_item

            game_ratio_info_url = game_ratio_info_url_base.format(game_info_item['game_id'])
            yield scrapy.Request(game_ratio_info_url, callback=self.parse,
                                 meta={'game_id': game_info_item['game_id'],
                                       'ser_num': game_info_item['ser_num'],
                                       'game_dt': game_info_item['game_dt']})

    def parse(self, response):
        game_id = response.meta['game_id']
        game_dt = response.meta['game_dt']
        ser_num = response.meta['ser_num']
        for tr in response.css('tr[xls="row"]'):
            tds = tr.xpath('descendant-or-self::td')
            company = tds[1].css('::text').get()
            # if company.lower().strip() not in ('威廉希尔','澳门','皇冠','易胜博','伟德'):
            if company.lower().strip() not in ('威廉希尔', '澳门', 'bet365', '皇冠', '易胜博', 'interwetten', '10bet', '伟德'):
            # if company.lower().strip() not in ('bet365','interwetten','10bet' ):
                continue
            ji_game_year = game_dt.year
            chu_game_year = game_dt.year
            ji_position_tm = tds[7].css('::text').get()
            chu_position_tm = tds[12].css('::text').get()
            if ji_position_tm[:5] == '01-01' and chu_position_ratio[:5] in ('12-30', '12-31'):
                chu_game_year = chu_game_year - 1

            ji = GameRatioInfoItem()
            ji_home_ratio = re.search('[.0-9]+', tds[3].css('::text').get()).group(0)
            ji_position_ratio = tds[4].css('::text').get().replace(' |降|升', '')
            ji_guest_ratio = re.search('[.0-9]+', tds[5].css('::text').get()).group(0)
            ji_position_tm = str(ji_game_year) + '-' + ji_position_tm
            ji['game_id'] = game_id
            ji['game_dt'] = game_dt
            ji['ser_num'] = ser_num
            ji['position_tm'] = ji_position_tm
            ji['home_ratio'] = ji_home_ratio
            ji['position_ratio'] = ji_position_ratio
            ji['guest_ratio'] = ji_guest_ratio
            ji['status'] = '即'
            ji['company'] = company
            yield ji

            chu = GameRatioInfoItem()
            chu_home_ratio = re.search('[.0-9]+', tds[9].css('::text').get()).group(0)
            chu_position_ratio = tds[10].css('::text').get().replace(' |降|升', '')
            chu_guest_ratio = re.search('[.0-9]+', tds[11].css('::text').get()).group(0)
            chu_position_tm = str(chu_game_year) + '-' + chu_position_tm
            chu['game_id'] = game_id
            chu['game_dt'] = game_dt
            chu['ser_num'] = ser_num
            chu['position_tm'] = chu_position_tm
            chu['home_ratio'] = chu_home_ratio
            chu['position_ratio'] = chu_position_ratio
            chu['guest_ratio'] = chu_guest_ratio
            chu['status'] = '初'
            chu['company'] = company
            yield chu
