import psycopg2

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
        cur.execute("SELECT * " +
                    "FROM account " +
                    "WHERE facebook_id = %s" % facebook_id);

        if cur.fetchone() is not None:
            result = False
        else:
            result = True

        cur.close()
        return result

    def createNewAccount(self, facebook_id, created_time):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO account (facebook_id,created_at,last_access) " +
                    "VALUES (%s, %s, $s)" % (facebook_id,created_time,created_time))  
        self.conn.commit()
        cur.close()