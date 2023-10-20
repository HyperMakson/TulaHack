
import sqlite3 as sq
def sql_start():
    global base, cur
    base = sq.connect('baza.db')
    cur = base.cursor()
    if base:
        print("БД подключена успешно")

async def sql_add_(message):
    

