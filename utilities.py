import calendar

def diff_month(date1, date2):
    return (date1.year - date2.year) * 12 + date1.month - date2.month


def get_last_day_of_month(year, month):
    return calendar.monthrange(year, month)[1]


def convert_card_to_digit(card_num):
    ranks_str = card_num.split()
    digit = 0
    for rank_str in ranks_str:
        for char_digit in rank_str:
            digit = digit + int(char_digit)
            if digit > 9:
                digit = sum(map(int, str(digit)))
                
    return digit


def get_seeded_file_name(seed, valuation_date):
    short_timestamp = valuation_date.strftime('%Y%m')
    long_timestamp = valuation_date.strftime('%Y%m%d%H%M%S')
    file_name = '_'.join([short_timestamp, str(seed), long_timestamp])
    return file_name


def write_csv_file(file_name, data_frame):
    data_frame.to_csv(file_name, sep=',', encoding='utf-8')