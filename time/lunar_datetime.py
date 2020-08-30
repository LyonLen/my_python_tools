# coding=UTF-8
#########################################################
# Author        : Lyon
# Email         : 397835809@qq.com
# Last modified : 2018-12-26 04:16:02
# Filename      : lunar_datetime.py
# Description   : 
#########################################################
#!/usr/bin/python
import json
# from 1900-01-31 to 2050
raw_data = (
            0x04bd8,0x04ae0,0x0a570,0x054d5,0x0d260,0x0d950,0x16554,0x056a0,0x09ad0,0x055d2,
            0x04ae0,0x0a5b6,0x0a4d0,0x0d250,0x1d255,0x0b540,0x0d6a0,0x0ada2,0x095b0,0x14977,
            0x04970,0x0a4b0,0x0b4b5,0x06a50,0x06d40,0x1ab54,0x02b60,0x09570,0x052f2,0x04970,
            0x06566,0x0d4a0,0x0ea50,0x06e95,0x05ad0,0x02b60,0x186e3,0x092e0,0x1c8d7,0x0c950,
            0x0d4a0,0x1d8a6,0x0b550,0x056a0,0x1a5b4,0x025d0,0x092d0,0x0d2b2,0x0a950,0x0b557,
            0x06ca0,0x0b550,0x15355,0x04da0,0x0a5d0,0x14573,0x052d0,0x0a9a8,0x0e950,0x06aa0,
            0x0aea6,0x0ab50,0x04b60,0x0aae4,0x0a570,0x05260,0x0f263,0x0d950,0x05b57,0x056a0,
            0x096d0,0x04dd5,0x04ad0,0x0a4d0,0x0d4d4,0x0d250,0x0d558,0x0b540,0x0b5a0,0x195a6,
            0x095b0,0x049b0,0x0a974,0x0a4b0,0x0b27a,0x06a50,0x06d40,0x0af46,0x0ab60,0x09570,
            0x04af5,0x04970,0x064b0,0x074a3,0x0ea50,0x06b58,0x055c0,0x0ab60,0x096d5,0x092e0,
            0x0c960,0x0d954,0x0d4a0,0x0da50,0x07552,0x056a0,0x0abb7,0x025d0,0x092d0,0x0cab5,
            0x0a950,0x0b4a0,0x0baa4,0x0ad50,0x055d9,0x04ba0,0x0a5b0,0x15176,0x052b0,0x0a930,
            0x07954,0x06aa0,0x0ad50,0x05b52,0x04b60,0x0a6e6,0x0a4e0,0x0d260,0x0ea65,0x0d530,
            0x05aa0,0x076a3,0x096d0,0x04bd7,0x04ad0,0x0a4d0,0x1d0b6,0x0d250,0x0d520,0x0dd45,
            0x0b5a0,0x056d0,0x055b2,0x049b0,0x0a577,0x0a4b0,0x0aa50,0x1b255,0x06d20,0x0ada0
           )

# the Gregorian calendar leap year
def IsLeapYear(year):
    if year % 100 == 0:
        if year % 400 == 0:
            return True
        else:
            return False
    elif year % 4 == 0:
        return True
    else:
        return False

def month_data_cal(year):
    isleapyear = IsLeapYear(year)
    month_data = {}
    for i in range(1, 13):
        days = 30
        if i == 2:
            days = 28
            if isleapyear:
                days += 1
            month_data[i] = days
            continue
        if yearmonthstr[i-1] == '1':
            days += 1
        month_data[i] = days
    return month_data

yearmonthstr    = "101010110101"
month_data      = month_data_cal(2001)
leap_month_data = month_data_cal(2004)

def next_date(str_date):
    start_date  = str_date.split("-")
    start_year  = (int)(start_date[0])
    start_month = (int)(start_date[1])
    start_day   = (int)(start_date[2])
    if IsLeapYear(start_year):
        tmp_month_data = leap_month_data
    else:
        tmp_month_data = month_data
    if start_month == 12:
        if start_day == 31:
            start_year += 1
            start_month = 1
            start_day = 1
        else:
            start_day += 1
    elif start_day == tmp_month_data[start_month]:
        start_month += 1
        start_day = 1
    else:
        start_day += 1
    return str(start_year) + "-" + str(start_month).rjust(2, "0") + "-" + str(start_day).rjust(2, "0") 

# the lunar calandar in China
def lunar_month_list():
    dict_year={}
    gen = (i for i in range(0, 200))
    for raw_item in raw_data:
        lunaryeardata = str(bin(raw_item))[2:].rjust(20, '0')
        month_data    = {}
        count         = 0
        isbigmonth    = True if bool(int(lunaryeardata[0:4], 2)) else False
        which_is_leap_month = int(lunaryeardata[16:20], 2)
        '''
        print lunaryeardata
        print lunaryeardata[16:20]
        print lunaryeardata[0:4]
        print lunaryeardata[4:16]
        '''
        for i in lunaryeardata[4:16]:
            count += 1
            basic_days = 29
            if count == which_is_leap_month:
                tmp_days_leap = basic_days
                if isbigmonth:
                    tmp_days_leap += 1
                month_data[count+100] = {"num": tmp_days_leap, "leap_month": which_is_leap_month}
            if i == '1':
                basic_days += 1
            month_data[count] = {"num": basic_days, "leap_month": 0}
        dict_year[gen.next()]=month_data
    return dict_year

lunar_month_list_data = lunar_month_list()
def lunar_next_day(lunar_date, is_leap_year):
    start_date  = lunar_date.split("-")
    start_year  = (int)(start_date[0])
    start_month = (int)(start_date[1])
    start_day   = (int)(start_date[2])

    isleapyear  = True if len(lunar_month_list_data[start_year]) == 13 else False
    start_is_leap_month = 0
    if isleapyear:
        start_is_leap_month = (int)(start_date[3])
        tmp_month_data = start_month + 100 if start_is_leap_month else start_month
        # 这里面都是月底
        if start_day == lunar_month_list_data[start_year][tmp_month_data]["num"]:
            # 起始月份就是闰月
            if bool(start_is_leap_month):
                # 12月跨年
                if start_month == 12:
                    start_year  += 1
                    start_month  = 1
                    start_day    = 1
                # 非12月，不跨年
                else:
                    start_month += 1
                    start_day    = 1
                start_is_leap_month = 0
            else:
                next_month_is_leap_month = True if lunar_month_list_data[start_year].has_key(start_month + 100) else False
                # 下个月是闰月
                if next_month_is_leap_month:
                    start_day           = 1
                    start_is_leap_month = 1
                # 下个月不是闰月
                else:
                    if start_month == 12:
                        start_year  += 1
                        start_month  = 1
                        start_day    = 1
                    else:
                        start_month += 1 
                        start_day    = 1
                    start_is_leap_month = 0
        else:
            start_day += 1
    else:
        if start_day == lunar_month_list_data[start_year][start_month]["num"]:
            if start_month == 12:
                start_year  += 1
                start_month  = 1
                start_day    = 1
            else:
                start_month += 1
                start_day    = 1
        else:
            start_day += 1
        start_is_leap_month = 0

    isleapyear  = True if len(lunar_month_list_data[start_year]) == 13 else False
    return '%d-%d-%d-%d' % (start_year, start_month, start_day, start_is_leap_month), bool(isleapyear)

if __name__ == "__main__":
    next_day =  next_date("1900-01-31")
    lunar_next_date, isleap = lunar_next_day("0-1-1-0", True)
    # 这个能跑出直到2050-01-22号的新历和农历的对应天
    for i in range(0,54777):
        next_day =  next_date(next_day)
        lunar_next_date, isleap = lunar_next_day(lunar_next_date, isleap)
        print next_day ,",", lunar_next_date
