import datetime
import sqlite3 

conn = sqlite3.connect('baza1.db')
cursor = conn.cursor()

current_date = datetime.date.today() #текущая дата и время
current_date = int(current_date.strftime("%d%m"))
#print(current_date)



#cursor.execute("SELECT `snils` FROM `Users`")
#dateint = cursor.fetchall()
#print(dateint)
#a = int(input('дата: \n')) #date
#b = a - 100 #dateint


#if current_date == b:
#    print('вам завтра на прием')
#else:
#    exit


#conn.close