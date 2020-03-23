import cx_Oracle
import json

class Connection:
    def __init__(self):
        login = 'c##u'
        passwd = 'c##u'
        ip = '127.0.0.1'
        port_ora = '1521'
        bd = 'xe'

        connstr = login + '/' + passwd + '@' + ip + ':' + port_ora + '/' + bd
        self.connection = cx_Oracle.connect(connstr, encoding='UTF-8', nencoding='UTF-8')


    def query_db(self, query, args=[]):
        cur = self.connection.cursor()
        cur.execute(query, args)
        r = [dict((cur.description[i][0], value) for i,value in enumerate(row)) for row in cur.fetchall()]
        cur.close()
        return r

    def merge_tbl(self, query, json_data):
        cur = self.connection.cursor()
        cur.prepare(query)
        cur.executemany(query, json.loads(json_data))
        self.connection.commit()
        cur.close()
