import re


def main():

    print(re.search('\d+', '英乙 9').group(0))
    # print(y)

    # extracted_features = extract_features(timeseries, column_id="id", column_sort="time")

    # impute(extracted_features)
    # features_filtered = select_features(extracted_features, y)
    # features_filtered = extract_relevant_features(timeseries, y, column_id='id', column_sort='time')
    # print(type(features_filtered))
    # print(features_filtered.head())

if __name__ == '__main__':
    main()