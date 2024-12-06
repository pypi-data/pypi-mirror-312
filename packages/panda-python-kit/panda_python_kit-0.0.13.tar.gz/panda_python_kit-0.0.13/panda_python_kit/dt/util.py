from dateutil import parser
from datetime import datetime
import time

# str
def str2dt(dt_str, date_format=None):
    """  
    将字符串转换为日期时间对象。  
    如果提供了日期格式，则使用strptime；否则，使用dateutil.parser.parse进行解析。  
    """
    if date_format:
        return datetime.strptime(dt_str, date_format)
    else:
        return parser.parse(dt_str)

def str2ts(dt_str, date_format=None):
    """
    将字符串转换为时间戳。
    如果提供了日期格式，则使用strptime；否则，使用dateutil.parser.parse进行解析。
    """
    dt = str2dt(dt_str, date_format)
    return dt2ts(dt)

def dt2ts(dt):
    """  
    将日期时间对象转换为时间戳。  
    """
    return int(dt.timestamp()*1000)


def ts2dt(ts):
    """  
    将时间戳转换为日期时间对象。  
    """
    return datetime.fromtimestamp(ts/1000)


def dt2str(dt, date_format):
    """  
    将日期时间对象转换为格式化的字符串。  
    """
    return dt.strftime(date_format)

def ts2str(ts, date_format="%Y%m%d%H%M%S"):
    """
    将时间戳转换为格式化的字符串。
    """
    return dt2str(ts2dt(ts), date_format)

def to_dt_str(input):
    """
    时间戳，或者日期对象，或者
    :param ts:
    :return:
    """
    if isinstance(input, int):
        return ts2str(input)
    elif isinstance(input, datetime):
        return dt2str(input)
    elif isinstance(input, str):
        if len(input) ==14:
            return input
        if len(input) ==10 :
            return ts2str(int(input)*1000)
        if len(input) == 13:
            return ts2str(int(input))
    else:
        raise Exception("ts must be int or datetime or str")
