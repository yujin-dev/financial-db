from psycopg2.extras import execute_values

class Ingestion:
    
    def __init__(self, conn, table_name, columns):
        """
            conn: psycopg2 connection object
        """
        self.conn = conn
        self.table_name = table_name
        self.columns = columns
         
    def _insert_values(self, data):
        if self.conn is not None:
            cursor = self.conn.cursor()
            sql = f"""
            INSERT INTO {self.table_name} ({','.join(self.columns)}) 
            VALUES %s;"""
            execute_values(cursor, sql, data)
            self.conn.commit()