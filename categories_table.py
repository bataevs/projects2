# Таблица персоны и особые действия с ней

from dbtable import *

class CategoriesTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "categories"

    def columns(self):
        return {"id": ["serial", "PRIMARY KEY"],
                "name": ["varchar(128)", "NOT NULL"]
                }

    def find_by_position(self, num):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        sql += " LIMIT 1 OFFSET %(offset)s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"offset": num - 1})
        return cur.fetchone()       
    
