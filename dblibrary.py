from datetime import datetime
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
                self.convertFbTimestampToDate(created_time),
                self.convertFbTimestampToDate(created_time)) 
        cur.execute(query,data) 
        self.conn.commit()
        cur.close()

    def convertFbTimestampToDate(self,timestamp):
        return datetime.fromtimestamp(timestamp/1000.0)

    def getAccountId(self, facebook_id):
        cur = self.conn.cursor()
        query = "SELECT id FROM account WHERE facebook_id = %s"
        data = (facebook_id, )
        cur.execute(query,data) 
        account_id = cur.fetchone()
        cur.close()
        return account_id

    def storeMessage(self, facebook_id, messageText, created_time): 
        account_id = self.getAccountId(facebook_id)
        cur = self.conn.cursor()
        query = "INSERT INTO message (account_id,body,send_at) VALUES (%s, %s, %s)"
        data = (account_id, messageText,
                self.convertFbTimestampToDate(created_time))
        cur.execute(query,data) 
        self.conn.commit()
        cur.close()

    def updateConversationState(self, facebook_id, state):
        account_id = self.getAccountId(facebook_id)
        cur = self.conn.cursor()
        query = "UPDATE account SET conversation_state = %s WHERE id = %s"
        data = (state, account_id)
        cur.execute(query,data) 
        self.conn.commit()
        cur.close()

    def getConversationState(self, facebook_id):
        cur = self.conn.cursor()
        query = "SELECT conversation_state FROM account WHERE facebook_id = %s"
        data = (facebook_id, )
        cur.execute(query,data) 
        conversation_state = cur.fetchone()[0]
        cur.close()
        return conversation_state

    def storeSong(self,title, author, track_id, facebook_id,created_time):
        account_id = self.getAccountId(facebook_id)
        cur = self.conn.cursor()
        query = "INSERT INTO song (account_id, track_id, title, author, created_at) VALUES (%s, %s, %s, %s, %s)"
        data = (account_id, track_id,
                title, author, self.convertFbTimestampToDate(created_time))
        cur.execute(query,data) 
        self.conn.commit()
        cur.close()


    def getNumberOfUsers(self):
        cur = self.conn.cursor()
        query = "SELECT count(id) FROM account"
        cur.execute(query) 
        result = cur.fetchone()[0]
        cur.close()
        return result

    def getMessageNumberPerDay(self):
        cur = self.conn.cursor()
        query = "select count(account.id), date_trunc('day', message.send_at) as daySent from account inner join message on account.id = message.account_id group by daySent order by daysent desc limit 10"
        cur.execute(query) 
        result = cur.fetchall()
        cur.close()
        return result
