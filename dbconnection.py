# Установка соединения с базой данных
# (параметры передаются через класс конфиг).
import psycopg2

class DbConnection:

    def __init__(self, config):
        self.dbname = config.dbname
        self.user = config.user
        self.password = config.password
        self.host = config.host
        self.prefix = config.dbtableprefix
        self.conn = psycopg2.connect(dbname = self.dbname,
                                    user = self.user, 
                                    password = self.password,
                                    host = self.host)

    def __del__(self):
        if self.conn:
            self.conn.close()

    def test(self):
        cur = self.conn.cursor()
        cur.execute("DROP TABLE IF EXISTS test CASCADE")
        cur.execute("CREATE TABLE test(test integer)")
        cur.execute("INSERT INTO test(test) VALUES(1)")
        self.conn.commit()
        cur.execute("SELECT * FROM test")
        result = cur.fetchall()
        cur.execute("DROP TABLE test")
        self.conn.commit()
        return (result[0][0] == 1)
        

