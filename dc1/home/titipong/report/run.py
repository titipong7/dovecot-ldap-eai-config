#!/usr/bin/python3

import os
import datetime
import mysql.connector
from datetime import date, datetime, timedelta
from mysql.connector import Error

os.chdir('/var/log/')

important = []
keep_phrases = ["imap-login: Login:"]
count7 = 0
count7set= set()
count30 = 0
count30set= set()
emailarray = []
emailset = set()

## for specific date 
#d1 = "30"
#date1 = "20220130"
#date_now = date_now - timedelta(days=3)
#cdate = "2022-01-30"

today = date.today()
d1 = today.strftime("%d")
date1 = today.strftime("%Y%m%d")

dd1 = int(d1)
dd2 = dd1 - 7

date_now = datetime.now()
date_last7days = date_now - timedelta(days=7)
date_last30days = date_now - timedelta(days=30)

cdate = today.strftime("%Y-%m-%d")
cdate1 = cdate+" 00:00:00"
cdate2 = cdate+" 23:59:59"

def connect(weekly, monthly, date1, date2):
    """ Connect to MySQL database """
    conn = None

    sql = "UPDATE kon_stat SET weekly_active_imap_user = %s, monthly_active_imap_user = %s WHERE logtime BETWEEN %s AND %s ";
    data = (weekly, monthly, date1, date2)
    try:
        conn = mysql.connector.connect(host='10.1.1.228',
                                       database='webcontent',
                                       user='mailstat',
                                       password='2P3K4Lsi_PW-1lOw')
        if conn.is_connected():
            print('Connected to MySQL database')

        cursor = conn.cursor()
        cursor.execute(sql, data)
        # accept the changes
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn is not None and conn.is_connected():
            conn.close()



def mdy_to_ymd(d):
    return datetime.strptime(d, '%b %d, %Y').strftime('%Y-%m-%d %H:%M:%S.%f')

#logday = mdy_to_ymd('May 25, 2021')
#date_time_obj = datetime.strptime(logday, '%Y-%m-%d %H:%M:%S.%f')
maillog = []
arr = os.listdir("/var/log/")
for item in arr:
    if 'maillog' in item:
        maillog.append(item)

# print(maillog)
for maillogfile in maillog:
    print(maillogfile)
    with open(maillogfile, "r", encoding="latin-1") as f:
        f = f.readlines()

    for line in f:
        for phrase in keep_phrases:
            if phrase in line:
                important.append(line)
                # print(line)
                l = line.split()
                month = l[0]
                day = l[1]
                email = l[7]
                email = email[6:]
                email = email[:-2]
                
                emailset.add(email)
                # for m in emailarray:
                #     if email in m:
                #         emailarray.append(email)
            
                logday = mdy_to_ymd(month+' '+day+', 2022')
                date_time_obj = datetime.strptime(logday, '%Y-%m-%d %H:%M:%S.%f')
                if date_last7days <= date_time_obj <= date_now:
                    count7 = count7 + 1
                    count7set.add(email)

                if date_last30days <= date_time_obj <= date_now:
                    count30 = count30 + 1
                    count30set.add(email)

                # print(count)
                # print(line.split(' '))
                #print(month)
                # print(day)
                #print(email)
                break
                

#print("Today's date:", date_now)
#print("date_time_obj", date_time_obj)

#print(email)
print(emailset)


f = open("/home/titipong/report/"+date1, "a")
f.write(str(len(count7set)) + ":" + str(count7) + ": imap-login last 7 days: "+str(date_last7days)+" to "+str(date_now)+"\r\n")
f.write(str(len(count30set)) + ":" + str(count30) + ": imap-login last 30 days: "+str(date_last30days)+" to "+str(date_now)+"\r\n")
f.close()
#print(important)
connect(str(len(count7set)), str(len(count30set)), cdate1, cdate2);
