
import sqlite3
from loguru import logger

class SqlLite:
    
    @logger.catch
    def __init__(self, nameDB: str, tableQuery: str):
        self.conn = sqlite3.connect(nameDB)
        self.cur  = self.conn.cursor()
        self.cur.execute(tableQuery)
        self.conn.commit()
    
    @logger.catch
    def send_values(self, query, values):
        """
            [query]: str - Запрос 
            [values]: list - Данные в томже порядке что и в запросе 
        """
        strVal = "values("    
        for _ in range(len(values)):
                strVal += "?,"
        strVal = strVal[0: -1]
        strVal += ')'
        #strDuplucate = f'ON CONFLICT(id_user) UPDATE set payload = {values[1]}, goloss = {values[2]}'
        self.cur.execute(query + strVal, values)
        self.conn.commit()

    
    @logger.catch
    def send(self, query):
        self.cur.execute(query)
        self.conn.commit()
    
    @logger.catch
    def update(self, query):
        self.cur.execute(query)
        self.conn.commit()

    @logger.catch
    def isHe(self, value) -> bool:
        """Проверяет есть ли в базе строка с таким значение"""
        tempVal = self.get(f"select * from golos where id_user = {value}")
        if tempVal == []:
            return False
        else: 
            return True

    @logger.catch
    def get(self, query):
        a = self.conn.execute(query)
        return list(a)

    @logger.catch
    def get_last_payload(self, user_id) -> str:
        lastPayload = self.get(f"select payload from golos where id_user = {user_id}")
        return list(lastPayload)[0][0]

    def clear_column(self, nameTable):
        self.conn.execute(
        f"""
        DELETE FROM {nameTable} WHERE 1
        """)
   
