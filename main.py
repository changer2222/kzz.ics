# coding=utf-8
import json, requests
from datetime import datetime, timedelta
from ics import Calendar, DisplayAlarm, Event

def main():
    url = "https://bit.ly/3jkKlrU"
    header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
    response = requests.get(url, headers=header)
    response.encoding = response.apparent_encoding
    json_data = json.loads(response.text)

    c = Calendar()
    for data in json_data:
        start_date_str = data['STARTDATE'].split('T')[0] #2020-10-24T00:00:00 ==> 2020-10-24
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        if start_date >= datetime.now().date():
            e = Event()
            e.name  = data['SNAME'] + "申购" 
            # 9:30 - 11:30
            e.begin = data['STARTDATE'].replace("T00:00:00", " 01:30:00") 
            e.end   = data['STARTDATE'].replace("T00:00:00", " 03:30:00") 
            e.alarms.append(DisplayAlarm(trigger=timedelta(minutes=30), display_text=e.name)) # 10:00
            c.events.add(e)
           
    with open('kzz.ics', 'w') as my_file:
        my_file.writelines(c)
        
if __name__ == '__main__':
    main()