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
            print(doc_fio)
            res = self.cursor.execute('SELECT `Doc_id` FROM `Docs` WHERE `Doc_fio` = ?', (doc_fio,)).fetchall()
            print(res)
            arr = []
            for row in res:
                arr.append(row[0])
            doc_id = arr[0]
            print(doc_id)
            return self.cursor.execute('INSERT INTO `Appoints` (`Doc_id`, `User_id`, `Date`, `Time`, `Tests`) VALUES(?,?,?,?,?)', (doc_id, user_id, date, time, 'expected'))
    def del_appoint(self, user_id, date, time):
        '''Удаление записи к врачу'''
        with self.connection:
            return self.cursor.execute('DELETE FROM `Appoints` WHERE `User_id` = ? AND `Date` = ? AND `Time` = ?', (user_id, date, time,))
    def get_all_appoints_user(self, user_id):
        '''Вывод всех записей пользователя '''
        with self.connection:
            res = self.cursor.execute('SELECT * FROM `Appoints` WHERE `User_id` = ?', (user_id,)).fetchall()
            arr = []
            arr1 = []
            for row in res:
                arr.append(row[0])
                arr.append(row[1])
                arr.append(row[2])
                arr.append(row[3])
                arr.append(row[4])
                arr1.append(arr)
                arr = []
        return arr1
    def get_all_docs(self, spec_name):
        
        '''Получение всех врачей заданых по заданной специальности'''
        
        with self.connection:
            res = self.cursor.execute('SELECT `Spec_id` FROM `Specs` WHERE `Spec_name` = ?', (spec_name,))
            res = self.cursor.execute('SELECT `Doc_fio` FROM `Docs`').fetchall()
            arr = []
            for row in res:
                arr.append(row[0])
            return arr
    def get_user(self, user_id):
        '''Получение данных о пользователе'''
        
        with self.connection:
            res = self.cursor.execute('SELECT `User_fio`, `Snils`, `Polis` FROM `Users` WHERE `User_id` = ?', (user_id,)).fetchone()
            user_fio = res[0]
            snils = res[1]
            polis = res[2]
        return user_fio, snils, polis
    def select_symptom(self):
        '''Получение всех симптомов'''
        with self.connection:
            res = self.cursor.execute('SELECT `Symptom` FROM `Symptoms`').fetchall()
            arr = []
            for row in res:
                arr.append(row[0])
            return arr
    def select_id(self, symp):
        '''Получение всех симптомов'''
        with self.connection:
            res = self.cursor.execute('SELECT `Spec_id` FROM `Symptoms` WHERE `Symptom` = ?', (symp,)).fetchall()
            arr = []
            for row in res:
                arr.append(row[0])
            return arr
    def find_specialist_for_symptom(self, id_sympt):
        '''Получение всех симптомов'''
        with self.connection:
            res = self.cursor.execute('SELECT `Spec_name` FROM `Specs` WHERE `Spec_id` = ?', (id_sympt,)).fetchall()
            arr = []
            for row in res:
                arr.append(row[0])
            return arr
    def get_time_date(self, date):
        with self.connection:
            res = self.cursor.execute('SELECT `Time` FROM `Appoints` WHERE `Date` = ?', (date,)).fetchall()
            arr = []
            for row in res:
                arr.append(row[0])
            return arr
















        
        
        
    

    

