import mysql.connector

class sql:
    def __init__(self) -> None:
        with open('info.txt', 'r') as f:
            user, pwd, db = (i.strip() for i in f.readlines())

        self.mycon = mysql.connector.connect(host='localhost', user=user, passwd=pwd, database=db)

        if not self.mycon.is_connected():
            print("Error while performing MySQL connection.")
            exit()

        self.table = db + '_tbl'
        self.mycur = self.mycon.cursor()
    
    def save(self, win: str, time: str):
        # Use parameterized queries to prevent SQL injection
        query = "INSERT INTO hat_tbl (win, time) VALUES (%s, %s)"
        self.mycur.execute(query, (win, time))
        self.mycon.commit()

sql().save('N', '00:00:19')
