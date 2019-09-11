import scrapy


class GameInfoItem(scrapy.Item):
    game_id = scrapy.Field()
    game_dt = scrapy.Field()
    ser_num = scrapy.Field()
    game_tm = scrapy.Field()
    league_simple_name = scrapy.Field()
    home_team_name = scrapy.Field()
    guest_team_name = scrapy.Field()
    game_rst = scrapy.Field()
    award = scrapy.Field()
    home_score = scrapy.Field()
    guest_score = scrapy.Field()
    home_rank = scrapy.Field()
    guest_rank = scrapy.Field()
    standard_home = scrapy.Field()
    standard = scrapy.Field()
    standard_guest = scrapy.Field()


class GameRatioInfoYazhiItem(scrapy.Item):
    game_id = scrapy.Field()
    game_dt = scrapy.Field()
    ser_num = scrapy.Field()
    position_tm = scrapy.Field()
    home_ratio = scrapy.Field()
    position_ratio = scrapy.Field()
    guest_ratio = scrapy.Field()
    status = scrapy.Field()
    company = scrapy.Field()


class GameRatioInfoOuzhiItem(scrapy.Item):
    game_id = scrapy.Field()
    game_dt = scrapy.Field()
    ser_num = scrapy.Field()
    win_ratio = scrapy.Field()
    draw_ratio = scrapy.Field()
    fail_ratio = scrapy.Field()
    status = scrapy.Field()
    company = scrapy.Field()