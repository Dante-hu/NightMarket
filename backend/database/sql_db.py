import sqlite3
import os

class SQL_DB:
    def __init__(self, path="./", db_name='default', db_url=None):
        """
        Initialize database connection.
        If db_url is provided, it connects to PostgreSQL (Supabase).
        Otherwise, it connects to local SQLite.
        """
        self.db_url = db_url
        self.db_path = os.path.join(path, f"{db_name}.db")
        self.is_postgres = db_url is not None

    def get_connection(self):
        if self.is_postgres:
            import psycopg2
            # Use the connection string from Render/Supabase
            return psycopg2.connect(self.db_url)
        else:
            return sqlite3.connect(self.db_path)

    def get_placeholder(self):
        """Postgres uses %s, SQLite uses ?"""
        return "%s" if self.is_postgres else "?"

    def create_table(self, table_name, table_columns):
        conn = self.get_connection()
        cursor = conn.cursor()
        command = f"CREATE TABLE IF NOT EXISTS {table_name} ({table_columns})"
        cursor.execute(command)
        conn.commit()
        conn.close()

    def insert(self, table_name, data_list):
        if not data_list:
            return
        
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            columns = list(data_list[0].keys())
            placeholder = self.get_placeholder()
            placeholders = ', '.join([placeholder for _ in columns])
            column_names = ', '.join(columns)
            
            query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"

            for data in data_list:
                values = [data[col] for col in columns]
                cursor.execute(query, values)
            
            conn.commit()
            conn.close()
            print(f"Successfully inserted {len(data_list)} records into {table_name}")
        except Exception as e:
            print(f"Error inserting into {table_name}: {e}")

    def get_data(self, command):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        conn.close()
        return data

    def update(self, table_name, data, where_clause, params=None):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            placeholder = self.get_placeholder()
            
            # Replace '?' with '%s' if we are in Postgres mode
            if self.is_postgres:
                where_clause = where_clause.replace('?', '%s')
                
            set_clause = ', '.join([f"{key} = {placeholder}" for key in data.keys()])
            query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
            
            values = list(data.values()) + list(params or ())
            cursor.execute(query, values)
            conn.commit()
            affected = cursor.rowcount
            conn.close()
            return affected
        except Exception as e:
            print(f"Error updating {table_name}: {e}")
            return 0