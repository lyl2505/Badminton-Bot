import json
from datetime import date

filename = 'check-in_dates.txt'

def member_info_init(filename):
    total_days = 1
    file_info = {'total_days': total_days,
                 'members': []}
    f = open(filename, 'r')
    today_date = date.today()
    for line in f:
        member_info = line.split(' ')
        username = member_info[0]

        # find number of days since last checkin
        checkin_date = date.fromisoformat(member_info[1])
        time_difference = (today_date - checkin_date).days

        # setup single member information dict
        times_played = 1
        member_dict = {username : {
                        'times_played': times_played,
                        'hours_played': 1,
                        'rate': times_played / total_days * 100,
                        'last_played': time_difference
        }}

        file_info['members'].append(member_dict)

    return file_info