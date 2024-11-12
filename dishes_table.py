# Таблица Телефоны и особые действия с ней.

from dbtable import *

class DishesTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "dishes"

    def columns(self):
        return {"category_id": ["integer", "REFERENCES categories(id)"],
                "name": ["varchar(128)", "NOT NULL"],
                "instruction": ["varchar(2056)", "NOT NULL"]}
    
    def primary_key(self):
        return ['category_id', 'name']

    def table_constraints(self):
        return ["PRIMARY KEY(category_id, name)"]

    def all_by_category_id(self, pid):
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE category_id = %s"
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, str(pid))
        return cur.fetchall()           

