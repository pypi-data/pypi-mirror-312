import psycopg2
from psycopg2 import sql
import io




class Executor:
    # def __init__(self, dbname, user, password, host='localhost', port='5432'):
    def __init__(self, dsn: str):
        self.connection = None
        self.cursor = None
        # print({"dsn": dsn})
        try:
            # self.connection = psycopg2.connect(
            #     dbname=dbname,
            #     user=user,
            #     password=password,
            #     host=host,
            #     port=port
            # )
            self.connection = psycopg2.connect(dsn)
            self.cursor = self.connection.cursor()
            print("Подключение к базе данных успешно!!!")
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")

    def insert_data_with_copy(self, table_name, data):
        """
        Вставляет список словарей в указанную таблицу с использованием COPY.
        
        :param table_name: Название таблицы.
        :param data: Список словарей с данными для вставки.
        """
        import json
        import re
        import pandas as pd

        if not data:
            print("Нет данных для вставки.")
            return
        
        columns = data[0].keys()
        
        output = io.StringIO()

        # Выгружаем DataFrame в CSV формат в объект StringIO
        # TODO: заебался я через циклы сделать взял пандас и вроде заработало
        pd.DataFrame(data).to_csv(output, index=False, sep=',')


        # Создаем временный CSV-файл в памяти
        # output = io.StringIO()
        
        # Записываем данные в формате CSV
        # output.write(','.join(columns) + '\n')  # Заголовок
    
        # for record in data:
        #     row = []
        #     for col in columns:
        #         # if isinstance(record[col], str):
        #         #     # row.append(json.dumps(record[col], ensure_ascii=False))
        #         #     row.append(re.escape(record[col]))
        #         #     continue

        #         if record[col] is None:
        #             row.append('')
        #             continue
        #         row.append(str(record[col]))
        #     row = ','.join(row) + '\n'
        #     output.write(row)
            # print(row)



        # Сбросим указатель на начало потока
        output.seek(0)

        # Используем COPY для вставки данных с f-строкой и двойными кавычками для колонок
        try:
            column_list = ', '.join(f'"{col}"' for col in columns)  # Оборачиваем названия колонок в двойные кавычки
            copy_query = f'COPY {table_name} ({column_list}) FROM STDIN WITH CSV HEADER'
            self.cursor.copy_expert(copy_query, output)
            # self.connection.commit()
            print(f'НЕ ЗАБУДЬ ЗАКОММИТИТЬ вставленные {len(data)} записей в таблицу "{table_name}" с использованием COPY.')
        except Exception as e:
            error_msg = f'Ошибка при вставке данных: {e}'
            self.connection.rollback()
            raise Exception(error_msg)

    def execute_query(self, query):
        """
        Выполняет произвольный SQL-запрос.
        
        :param query: SQL-запрос для выполнения.
        :return: Результат запроса (если есть).
        """
        try:
            self.cursor.execute(query)
            if query.strip().lower().startswith("select"):
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                print("Запрос выполнен успешно.")
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
            self.connection.rollback()

    def close(self):
        """Закрывает соединение с базой данных."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Соединение с базой данных закрыто.")

# Пример использования
if __name__ == "__main__":
    db = Executor(dbname='your_db', user='your_user', password='your_password')

    # Вставка данных с использованием COPY
    data_to_insert = [
        {'column1': 'value1', 'column2': 'value2'},
        {'column1': 'value3', 'column2': 'value4'}
    ]
    db.insert_data_with_copy('your_table', data_to_insert)

    # Выполнение запроса
    result = db.execute_query('SELECT * FROM your_table')
    print(result)

    # Закрытие соединения
    db.close()