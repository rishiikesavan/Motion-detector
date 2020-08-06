import cv2

img = cv2.imread("photo.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 127, 255, 0)[1]

cont, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

print(len(cont))

cv2.drawContours(img, cont, -1, (0, 255, 0), 3)

cv2.imshow("img", img)
cv2.imshow("gray", gray)
cv2.imshow("thresh", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()