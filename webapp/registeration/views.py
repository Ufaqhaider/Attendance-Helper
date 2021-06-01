from .forms import SignUpForm
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .forms import  ContactForm
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pickle as pickle

def loginform(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username)
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('runmodel')
        else:
            messages.info(request, 'Username OR Password is incorrect')
    form={}
    return render(request,'login.html',form)

def index(request):
    return render(request,'index.html')


@login_required(login_url='login')

def runmodel(request):
    return render(request,'runmodel.html')

def record(request):
    import pyautogui
    import cv2
    import numpy as np
    import os
    from PIL import ImageGrab

    # Specify resolution
    Size = (ImageGrab.grab()).size

    # Specify video codec
    codec = cv2.VideoWriter_fourcc(*"XVID")

    # Specify name of Output file
    filename = "Record.mp4"

    # Specify frames rate. We can choose any
    # value and experiment with it
    fps = 5.0

    # Creating a VideoWriter object
    out = cv2.VideoWriter(filename, codec, fps, Size)

    # Create an Empty window
    cv2.namedWindow("Live", cv2.WINDOW_NORMAL)

    # Resize this window
    cv2.resizeWindow("Live", 480, 270)

    while True:
        # Take screenshot using PyAutoGUI
        # img = pyautogui.screenshot()

        # Convert the screenshot to a numpy array
        img = np.array(ImageGrab.grab())

        # Convert it from BGR(Blue, Green, Red) to
        # RGB(Red, Green, Blue)
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Write it to the output file
        out.write(img)

        # Optional: Display the recording screen
        cv2.imshow('Live', frame)

        # Stop recording when we press 'q'
        if cv2.waitKey(1) == ord('q'):
            break

    # Release the Video writer
    out.release()

    # Destroy all windows
    cv2.destroyAllWindows()
    return redirect('runmodel')

def save(request):
    path = r'C:\Users\syed zia haider\PycharmProjects\Django\webapp\face\imagesattendance'
    images = []
    classnames = []
    # imagesAttendance
    mylist = os.listdir(path)
    # print(mylist)

    for cl in mylist:
        currentImage = cv2.imread(f'{path}/{cl}')
        images.append(currentImage)
        classnames.append(os.path.splitext(cl)[0])
    print("classnames - ", classnames)

    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
            file = open(r'C:\Users\syed zia haider\PycharmProjects\Django\webapp\face\encoded.pickle', 'wb')
        pickle.dump(encodeList, file)
        file.close()
        encodeList = pickle.load(
            open(r'C:\Users\syed zia haider\PycharmProjects\Django\webapp\face\encoded.pickle', 'rb'))
        return encodeList

    def markAttendance(names):
        with open(r'C:\Users\syed zia haider\PycharmProjects\Django\webapp\face\Attendance file\Attendance_sheet.csv',
                  'r+') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
            if names not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%H:%S')
                f.writelines(f'\n{names},{dtString}')
            # print(myDataList)

    encodeListKnown = findEncodings(images)
    # print(len(encodeListKnown))
    print('Encoding Complete')

    cap = cv2.VideoCapture(r'C:\Users\syed zia haider\PycharmProjects\Django\webapp\Record.mp4')

    while True:
        success, img = cap.read()
        imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

        faces_current_frame = face_recognition.face_locations(imgs)
        encodecurrentframe = face_recognition.face_encodings(imgs, faces_current_frame)

        for encodeface, faceLoc in zip(encodecurrentframe, faces_current_frame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeface)
            face_dis = face_recognition.face_distance(encodeListKnown, encodeface)
            # print(face_dis)
            matchIndex = np.argmin(face_dis)

            if matches[matchIndex]:
                names = classnames[matchIndex].upper()
                print(names)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, names, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markAttendance(names)

        cv2.imshow('Video', img)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return redirect('index')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, 'admin@example.com', ['ufaqhaider674@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("index")

    form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('username')

            messages.success(request,'Account was created for '+ raw_password)
            # login user after signing up
            return redirect('login')

            # redirect user to home page
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


