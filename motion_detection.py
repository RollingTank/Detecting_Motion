import cv2, time, pandas
from datetime import datetime
first_fr = None
video = cv2.VideoCapture(0)
stat_list = [None, None]
times = []
df = pandas.DataFrame(columns=["Start Time", "End Time"])
while True:
    check, frame = video.read()
    stat = 0
    gray_im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_im = cv2.GaussianBlur(gray_im, (21,21), 0)
    if first_fr is None:
        first_fr = gray_im
        continue

    delta_fr = cv2.absdiff(first_fr, gray_im)
    thresh_fr = cv2.threshold(delta_fr, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_fr = cv2.dilate(thresh_fr, None, iterations=2)
    (cnts,_) = cv2.findContours(thresh_fr.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for x in cnts:
        if cv2.contourArea(x) < 10000:
            continue
        stat = 1
        (a, b, w, h) = cv2.boundingRect(x)
        cv2.rectangle(frame, (a, b), (a+w, b+h), (0, 255, 0), 3)
    stat_list.append(stat)
    if stat_list[-1] ==  1 and stat_list[-2] == 0:
        times.append(datetime.now())
    if stat_list[-1] ==  0 and stat_list[-2] == 1:
        times.append(datetime.now())
    #cv2.imshow("Capture", gray_im)
    #cv2.imshow("T Frame", thresh_fr)
    cv2.imshow("Color Frame", frame)
    key = cv2.waitKey(1)
    #print(gray_im)
    if key == ord('q'):
        if stat == 1: 
            times.append(datetime.now())
        break
    print(stat)
    datetime.now()

for j in range(0, len(times), 2):
    df=df.append({"Start Time": times[j], "End Time": times[j+1]}, ignore_index=True)
df.to_csv("resources\Times.csv")
video.release()
cv2.destroyAllWindows
