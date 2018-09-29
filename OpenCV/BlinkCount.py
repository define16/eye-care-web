import threading as thread;
import time;
import Project.OpenCV.mysql as db;

def StartThreading():
    global second, flag;
    flag = True;
    second =0;
    t = thread.Thread(target=Timer)
    t.start();

def Timer ():
    global second ,flag;
    check5min, sum, avg = 0, 0, 0.0;

    while True :
        while flag :
            if second < 60 and (check5min % 5 != 0 or check5min == 0):  # 1분
                second += 1;
                time.sleep(1);

            else :
                #db에 저장
                if check5min > 4 :
                    avg = sum / 5;
                    print("평균 눈깜빡임 : ", avg)

                    #현재 날짜와 시간
                    now = time.localtime()
                    nowdate = "%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday);
                    nowtime = "%02d:%02d:%02d" % (now.tm_hour, now.tm_min, now.tm_sec);
                    # DB에 저장
                    db.init()
                    db.insert_data(getName() ,nowdate ,nowtime ,avg); # def insert_data(id_, date_, time_, count_):

                    sum = 0;
                    check5min = -1;
                    setCount(0);

                sum += getCount();
                print("sum : ", sum)
                check5min += 1;
                second = 0;
                setCount(0);

def Pause() :
    global flag;
    flag = False;

def ReStart() :
    global flag;
    flag = True;


def getSecond() :
    global second;
    return second;

def setCount(cnt) :
    global count;
    count = cnt;

def getCount():
    global count;
    print("getcount : " , count);
    return count;

def setName(n) :
    global name;
    name = n;

def getName() :
    global name;
    return name;

