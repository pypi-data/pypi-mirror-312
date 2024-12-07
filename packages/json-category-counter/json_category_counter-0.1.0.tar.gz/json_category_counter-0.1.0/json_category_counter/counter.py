# json_category_counter/counter.py

import sys
import json

def count_category_and_total(json_file, key_one):
    """
    读取 JSON 文件，统计每个分类的 'Tests' 数量，并返回总数和每个分类的数量字典。

    :param json_file: JSON 文件路径
    :param key_one: JSON 中的一级键
    :return: (total_count, category_dict) 其中 total_count 是总数，category_dict 是每个分类及其数量的字典
    """
    with open(json_file, encoding='utf-8') as f:
        f_read = json.load(f)

    # 获取 key_one 下的所有分类
    categories = f_read.get(key_one, {}).keys()
    list_categories = list(categories)

    total_count = 0
    category_dict = {}

    # 统计每个分类的数量
    for category in list_categories:
        count_number = len(f_read[key_one][category]['Tests'])
        print(f"{category} count is : {count_number}")
        total_count += count_number
        category_dict[category] = count_number

    return total_count, category_dict
