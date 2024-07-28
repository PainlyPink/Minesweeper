#sql connector
import mysql.connector as sqltor
mycon=sqltor.connect(host='localhost',user='root',passwd='1Azeez1234',database='csxiic')
if mycon.is_connected():
    print('Successfully connected to DataBase.')

                     