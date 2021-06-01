import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pickle as pickle

path=r'C:\Users\syed zia haider\PycharmProjects\Django\webapp\face\imagesattendance'
images = []
classnames=[]
# imagesAttendance
mylist = os.listdir(path)
#print(mylist)

for cl in mylist:
    currentImage = cv2.imread(f'{path}/{cl }')
    images.append(currentImage)
    classnames.append(os.path.splitext(cl)[0])
print("classnames - ",classnames)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
        file = open(r'C:\Users\syed zia haider\PycharmProjects\Django\webapp\face\encoded.pickle','wb')
    pickle.dump(encodeList,file)
    file.close()
    encodeList = pickle.load(open(r'C:\Users\syed zia haider\PycharmProjects\Django\webapp\face\encoded.pickle','rb'))
    return encodeList


def markAttendance(names):
    with open(r'C:\Users\syed zia haider\PycharmProjects\Django\webapp\face\Attendance file\Attendance_sheet.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if names not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%H:%S')
            f.writelines(f'\n{names},{dtString}')
        #print(myDataList)


encodeListKnown = findEncodings(images)
#print(len(encodeListKnown))
print('Encoding Complete')


cap = cv2.VideoCapture(r'C:\Users\syed zia haider\PycharmProjects\Django\webapp\face\Program_file\Record.mp4')

while True:
    success, img = cap.read()
    imgs = cv2.resize(img,(0,0),None,0.25,0.25)
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

    faces_current_frame = face_recognition.face_locations(imgs)
    encodecurrentframe = face_recognition.face_encodings(imgs,faces_current_frame)

    for encodeface, faceLoc in zip(encodecurrentframe, faces_current_frame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeface)
        face_dis = face_recognition.face_distance(encodeListKnown, encodeface)
        #print(face_dis)
        matchIndex = np.argmin(face_dis)

        if matches[matchIndex]:
            names  = classnames[matchIndex].upper()
            print(names)
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,names,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(names)

    cv2.imshow('Video',img)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
