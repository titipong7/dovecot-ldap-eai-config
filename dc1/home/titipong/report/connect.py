import mysql.connector
import datetime
from datetime import date
from mysql.connector import Error

def connect():
    """ Connect to MySQL database """
    conn = None

    date_object = datetime.date.today()
    date_str = date_object.strftime('%Y-%m-%d')

    date1 = date_str+" 00:00:00"
    date2 = date_str+" 23:59:59"
    sql = "UPDATE kon_stat SET weekly_active_imap_user = '2', monthly_active_imap_user = '2'  WHERE logtime BETWEEN %s AND %s ";
    data = (date1, date2)
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


if __name__ == '__main__':
    connect()
