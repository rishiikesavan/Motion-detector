import cv2, time, numpy, pandas
from datetime import datetime

first_frame = None

times = []
df = pandas.DataFrame(columns = ["Start", "End"])
prev_status = 0

video = cv2.VideoCapture(0)

while True:

    status = 0
    check, frame = video.read()

    color = frame.copy()
    color = numpy.flip(color, 1)
    color = numpy.array(color)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(frame, (21, 21), 0)
    frame = numpy.flip(frame, 1)

    if first_frame is None:
        first_frame = frame
        continue
    
    delta_frame = cv2.absdiff(first_frame, frame)
    thresh_frame = cv2.threshold(delta_frame, 20, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

    (cont, _) = cv2.findContours(thresh_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #contours_frame = frame.copy()
    #cv2.drawContours(contours_frame, cont, -1, (0, 255, 0), 3)
    for contours in cont:
        if cv2.contourArea(contours) < 10000:
            continue
        status = 1
        x, y, w, h = cv2.boundingRect(contours)
        cv2.rectangle(color, (x, y), (x + w, y + h), (0, 255, 0), 3)
    

    cv2.imshow("first frame", frame)
    cv2.imshow("delta frame", delta_frame)
    cv2.imshow("thresh frame", thresh_frame)
    cv2.imshow("color", color)
    #cv2.imshow("contours frame", contours_frame)

    key = cv2.waitKey(1)

    if prev_status == 0 and status == 1:
        times.append(datetime.now())
    if prev_status == 1 and status == 0:
        times.append(datetime.now())
    
    prev_status = status

    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break


for i in range(0, len(times), 2):
    df = df.append({"Start":times[i], "End": times[i + 1]}, ignore_index = True)

print(df)
df.to_csv("times.csv")

video.release()
cv2.destroyAllWindows()
