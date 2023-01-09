import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from detect_mask_video import detect_and_predict_mask,getNet
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import os
from sms import sendMessage

path = '.\\Face\\Face-Mask-Detection\\' + 'imagesFile'
# testing data set
images = []
classNames = []

myList = os.listdir(path)
# print(myList)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
# print(classNames)

# image encoding 
def findEncodings(images):
    encodeList = []
    # print(images)
    for img in images:
        # print("+++++",img)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def markAttendance(name,mask = False):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        # print(myDataList)
        nameList = []
        for line in myDataList:
            # print(line)
            entry = line.split(',')
            # print(entry)
            if entry[0] not in nameList:
                nameList.append(entry[0])
            # print(nameList)
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString},{"with Mask" if mask else"Not Wear Mask"}')



encodeListKnown = findEncodings(images)


def main():
    faceNet , maskNet = getNet()
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()

    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = vs.read()

        imgS = cv2.resize(frame,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

        frame = imutils.resize(frame, width=400)

        # detect faces in the frame and determine if they are wearing a
        # face mask or not
        (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

        # loop over the detected face locations and their corresponding
        # locations
        label = "Not Wearing mask"
        for (box, pred) in zip(locs, preds):
            # unpack the bounding box and predictions
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred

            # determine the class label and color we'll use to draw
            # the bounding box and text
            label = "Wearing Mask" if mask > withoutMask else "Not Wearing Mask"
            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

            # include the probability in the label
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

            # display the label and bounding box rectangle on the output
            # frame
            cv2.putText(frame, label, (startX, startY - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame =face_recognition.face_encodings(imgS,facesCurFrame)

        for encodeFace , faceLoc in zip(encodesCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)

            matchIndex = np.argmin(faceDis)
            # print(faceDis)
            # print("------",matchIndex)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                # if name not in allDetectedSoFar:
                #     print(name,time.time(),label)
                #     allDetectedSoFar.add(name)

                if name == 'AKHI PIC':
                    sendMessage("Akhiles",7301222745,{
                         'days' : 23, 'presence' : 76,
                         })

                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4 ,x2*4,y2*4,x1*4
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markAttendance(name,pred[0] > pred[1])
                print(name)
        # show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()

main()