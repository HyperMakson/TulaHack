import datetime
import sqlite3
import asyncio
import aioschedule

async def noon_print():
    print("It's noon!")

async def scheduler():
    aioschedule.every().day.at("12:00").do(noon_print)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(_):
    asyncio.create_task(scheduler())

conn = sqlite3.connect('baza.db')
cursor = conn.cursor()

current_date = datetime.date.today() #текущая дата и время
current_date = int(current_date.strftime("%d%m"))
#print(current_date)

#finally

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