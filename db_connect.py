
import sqlite3 

class dbworker:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()
    def user_exists(self, user_id):
        with self.connection:
            '''Проверка наличия пользователя в базе'''
            result = self.cursor.execute('SELECT * FROM `Users` WHERE `User_id` = ?', (user_id,)).fetchall()
            return bool(len(result))
    def add_user(self, user_id, user_fio, user_snils, user_polis):
        '''Добавление пользователя'''
        with self.connection:
            return self.cursor.execute('INSERT INTO `Users` (`User_id`, `User_fio`, `Snils`, `Polis`) VALUES(?,?,?,?)', (user_id, user_fio, user_snils, user_polis))
    def add_appoint(self, doc_fio, user_id, date, time):
        '''Добавление записи к врачу'''
        with self.connection:
            doc_id = self.cursor.execute('SELECT * FROM `Docs` WHERE `Doc_fio` = ?', (doc_fio,))
            return self.cursor.execute('INSERT INTO `Appoints` (`Doc_id`, `User_id`, `Date`, `Time`, `Tests`) VALUES(?,?,?,?,?)', (doc_id, user_id, date, time, 'expected'))
    def del_appoint(self, user_id, date, time):
        '''Удаление записи к врачу'''
        with self.connection:
            return self.cursor.execute('DELETE FROM `Appoints` WHERE `User_id` = ? AND `Date` = ? AND `Time` = ?',(user_id, date, time,))
    def get_all_appoints_user(self, user_id):
        '''Вывод всех записей пользователя'''
        with self.connection:
            return self.cursor.execute('SELECT * FROM `Appoints` WHERE `User_id` = ?', (user_id,)).fetchall()
    def get_all_docs(self):
        '''Вывод всех врачей'''
        with self.connection:
            return self.cursor.execute('SELECT `Doc_fio` FROM `Docs`').fetchall()
        
            
        
        
        
        
    

    

