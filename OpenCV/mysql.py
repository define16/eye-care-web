import pymysql;

url = "localhost"
id='root'
password='20196637'
dbName='twenty'

def init():
    global db, cursor;
    db = pymysql.connect(host=url, port=3306, user=id, passwd=password, db=dbName, charset='utf8');
    cursor = db.cursor()

def insert_data(id_, date_, time_, count_):
    try:
        sql = "INSERT INTO eyesdata (ID, DATE, TIME, COUNT) VALUES('" + str(id_) \
              + "', '" + str(date_) +"', '" + str(time_) +"', '" + str(count_) + "')"
        print(sql)
        cursor.execute(sql)

        db.commit()
        print(cursor.lastrowid)
    finally:
        db.close();




