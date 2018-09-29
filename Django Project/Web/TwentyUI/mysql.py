from django.db import connection

f, idex1 = True, ""; # Starting.html이 한번만 돌 수 있게 체크

def test_insert_data():
    sql = "INSERT INTO test1 (no, name, geo) VALUES('1', '파이썬에서 저장됨', '10.3')"
    print(sql)
    connection.cursor().execute(sql)

    connection.commit()
    print(connection.cursor().lastrowid)

def insert_data_boder(id1,date1,time1,title1,content1,email):
    sql = "INSERT INTO board (ID, DATE, TIME, Title, Content, Email) VALUES('"+ str(id1) \
          + "', '" + str(date1) + "', '" + str(time1) + "', '" + str(title1) + "', '" + str(content1) +"', '" + str(email)+ "')"

    print(sql)
    connection.cursor().execute(sql)

    connection.commit()

def insert_data_boder_comment(id1,date1,time1,content1, idx1):
    sql = "INSERT INTO board_coment (ID, DATE, TIME, Content, idx_Content) VALUES('"+ str(id1) + "', '" + str(date1) + "', '" + str(time1) + "', '" + str(content1) + "', '" + str(idx1)  + "')"

    print(sql)
    connection.cursor().execute(sql)

    connection.commit()

def select_data() :

    cursor = connection.cursor();
    sql = "select * from test1"
    cursor.execute(sql)
    context = []
    # 데이타 Fetch
    rows = cursor.fetchall()
    for row in rows :
        dic = {'no':row[0],'name':row[1],'geo':row[2]}
        context.append(dic)
    # print(rows)

    return context;

def select_login() :
    cursor = connection.cursor();
    sql = "select * from member"
    cursor.execute(sql)
    context = []
    rows = cursor.fetchall()
    for row in rows :
        dic = {'ID':row[0],'PW':row[1],'NAME':row[2]}
        context.append(dic)
    return context;

def select_eye_data_for_Starting(i) :
    global f, idex1;
    id1 = i
    if f:
        cursor = connection.cursor();
        sql = "select idx from eyesdata WHERE ID='"+id1+"'  ORDER BY idx DESC Limit 1"
        print(sql)
        cursor.execute(sql)
        context = []
        # 데이타 Fetch
        rows = cursor.fetchall()
        for n in rows :
            idex1 = str(n[0])
        f = False;
    cursor = connection.cursor();
    sql = "select DATE, TIME, COUNT from eyesdata WHERE ID='" + id1 + "' and idx >=" + idex1 + " ORDER BY idx DESC"
    print(sql)
    cursor.execute(sql)
    # 데이타 Fetch
    rows = cursor.fetchall()
    return rows;

def select_eye_data(id1) :
    cursor = connection.cursor();
    sql = "select DATE, TIME, COUNT from eyesdata WHERE ID='"+id1+"'"
    print(sql)
    cursor.execute(sql)
    context = []
    # 데이타 Fetch
    rows = cursor.fetchall()

    return rows;



def select_data_boradView() :
    cursor = connection.cursor();
    sql = "select idx ,ID ,DATE ,Title from board ORDER BY idx DESC"
    cursor.execute(sql)
    context = []
    # 데이타 Fetch
    rows = cursor.fetchall()
    for row in rows :
        dic = {'idx':row[0],'ID':row[1],'DATE':row[2],'Title':row[3]}
        context.append(dic)
    return context;

def select_data_boradView1(id1) :
    cursor = connection.cursor();
    sql = "select idx ,ID ,DATE ,Title from board WHERE ID='"+id1+"' ORDER BY idx DESC"
    cursor.execute(sql)
    # 데이타 Fetch
    rows = cursor.fetchall()

    return rows;


def select_data_boradRead(idx, name) :
    cursor = connection.cursor();
    sql = "select * from board where idx =" + str(idx)
    cursor.execute(sql)
    context = []
    # 데이타 Fetch
    rows = cursor.fetchall()
    idx_A,ID_A,DATE_A,TIME_A,Title_A, Content_A,Email_A = [],[],[],[],[],[],[];

    for row in rows :
        idx_A.append(row[0])
        ID_A.append(row[1])
        DATE_A.append(row[2])
        TIME_A.append(row[3])
        Title_A.append(row[4])
        Content_A.append(row[5])
        Email_A.append(row[7])

    dic = {'idx':idx_A,'ID':ID_A,'DATE':DATE_A, 'TIME':TIME_A, 'Title':Title_A, 'Content':Content_A, 'Email':Email_A, 'name' : name}
    context.append(dic)

    return context;



