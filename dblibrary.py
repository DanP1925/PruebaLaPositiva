import psycopg2
from datetime import datetime

class DbLibrary:

    conn = None

    def __init__(self):
        self.conn = psycopg2.connect(                                                
            dbname ='df1o3rgm7v9iro',                                           
            user='hfvqfbvdnwehlu',                                              
            password='15be2066cee0dd4fa30591b4887ee220528fa4b6a0ca23f09c36f2b089656130',
            host='ec2-54-204-46-236.compute-1.amazonaws.com',                   
            port='5432')         
    
    def close(self):
        self.conn.close()

    def isFirstTime(self, facebook_id):
        cur = self.conn.cursor()
        query = "SELECT * FROM account WHERE facebook_id = %s"
        data = (facebook_id, )
        cur.execute(query,data);

        if cur.fetchone() is not None:
            result = False
        else:
            result = True

        cur.close()
        return result

    def createNewAccount(self, facebook_id, created_time):
        cur = self.conn.cursor()
        query = "INSERT INTO account (facebook_id,created_at,last_access) VALUES (%s, %s, %s)"
        data = (facebook_id,
                datetime.fromtimestamp(created_time/1000.0),
                datetime.fromtimestamp(created_time/1000.0)) 
        cur.execute(query,data) 
        self.conn.commit()
        cur.close()
