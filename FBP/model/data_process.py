# -*- coding: utf-8 -*-
import pandas as pd
import configparser
import re
from tsfresh import extract_relevant_features
from sklearn.tree import DecisionTreeClassifier
from tsfresh.feature_extraction import MinimalFCParameters, EfficientFCParameters, ComprehensiveFCParameters
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

base_path = './../crawler/output'
game_info_test_path = base_path + '/game_info_2019.csv'
game_info_tot_path = base_path + '/game_info.csv'
game_info_increment_path = base_path + '/game_info_increment.csv'
game_info_model_path = 'data/game_info_model.csv'

game_ratio_info_test_path = base_path + '/game_ratio_info_2019.csv'
game_ratio_info_tot_path = base_path + '/game_ratio_info.csv'
game_ratio_info_increment_path = base_path + '/game_ratio_info_increment.csv'
game_ratio_info_model_path = 'data/game_ratio_info_model.csv'


def get_conf_item(section, option, conf_file='config.cof', is_eval=False):
    """
    获取配置文件中的配置项
    :param section:配置项归属组名称
    :param option:配置项名称
    :param conf_file:配置文件路径
    :param is_eval:是否计算字符串中的代码
    :return:返回配置项的值
    """
    cfg = configparser.ConfigParser()
    cfg.read(conf_file, encoding='utf8')
    option = cfg.get(section, option)
    if is_eval:
        option = eval(option)
    return option


def get_three_cls(home_score, guest_score):
    """
    赛果的三元分类映射
    :param home_score:主队得分
    :param guest_score:客队得分
    :return:分类
    """
    if home_score > guest_score:
        return 1
    elif home_score == guest_score:
        return 0
    else:
        return 2


def process_game_info(path):
    """
    清理比赛信息数据
    :param path: 比赛信息路径
    :return: 返回清理后的数据
    """
    game_info = pd.read_csv(path, encoding='utf8')
    game_info_clean = game_info[get_conf_item('data', 'game_info_raw', is_eval=True)]
    game_info_clean['home_rank_clean'] = game_info_clean['home_rank'].fillna(0).map(lambda x: re.search('\d+', str(x)).group(0))
    game_info_clean['guest_rank_clean'] = game_info_clean['guest_rank'].fillna(0).map(lambda x: re.search('\d+', str(x)).group(0))
    game_info_clean['game_rst_two_cls'] = game_info_clean.apply(lambda x: 1 if x['home_score'] > x['guest_score'] else 0, axis=1)
    game_info_clean['game_rst_three_cls'] = game_info_clean.apply(lambda x: get_three_cls(x['home_score'], x['guest_score']), axis=1)
    return game_info_clean


def process_game_ratio_info(path):
    """
    清理比赛赔率变化信息数据
    :param path: 比赛赔率变化信息路径
    :return: 返回清理后的数据
    """
    game_ratio_info = pd.read_csv(path, encoding='utf8')
    game_ratio_info_clean = game_ratio_info[get_conf_item('data', 'game_ratio_info_raw', is_eval=True)]
    odds_grail_map = get_conf_item('data', 'odds_grail_map', is_eval=True)
    game_ratio_info_clean['odds_grail'] = game_ratio_info_clean['position_ratio'].map(odds_grail_map)
    return game_ratio_info_clean


def get_intersection(game_info_df, game_ratio_info_df):
    """
    对比比赛信息和比赛赔率变化信息，只保留两个数据集有交集的数据，交集依据game_id
    :param game_info_df:比赛信息数据集
    :param game_ratio_info_df:比赛赔率变化信息数据集
    :return:返回game_id重合的两个数据集
    """
    game_info_game_id_set = set(game_info_df['game_id'].values)
    game_ratio_info_df.dropna(axis=0, how='any', inplace=True)
    game_ratio_info_game_id_set = set(game_ratio_info_df['game_id'].values)
    game_id_intersection = game_info_game_id_set & game_ratio_info_game_id_set
    game_info_df = game_info_df[game_info_df['game_id'].isin(game_id_intersection)]
    game_ratio_info_df = game_ratio_info_df[game_ratio_info_df['game_id'].isin(game_id_intersection)]
    return game_info_df, game_ratio_info_df


def append_increment_data():
    """
    添加数据到文件中
    :return:
    """
    game_info_df = process_game_info(game_info_increment_path)
    game_ratio_info_df = process_game_ratio_info(game_ratio_info_increment_path)
    game_info_clean, game_ratio_info_clean = get_intersection(game_info_df, game_ratio_info_df)
    game_info_clean.to_csv(game_info_model_path, mode='a', header=False, index=False)
    game_ratio_info_clean.to_csv(game_ratio_info_model_path, mode='a', header=False, index=False)
    return None


def init_data_model():
    """
    初始化所有数据
    :return:
    """
    game_info_df = process_game_info(game_info_test_path)
    game_ratio_info_df = process_game_ratio_info(game_ratio_info_test_path)
    game_info_clean, game_ratio_info_clean = get_intersection(game_info_df, game_ratio_info_df)
    game_info_clean.to_csv(game_info_model_path, mode='w', index=False)
    game_ratio_info_clean.to_csv(game_ratio_info_model_path, mode='w', index=False)
    return None


def extract_game_tot_feature(game_info_df, game_ratio_info_df):
    game_ratio_info_data = game_ratio_info_df[get_conf_item('data', 'game_ratio_info_clean', is_eval=True)]
    game_ratio_info_data.drop(['odds_grail', 'guest_ratio'], axis=1, inplace=True)
    y = game_info_df[['game_id', 'game_rst_two_cls']]
    y = pd.Series(y['game_rst_two_cls'].map(lambda x: x == 1).values, index=y.game_id)
    settings = ComprehensiveFCParameters()
    game_ratio_info_model = extract_relevant_features(game_ratio_info_data, y, fdr_level=0.1, default_fc_parameters=settings, column_id='game_id', column_sort='position_tm')
    game_ratio_info_model.to_csv('game_ratio_info_model.csv', index=True)


def main():
    init_data_model()
    # append_increment_data()
    game_info_model = pd.read_csv(game_info_model_path, encoding='utf8')
    game_ratio_info_model = pd.read_csv(game_ratio_info_model_path, encoding='utf8')
    extract_game_tot_feature(game_info_model, game_ratio_info_model)
    game_ratio_info_model = pd.read_csv('game_ratio_info_model.csv', encoding='utf8')
    game_ratio_info_model.drop(['id'], axis=1, inplace=True)
    y = game_info_model['game_rst_two_cls']
    # game_ratio_info_model.to_csv('game_ratio_info_model_1.csv', index=False)
    X_train, X_test, y_train, y_test = train_test_split(game_ratio_info_model, y, test_size=0.6)
    cl = DecisionTreeClassifier()
    cl.fit(X_train, y_train)
    print(classification_report(y_test, cl.predict(X_test)))


if __name__ == '__main__':
    main()