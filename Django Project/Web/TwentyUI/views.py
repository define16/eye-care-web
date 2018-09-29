# Create your views here.

import os, time;
from django.shortcuts import render
from django.http import HttpResponse
from . import mysql as db;
from . import forms;

refreshCount = 0;
userId=""
userName=""

def index(request):
    setRefreshCount(0);
    return render(request,'TwentyUI/index.html')

def index_login(request):
    if getRefreshCount() == 1 :
        start_opencv('taskkill /f /im EyeTracker.exe');
        setRefreshCount(0);

    setRefreshCount(0);
    user = getUserName()
    return render(request,'TwentyUI/index_login.html', {'name' : user} )

def info(request):
    return render(request,'TwentyUI/info.html')

def join(request):
    return render(request,'TwentyUI/join.html')


def info_login(request):
    user = getUserName()
    return render(request,'TwentyUI/info_login.html', {'name' : user })

def Starting(request):
    if getRefreshCount() == 0 :
        start_opencv('start /d "D:\Programing Folder\Python\class\Project\OpenCV\dist" /b EyeTracker.exe');
        setRefreshCount(1);
    context = []
    tempId = getUserId()
    rows = db.select_eye_data_for_Starting(tempId);
    for row in rows :
        dic = {'DATE':row[0],'TIME':row[1],'COUNT':row[2]}
        context.append(dic)
    return render(request,'TwentyUI/Starting.html', {'contexts': context})


def boderView(request):
    context = db.select_data_boradView();
    return render(request,'TwentyUI/boderView.html', {'contexts':context})


def boderView_login(request):

    context = [];
    tempId = getUserName();
    rows = db.select_data_boradView1(tempId);
    for row in rows :
        dic = {'idx':row[0],'ID':row[1],'DATE':row[2],'Title':row[3], 'Name': tempId}
        context.append(dic)
    return render(request,'TwentyUI/boderView_login.html', {'contexts':context})

# url를 통해서 넘겨받은 변수 idx
def boderRead(request):
    idx = request.GET.get('idx') # ? 뒤 변수 넘겨줄때 사용 get방식
    tempId = getUserName()[0]
    context = db.select_data_boradRead(idx, tempId['NAME']);
    return render(request,'TwentyUI/boderRead.html', {'contexts':context})

def boderWrite(request):
    tempId = getUserName()
    return render(request,'TwentyUI/boderWrite.html', {'contexts':tempId})

def Login(request):
    return render(request,'TwentyUI/Login.html')

def MyPage(request):
    tempId = getUserId()
    rows = db.select_eye_data(tempId);
    context,date_A,time_A = [],[],[];
    total_count,total_cnt, total = 0,0,0.0;

    #시간 그래프
    for i in range(0, 25): #일자
        temp_cnt, cnt = 0, 0
        for row in rows :
            date_, time_, count_ = row[0], row[1], row[2];

            if date_ == getDate() :
                temp = int(time_.split(":")[0])
                if temp == i :
                    temp_cnt += count_;
                    cnt += 1;
                    total_count += count_;
                    total_cnt += 1;
        if cnt == 0 :
            time_A.append(0);
        else :
            time_A.append(temp_cnt/cnt);

    #월간 그래프
    for i in range(1,13) :
        temp_cnt, cnt = 0, 0
        for row in rows:
            date_, count_ = row[0], row[2];
            year = date_.split("-")[0]
            if year == getDate().split("-")[0]:
                temp = int(date_.split("-")[1])
                if temp == i:

                    temp_cnt += count_;
                    cnt += 1;

        if cnt == 0 :
            date_A.append(0);
        else :
            date_A.append(temp_cnt / cnt);

    # 현재까지 눈상태
    total = total_count / total_cnt;
    picture = ["very bad.png","bad.png","normal.png","good.png","very good.png"]
    if int(total) > 34 :
        pic = "static/images/" + picture[4];
        coment = "상태가 아주 좋아! 오늘 평균 눈깜빡임수 : " +  str(int(total)) + "회"
    elif int(total) < 35 and int(total)  > 24:
        pic = "static/images/" + picture[3];
        coment = "상태가 좋아! 오늘 평균 눈깜빡임수 : " +  str(int(total)) + "회"
    elif int(total)  < 25 and int(total)  > 15:
        pic = "static/images/" + picture[2] ;
        coment = "상태가 보통이야! 오늘 평균 눈깜빡임수 : " +  str(int(total)) + "회"
    elif int(total)  < 15 and int(total)  > 4:
        pic = "static/images/" + picture[1] ;
        coment = "상태가 나빠! 오늘 평균 눈깜빡임수 : " +  str(int(total)) + "회"
    else :
        pic = "static/images/" +  picture[0];
        coment = "상태가 아주 나빠! 오늘 평균 눈깜빡임수 : " +  str(int(total)) + "회"
    tempId = getUserName()
    dic = {'Month': date_A, 'Time': time_A,'Pic': pic, 'Coment': coment  ,'Name': tempId}
    context.append(dic)

    return render(request,'TwentyUI/MyPage.html',{'contexts':context})

def start_opencv(path):
    os.system(path)

def Write(request):
    if request.method == 'POST':
        form = forms.ContentForm(request.POST) #넘겨 받는다
        print(form);
        if form.is_valid(): # 데이터가 있는지 확인
            subject=form.data['subject']
            content=form.data['content']
            email=form.data['email']
            tempId = getUserName()[0];
            print(tempId['NAME'])
            db.insert_data_boder(tempId['NAME'],getDate(),getTime(),subject,content,email);
            context = db.select_data_boradView(tempId['NAME']);
            return render(request, 'TwentyUI/boderView_login.html', {'contexts': context})


def CheckIdPw(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST) #넘겨 받는다
        if form.is_valid(): # 데이터가 있는지 확인
            flag = False;
            id = form.data['id']
            pw = form.data['pw']

            context = db.select_login();
            for con in context :
                if con['ID'] == id and con['PW'] == pw :
                    flag = True;
                    setUserName(con['NAME']);
                    setUserId(con['ID']);

            if flag :
                return render(request, 'TwentyUI/index_login.html', {'name' : getUserName()})
            else :
                return HttpResponse('로그인 실패. 다시 시도 해보세요.')

        else :
            return HttpResponse('그냥 오류')


def setRefreshCount(cnt):
    global refreshCount;

    refreshCount= cnt;

def getRefreshCount() :
    global refreshCount
    return refreshCount;

def getDate() :
    now = time.localtime()
    nowdate = "%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday);
    return nowdate;

def getTime() :
    now = time.localtime()
    nowtime = "%02d:%02d:%02d" % (now.tm_hour, now.tm_min, now.tm_sec);
    return  nowtime;

def getUserName() :
    global userName;
    context = []
    dic = {'NAME': userName}
    context.append(dic)
    return context;

def setUserName(n) :
    global userName;
    userName = n;

def getUserId():
    global userId;
    return userId;

def setUserId(i) :
    global userId;
    userId = i;


################################################################################################################
# TEST
# def Test_eyesTracker(request):
#     # try:
#     #     return StreamingHttpResponse((VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
#     # except:  # This is bad! replace it with proper handling
#     #     pass
#     # t = thread.Thread(target=eye.main())
#     # t.start();
#     refresh_cnt = getRefreshCount()
#     if refresh_cnt == 0 :
#         # (C:\Users\User\Anaconda3\envs\py36_maanya) D:\Programing Folder\Python\class\Project\end>pyinstaller EyeTracker.py -F
#         start_opencv('start /d "D:\Programing Folder\Python\class\Project\end\dist" /b EyeTracker.exe');
#         setRefreshCount(1)
#
#     return render(request,'TwentyUI/eyes_tracker_test.html')


# def index(request):
#     context = db.select_data();
#
#     return render(request,'TwentyUI/index.html', {'context':context})

# def nextPage(request) :
#     context = db.select_data();
#
#     return render(request,'TwentyUI/nextPage.html')
#
#
# def Write_Comment1(request):
#     if request.method == 'POST':
#         print("1")
#         form = forms.CommentForm(request.POST) #넘겨 받는다
#         print(form)
#         print("1")
#         if form.is_valid(): # 데이터가 있는지 확인
#             print("5")
#             content = form.data['comment']
#             idx = form.data['idx1']
#             tempId = getUserName()[0];
#             print("1")
#             db.insert_data_boder_comment(tempId['NAME'],getDate(),getTime(),content,idx);
#             print("1")
#             context = db.select_data_boradRead(idx, tempId['NAME']);
#             url = 'TwentyUI/boderRead.html?idx=' + idx
#             return render(request, url, {'contexts': context})
#
#
# def form_test(request):
#     if request.method == 'POST':
#         form = forms.ContentForm(request.POST) #넘겨 받는다
#         if form.is_valid(): # 데이터가 있는지 확인
#             subject=form.data['subject']
#             content=form.data['content']
#             print(subject)
#             print(content)
#             db.insert_data_boder("id1",getDate(),getTime(),subject,content);
#             context = db.select_data_boradView();
#             return render(request, 'TwentyUI/boderView.html', {'contexts': context})
