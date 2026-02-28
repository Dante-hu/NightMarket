import sqlite3

class SQL_DB:
    def __init__(self, path="./", db_name='default'):
        """Initialize database connection and create core tables.
        
        Args:
            path: Directory path for database file
            db_name: Database filename without extension
            mode: Mode options for testing and prod
        """
        self.db_path = path + db_name + ".db"
        

    # NEW: thread-safe connection creator
    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_table(self, table_name, table_columns):
        """Create table with specified columns if it doesn't exist.
        
        Args:
            table_name: Name of table to create
            table_columns: SQL column definitions string
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        command = "CREATE TABLE IF NOT EXISTS %s (%s)" % (table_name, table_columns)
        cursor.execute(command)
        conn.commit()
        conn.close()

    def insert(self, table_name, data_list):
        """Insert data into specified table with parameterized queries.
        
        Args:
            table_name: Target table name for insertion
            data_list: List of dictionaries containing field-value pairs
        """
        try:
            if not data_list:
                return
            
            columns = list(data_list[0].keys())
            placeholders = ', '.join(['?' for _ in columns])
            column_names = ', '.join(columns)
            query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"

            conn = self.get_connection()
            cursor = conn.cursor()

            for data in data_list:
                values = [data[col] for col in columns]
                cursor.execute(query, values)
            
            conn.commit()
            conn.close()
            print(f"Successfully inserted {len(data_list)} records into {table_name}")
            
        except Exception as e:
            print(f"Error inserting into {table_name}: {e}")
            print(f"Data that failed: {data_list}")
    
    def get_table(self, table_name):
        """Check if table exists in database.
        
        Args:
            table_name: Name of table to check
            
        Returns:
            List containing table information if exists, empty list otherwise
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        command = "SELECT name FROM sqlite_master WHERE name='%s'" % table_name
        res = cursor.execute(command)
        table_list = res.fetchall()
        conn.close()
        return table_list

    def get_data(self, command):
        conn = self.get_connection()
        cursor = conn.cursor()
        res = cursor.execute(command)
        data = res.fetchall()
        conn.close()
        return data
