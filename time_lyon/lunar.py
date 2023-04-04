# coding=UTF-8
#########################################################
# Author        : Lyon
# Email         : 397835809@qq.com
# Last modified : 2020-08-30 16:25:42
# Filename      : lunar.py
# Description   : 公历转农历日期转换
#########################################################
# !/usr/bin/python

import os
import datetime

# 农历年份原始数据, 从公历1900-01-31为农历00-01-01起算
LUNAR_YEAR_RAW_DATA = (
    0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2,
    0x04ae0, 0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0, 0x14977,
    0x04970, 0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970,
    0x06566, 0x0d4a0, 0x0ea50, 0x06e95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950,
    0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0, 0x092d0, 0x0d2b2, 0x0a950, 0x0b557,
    0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5d0, 0x14573, 0x052d0, 0x0a9a8, 0x0e950, 0x06aa0,
    0x0aea6, 0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260, 0x0f263, 0x0d950, 0x05b57, 0x056a0,
    0x096d0, 0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558, 0x0b540, 0x0b5a0, 0x195a6,
    0x095b0, 0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46, 0x0ab60, 0x09570,
    0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x055c0, 0x0ab60, 0x096d5, 0x092e0,
    0x0c960, 0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0, 0x0cab5,
    0x0a950, 0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x15176, 0x052b0, 0x0a930,
    0x07954, 0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0, 0x0d260, 0x0ea65, 0x0d530,
    0x05aa0, 0x076a3, 0x096d0, 0x04bd7, 0x04ad0, 0x0a4d0, 0x1d0b6, 0x0d250, 0x0d520, 0x0dd45,
    0x0b5a0, 0x056d0, 0x055b2, 0x049b0, 0x0a577, 0x0a4b0, 0x0aa50, 0x1b255, 0x06d20, 0x0ada0
)

# 取出闰月的掩码
MASK_GET_LUNAR_MONTH = 0x0000f

# 若是有闰月，确定闰月大小月，为0是小月
MASK_GET_LUNAR_LEAP_MONTH_BIG = 0xf0000

# 取出除闰月外正常的大小月关系的掩码
MASK_GET_NORMAL_MONTH_BIG = 0x0fff0

# 年份原始数据解析后存入字典
LUNAR_YEAR_ANALYSED_DICT = dict()

# 用来确定今年是农历的哪一年
LUNAR_YEAR_DAY_COUNT_LIST = list()

START_LUNAR_YEAR = 0

def _init_lunar_year_analysed_dict():
    now_year = START_LUNAR_YEAR
    for one_year_bits in LUNAR_YEAR_RAW_DATA:
        leap_month = one_year_bits & MASK_GET_LUNAR_MONTH
        normal_month_big = (one_year_bits & MASK_GET_NORMAL_MONTH_BIG) >> 4
        normal_month_big = "0" * (12 - len(bin(normal_month_big).replace("0b", ""))) + bin(normal_month_big).replace(
            "0b", "")
        is_big_leap_month = (one_year_bits & MASK_GET_LUNAR_LEAP_MONTH_BIG if leap_month > 0 else 0) >> 16
        LUNAR_YEAR_ANALYSED_DICT[now_year] = {
            "NormalMonthBig": normal_month_big,
            "LeapMonth": leap_month,
            "IsLeapMonthBig": is_big_leap_month
        }
        day_count = _count_a_lunar_yaar_days(leap_month, is_big_leap_month, normal_month_big)
        LUNAR_YEAR_DAY_COUNT_LIST.append(day_count)
        now_year += 1


def _count_a_lunar_yaar_days(leap_month, is_big_leap_month, normal_month_big):
    if not leap_month:
        day_count = 0
    elif is_big_leap_month:
        day_count = 30
    else:
        day_count = 29
    return day_count + 12 * 29 + normal_month_big.count("1")


# 农历的年份解析数据已经准备好
_init_lunar_year_analysed_dict()

# 开始的年 月 日（公历）
START_DATE_TIME = datetime.datetime.strptime("%04d-%02d-%02d" % (1900, 1, 30), '%Y-%m-%d')

def _count_gap_days_from_start_year(datetime_str):
    '''
    :param   datetime_str: eg "2020-08-30"
    :return: gap_days
    '''
    return (datetime.datetime.strptime(datetime_str, '%Y-%m-%d') - START_DATE_TIME).days


def _get_this_lunner_year_month_list(year_analysed_dict):
    leap_month = year_analysed_dict["LeapMonth"]
    month_list = list()
    for idx, is_big in enumerate(year_analysed_dict["NormalMonthBig"]):
        month = idx + 1
        if is_big == "0":
            month_list.append(29)
        else:
            month_list.append(30)
        if month == leap_month:
            month_list.append(30 if year_analysed_dict["IsLeapMonthBig"] else 29)
    return month_list


def get_lunar_date_str_from_date_str(datetime_str):
    '''
    :param   datetime_str: eg "2020-08-30" should larger than "1900-01-30" and less than 2050-01-21
    :return: lunar_datetime_str eg like: "0120-04-15 Lunar" or "0120-04-15"
    '''
    gap_days = _count_gap_days_from_start_year(datetime_str)
    if gap_days <= 0:
        raise ValueError("%s is not a valid input!" % datetime_str)
    year_analysed_dict, got_lunar_year = None, None
    for idx, year_days in enumerate(LUNAR_YEAR_DAY_COUNT_LIST):
        if gap_days < year_days:
            got_lunar_year = idx
            year_analysed_dict = LUNAR_YEAR_ANALYSED_DICT.get(idx)
            break
        else:
            gap_days -= year_days
    if got_lunar_year is None or year_analysed_dict is None:
        raise Exception("Got no lunar year or year_analysed_dict!")
    lunar_year_month_list = _get_this_lunner_year_month_list(LUNAR_YEAR_ANALYSED_DICT[got_lunar_year])
    now_month = 1
    for idx, day_count in enumerate(lunar_year_month_list):
        if gap_days <= day_count:
            break
        else:
            gap_days -= day_count
        now_month += 1
    if gap_days <= 0:
        raise Exception("gap_days <= 0 after calculating!")
    is_leap_month = ""
    if year_analysed_dict["LeapMonth"] and now_month > year_analysed_dict["LeapMonth"]:
        now_month -= 1
        if now_month == year_analysed_dict["LeapMonth"]:
            is_leap_month = "Leap"
    return "%04d-%02d-%02d %s" % (got_lunar_year, now_month, gap_days, is_leap_month)

if __name__ == "__main__":
    print(get_lunar_date_str_from_date_str("1900-01-31"))
