from urllib.error import URLError
from urllib.request import urlopen

import gzip
import zlib
from jsonpath import jsonpath
from bs4 import BeautifulSoup
import time
import logging
import requests

import pandas as pd
import json
import datetime


# 通过指定的字符集对页面进行解码(不是每个网站都将字符集设置为utf-8)
def decode_page(page_bytes, charsets=('utf-8',)):
    page_html = None
    for charset in charsets:
        try:
            page_html = page_bytes.decode(charset)
            break
        except UnicodeDecodeError as e:
            pass
            logging.error('Decode:', e)
    return page_html


# 获取页面的HTML代码(通过递归实现指定次数的重试操作)
def get_page_html(seed_url, *, retry_times=3, charsets=('utf-8',)):
    page_html = None
    try:
        repsonse = urlopen(seed_url)
        html = repsonse.read()
        encoding = repsonse.info().get('Content-Encoding')
        if encoding == 'gzip':
            html = zlib.decompress(html, 16+zlib.MAX_WBITS)
        elif encoding == 'deflate':
            try:
                html = zlib.decompress(html, -zlib.MAX_WBITS)
            except zlib.error:
                html = zlib.compress(html)
        page_html = decode_page(html, charsets)
        # page_html = requests.get(seed_url)
    except URLError as e:
        logging.error('URL:', e)
        if retry_times > 0:
            return get_page_html(seed_url, retry_times=retry_times - 1,
                                 charsets=charsets)
    except TimeoutError as e:
        logging.error('URL:', e)
        if retry_times > 0:
            return get_page_html(seed_url, retry_times=retry_times - 1,
                                 charsets=charsets)
    return page_html


# 解析json，获取比赛信息
def get_today_game_info_new(json_str, start_dt):
    if not len(json_str['matches']):
        return None
    ser_num = get_val_by_xpath(json_str, '$.matches[*].serNum')
    # 只保留编号
    ser_num = [x[2:] for x in ser_num]
    # 联赛
    league_simple_name = get_val_by_xpath(json_str, '$.matches[*].leagueSimpName')
    # 开赛时间
    game_datetime = get_val_by_xpath(json_str, '$.matches[*].time')
    # 比赛编号
    game_id = get_val_by_xpath(json_str, '$.matches[*].id')
    # 主队名称
    home_team_name = get_val_by_xpath(json_str, '$.matches[*].hoTeamName')
    # 客队名称
    guest_team_name = get_val_by_xpath(json_str, '$.matches[*].guTeamName')
    # 主队排名
    home_rank = get_val_by_xpath(json_str, '$matches[*].hoRank')
    # 客队排名
    guest_rank = get_val_by_xpath(json_str, '$matches[*].guRank')
    # 主队得分
    home_score = get_val_by_xpath(json_str, '$.matches[*].hoScore')
    # 客队得分
    guest_score = get_val_by_xpath(json_str, '$.matches[*].guScore')
    # 胜赔
    standard_home = get_val_by_xpath(json_str, '$.matches[*].standardHome')
    # 平赔
    standard = get_val_by_xpath(json_str, '$.matches[*].standard')
    # 负赔
    standard_guest = get_val_by_xpath(json_str, '$.matches[*].standardGuest')
    # 胜平负奖金
    award = [' '.join([x, y, z]) for x in standard_home for y in standard for z in standard_guest]
    game_dt = [start_dt for x in game_datetime]
    game_tm = list(map(lambda x: x[11:], game_datetime))
    game_score = list(zip(home_score, home_score))
    game_rst = list(map(lambda x: '-'.join(x), game_score))

    game_info_zip = zip(game_dt, ser_num, game_tm, league_simple_name, home_team_name, guest_team_name,\
                        game_rst, award, home_score, guest_score, game_id, home_rank, guest_rank, standard_home, standard, standard_guest)

    return game_info_zip


# 解析json，获取比赛信息
def get_today_game_info(json_str, start_dt):
    if not len(json_str['matches']):
        return None
    # 编号
    serNum = get_val_by_xpath(json_str, '$.matches[*].serNum')
    # 只保留编号
    serNum = [x[2:] for x in serNum]
    # 联赛
    leagueSimpName = get_val_by_xpath(json_str, '$.matches[*].leagueSimpName')
    # 开赛时间
    game_datetime = get_val_by_xpath(json_str, '$.matches[*].time')
    # 比赛编号
    id = get_val_by_xpath(json_str, '$.matches[*].id')
    # 状态 -1：完
    status = get_val_by_xpath(json_str, '$.matches[*].status')
    # 主队
    hoTeamName = get_val_by_xpath(json_str, '$.matches[*].hoTeamName')
    # 客队
    guTeamName = get_val_by_xpath(json_str, '$.matches[*].guTeamName')
    # 主队得分
    hoScore = get_val_by_xpath(json_str, '$.matches[*].hoScore')
    # 客队得分
    guScore = get_val_by_xpath(json_str, '$.matches[*].guScore')
    # 胜
    standardHome = get_val_by_xpath(json_str, '$.matches[*].standardHome')
    # 平
    standard = get_val_by_xpath(json_str, '$.matches[*].standard')
    # 负
    standardGuest = get_val_by_xpath(json_str, '$.matches[*].standardGuest')
    # 胜负平奖金
    award = [' '.join([x, y, z]) for x in standardHome for y in standard for z in standardHome]
    game_dt = [start_dt for x in game_datetime]
    game_tm = list(map(lambda x: x[11:], game_datetime))
    game_score = list(zip(hoScore, guScore))
    game_rst = list(map(lambda x: '-'.join(x), game_score))

    game_info_zip = zip(game_dt, serNum, game_tm, leagueSimpName, hoTeamName, guTeamName, game_rst, award, hoScore, guScore, id)
    return game_info_zip


# 根据比赛的信息获取比赛的赔率信息
def get_game_ratio_info(game_info_list):
    base_link = 'https://odds.13322.com/toDetailNew?companys=3&thirdmhId={0}&matchId={0}&flag=2&dateTime={1}'
    game_ratio_info_list = []
    for game_info in game_info_list:
        game_id = game_info[-1]
        game_ser_num = game_info[1]
        game_dt = game_info[0]
        game_ratio_url = base_link.format(game_id, game_dt)
        # print(game_ratio_url)
        page_html = get_page_html(game_ratio_url)
        if page_html is None:
            continue
        soup = BeautifulSoup(page_html, 'lxml')
        # companies = soup.find_all('span', 'companyNames')
        # if companies == []:
        #     print(companies)
        # company1 = companies[0].text
        # # company2 = ''
        # # for company in companies:
        # #     if company['id'] == 'company1':
        # #         company1 = company.text
        # #     if company['id'] == 'company2':
        # #         company2 = company.text

        ratios_list = soup.find_all('tbody', 'tb_bar')
        for ratios in ratios_list:
            for tr in ratios.find_all('tr'):
                tr_list = list(tr.find_all('td'))
                status = tr_list[-1]
                position_ratio = tr_list[3].text
                if status.text.strip() not in ('早', '初盘', '即') or position_ratio in ('封', ',封'):
                    continue
                position_tm = tr_list[5].text
                host_ratio = tr_list[2].text
                guest_ratio = tr_list[4].text
                ratio_info = [game_dt, game_ser_num, position_tm, position_ratio, host_ratio, guest_ratio]
                ratio_info.append('皇冠')
                ratio_info.append(game_id)
                game_ratio_info_list.append(ratio_info)
    return game_ratio_info_list


# 开始执行爬虫程序并对指定的数据进行持久化操作
def start_crawl_new(start_dt, end_dt, day_step, url_base):
    file_start_dt = start_dt
    file_end_dt = end_dt
    if url_base is None:
        url_base = 'https://live.13322.com/lotteryScore/list?getExtra=2&lang=zh&date={0}'
    game_info_columns = ['比赛日期', '比赛序号', '比赛时间', '赛事类型', '主队名称', '客队名称', '比分赛果', '胜平负奖金', '主队得分', '客队得分', '比赛ID', '主队排名', '客队排名', '胜赔', '平赔', '负赔']
    game_ratio_info_columns = ['比赛日期', '比赛序号', '盘口时间', '赔率盘口', '主水', '客水', '博彩公司名称', '比赛ID']
    game_info_list = []
    game_ratio_info_list = []

    # 将DataFrame存储为csv,index表示是否显示行名，default=True
    while start_dt <= end_dt:
        print('*' * 100, '正在抓取{}的比赛信息'.format(start_dt), '*' * 100)
        url = url_base.format(start_dt)
        response = get_page_html(url, charsets=('utf-8', 'gbk', 'gb2312'))
        if response is None:
            start_dt = start_dt + day_step
            continue
        json_str = json.loads(response)
        tmp = get_today_game_info_new(json_str, start_dt)
        if tmp is None:
            start_dt = start_dt + day_step
            print('*' * 100, '{}没有数据'.format(start_dt), '*' * 100)
            continue
        game_info_list_tmp = list(tmp)
        game_info_list.extend(game_info_list_tmp)
        game_ratio_info_list.extend(get_game_ratio_info(game_info_list_tmp))
        print('*' * 100, '{}的比赛信息已经抓取完成'.format(start_dt), '*' * 100)
        start_dt = start_dt + day_step
        time.sleep(3)
    game_info_df = pd.DataFrame(game_info_list, columns=game_info_columns)
    game_info_df.drop(['主队得分', '客队得分', '比赛ID'], axis=1, inplace=True)
    game_ratio_info_df = pd.DataFrame(game_ratio_info_list, columns=game_ratio_info_columns)
    game_ratio_info_df.drop(['比赛ID'], axis=1, inplace=True)
    game_info_df.to_csv('game_info_{}-{}.csv'.format(file_start_dt.strftime('%y%m%d'), file_end_dt.strftime('%y%m%d')), index=False, sep=',', columns=game_info_columns[:-3])
    game_ratio_info_df.to_csv('game_ratio_info_{}-{}.csv'.format(file_start_dt.strftime('%y%m%d'), file_end_dt.strftime('%y%m%d')), index=False, sep=',', columns=game_ratio_info_columns[:-1])


# 开始执行爬虫程序并对指定的数据进行持久化操作
def start_crawl(start_dt, end_dt, day_step, url_base):
    file_start_dt = start_dt
    file_end_dt = end_dt
    if url_base is None:
        url_base = 'https://live.13322.com/lotteryScore/list?getExtra=2&lang=zh&date={0}'
    game_info_columns = ['比赛日期', '比赛序号', '比赛时间', '赛事类型', '主队名称', '客队名称', '比分赛果', '胜平负奖金', '主队得分', '客队得分', '比赛ID']
    game_ratio_info_columns = ['比赛日期', '比赛序号', '盘口时间', '赔率盘口', '主水', '客水', '博彩公司名称', '比赛ID']
    game_info_list = []
    game_ratio_info_list = []

    # 将DataFrame存储为csv,index表示是否显示行名，default=True
    while start_dt <= end_dt:
        print('*' * 100, '正在抓取{}的比赛信息'.format(start_dt), '*' * 100)
        url = url_base.format(start_dt)
        response = get_page_html(url, charsets=('utf-8', 'gbk', 'gb2312'))
        if response is None:
            start_dt = start_dt + day_step
            continue
        json_str = json.loads(response)
        tmp = get_today_game_info(json_str, start_dt)
        if tmp is None:
            start_dt = start_dt + day_step
            print('*' * 100, '{}没有数据'.format(start_dt), '*' * 100)
            continue
        game_info_list_tmp = list(tmp)
        game_info_list.extend(game_info_list_tmp)
        game_ratio_info_list.extend(get_game_ratio_info(game_info_list_tmp))
        print('*' * 100, '{}的比赛信息已经抓取完成'.format(start_dt), '*' * 100)
        start_dt = start_dt + day_step
        time.sleep(3)
    game_info_df = pd.DataFrame(game_info_list, columns=game_info_columns)
    game_info_df.drop(['主队得分', '客队得分', '比赛ID'], axis=1, inplace=True)
    game_ratio_info_df = pd.DataFrame(game_ratio_info_list, columns=game_ratio_info_columns)
    game_ratio_info_df.drop(['比赛ID'], axis=1, inplace=True)
    game_info_df.to_csv('game_info_{}-{}.csv'.format(file_start_dt.strftime('%y%m%d'), file_end_dt.strftime('%y%m%d')), index=False, sep=',', columns=game_info_columns[:-3])
    game_ratio_info_df.to_csv('game_ratio_info_{}-{}.csv'.format(file_start_dt.strftime('%y%m%d'), file_end_dt.strftime('%y%m%d')), index=False, sep=',', columns=game_ratio_info_columns[:-1])


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


def get_today_game_info_500(response, start_dt):
    soup = BeautifulSoup(response, 'lxml')
    game_info = []
    print(soup.prettify())
    xx = soup.find_all('tbody', id="match-tbody").find_all('tr')
    for tr in soup.find_all('tbody', id='main-body'):
        game_info_item = dict()
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
            game_info_item['award'] = ' '.join(
                [game_info_item['standardHome'], game_info_item['standard'], game_info_item['standardGuest']])
        game_info.append(game_info_item)
    return game_info


def start_crawl_500(start_dt, end_dt, day_step, url_base):
    file_start_dt = start_dt
    file_end_dt = end_dt
    if url_base is None:
        url_base = 'https://live.13322.com/lotteryScore/list?getExtra=2&lang=zh&date={0}'
    game_info_columns = ['比赛日期', '比赛序号', '比赛时间', '赛事类型', '主队名称', '客队名称', '比分赛果', '胜平负奖金', '主队得分', '客队得分', '比赛ID']
    game_ratio_info_columns = ['比赛日期', '比赛序号', '盘口时间', '赔率盘口', '主水', '客水', '博彩公司名称', '比赛ID']
    game_info_list = []
    game_ratio_info_list = []
    # 将DataFrame存储为csv,index表示是否显示行名，default=True
    while start_dt <= end_dt:
        print('*' * 100, '正在抓取{}的比赛信息'.format(start_dt), '*' * 100)
        url = url_base.format(start_dt)
        response = get_page_html(url, charsets=('utf-8', 'gbk', 'gb2312'))
        if response is None:
            start_dt = start_dt + day_step
            continue
        tmp = get_today_game_info_500(response, start_dt)
        if tmp is None:
            start_dt = start_dt + day_step
            print('*' * 100, '{}没有数据'.format(start_dt), '*' * 100)
            continue
        game_info_list_tmp = list(tmp)
        game_info_list.extend(game_info_list_tmp)
        game_ratio_info_list.extend(get_game_ratio_info(game_info_list_tmp))
        print('*' * 100, '{}的比赛信息已经抓取完成'.format(start_dt), '*' * 100)
        start_dt = start_dt + day_step
        time.sleep(3)
    game_info_df = pd.DataFrame(game_info_list, columns=game_info_columns)
    game_info_df.drop(['主队得分', '客队得分', '比赛ID'], axis=1, inplace=True)
    game_ratio_info_df = pd.DataFrame(game_ratio_info_list, columns=game_ratio_info_columns)
    game_ratio_info_df.drop(['比赛ID'], axis=1, inplace=True)
    game_info_df.to_csv('game_info_{}-{}.csv'.format(file_start_dt.strftime('%y%m%d'), file_end_dt.strftime('%y%m%d')),
                        index=False, sep=',', columns=game_info_columns[:-3])
    game_ratio_info_df.to_csv(
        'game_ratio_info_{}-{}.csv'.format(file_start_dt.strftime('%y%m%d'), file_end_dt.strftime('%y%m%d')),
        index=False, sep=',', columns=game_ratio_info_columns[:-1])


def main():
    # ssl._create_default_https_context = ssl._create_unverified_context
    start_dt = datetime.date(2019, 7, 9)
    day_step = datetime.timedelta(days=1)
    # end_dt = datetime.date.today()
    end_dt = datetime.date(2019, 7, 9)
    page_url_base = 'https://live.13322.com/lotteryScore/list?getExtra=2&lang=zh&date={0}'
    start_crawl(start_dt, end_dt, day_step, page_url_base)
    # start_crawl_new(start_dt, end_dt, day_step, page_url_base)


game_info_url_base = 'http://odds.500.com/index_jczq_{0}.shtml'
game_ratio_info_url_base = 'http://odds.500.com/fenxi/yazhi-{0}.shtml'


def main_500():
    start_dt = datetime.date(2019, 7, 7)
    day_step = datetime.timedelta(days=1)
    # end_dt = datetime.date.today()
    end_dt = datetime.date(2019, 7, 8)
    start_crawl_500(start_dt, end_dt, day_step, url_base=game_info_url_base)


    pass


if __name__ == '__main__':
    main()
#     https://odds.13322.com/toDetailNew?companys=3&companys=-3&thirdmhId=3705040&matchId=3705040&dateTime=2019-01-01&flag=2&refreshTime=20
