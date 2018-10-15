import cv2;
import numpy as np;
import Project.OpenCV.BlinkCount as blink;
import sys
# C:/Users/User/Anaconda3/envs/py36_maanya/Library/etc/haarcascades/haarcascade_frontalface_alt.xml

def main(name) :
    global IsBlink, count
    IsBlink = False;
    count = 0;
    blink.setName(name)

    face_cascade = cv2.CascadeClassifier('C:/Users/User/Anaconda3/envs/py36_maanya/Library/etc/haarcascades/haarcascade_frontalface_alt2.xml');
    eye_cascade = cv2.CascadeClassifier('C:/Users/User/Anaconda3/envs/py36_maanya/Library/etc/haarcascades/haarcascade_eye.xml');

    if face_cascade.empty() :
        raise IOError('Unable to load the face cascade classifier xml file');
    if eye_cascade.empty() :
        raise IOError('Unable to load the eyes cascade classifier xml file');

    cap = cv2.VideoCapture(0); # 카메라 선택
    ds_factor = 1;
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    blink.setCount(0)
    blink.StartThreading();  # 타이머 시작

    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    out = cv2.VideoWriter('D:\TodayEyes.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))

    while True :
        ret, frame = cap.read();
        frame = cv2.resize(frame, None, fx=ds_factor, fy= ds_factor, interpolation=cv2.INTER_AREA);
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
        faces = face_cascade.detectMultiScale(gray, 1.1, 5, 0, (100, 100)) # 얼굴영역안에 눈이 있기 때문에 먼저 찾는다.
        '''
        CascadeClassifier의  detectMultiScale 함수에 grayscale 이미지를 입력하여 얼굴을 검출
        첫 번째 인자인 image는 바로 검출하고자 하는 원본 이미지를 의미
        두 번째 인자인 scaleFactor는 이미지 피라미드에서 사용되는 scale factor를 의미
        세 번쨰 인자인 minNeighbors는 이미지 피라미드에 의한 여러 스케일의 크기에서 minNeighbors 횟수 이상 검출된 object는 valid하게 검출
        네 번째 인자인 flags는 old cascade 사용시에만 의미를 가지는 파라미터
        다섯 번째 인자인 (minSize, MaxSize)
        '''

        if (np.size(faces) > 0):  # 벡터의 크기를 계산
            blink.ReStart();
            print("second : ", blink.getSecond())
            for (x,y,w,h) in faces :
                cv2.rectangle(frame,(x,y), (x+w,y+h),(0,0,255),3) # 사각형을 그림
                roi_gray = gray[y:y+h, x:x+w]; # 검출된 얼굴영역을 흑백으로 변환
                roi_color = frame[y:y+h, x:x+w] # 관심영역
                #print("x : " ,roi_color )
                lefteyes = eye_cascade.detectMultiScale(roi_gray, 1.5, 5, 0, (50, 50)); # 벡터 값을 변환

                # print("eyes : ",np.size(lefteyes))

                if(np.size(lefteyes) > 0) :  # 벡터의 크기(눈영역의 크기)를 계산
                    IsBlink = True; # 처음 시작할 때 눈의 영역이 검출되는 순간부터 시작하기 위해서 사용된 변수
                    for(x_eye, y_eye,w_eye,h_eye) in lefteyes :
                        center = (int(x_eye + 0.5*w_eye), int(y_eye + 0.5*h_eye));
                        radius = int(0.3 * (w_eye + h_eye));
                        color = (255, 0, 255);
                        thickness = 5;
                        cv2.circle(roi_color, center, radius, color, thickness); # 검출된 눈영역에 원을 그림
                else :
                    if IsBlink :
                        print("눈을 감았다")
                        count = blink.getCount() + 1;
                        blink.time.sleep(0.025);
                        blink.setCount(count)
                        print("count : " , blink.getCount())

        else :
            IsBlink = False;
            blink.Pause();


        cv2.imshow('Eye Detector', frame);  # 없애면 안뜬다.
        c = cv2.waitKey(1);

        if c == 27 :
            blink.Pause();
            break;

    cap.release();
    cv2.destroyAllWindows();


def resetCount() :
    global count;
    count = 0;

if __name__ == "__main__" :
    main(sys.argv[1]);
