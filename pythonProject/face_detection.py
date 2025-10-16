

#step 1:
# import cv2
#
#
# # Black and White (gray scale)
# Img = cv2.imread('bill.png', 1)
# # print(Img)
# # cv2.imshow('bill', Img)
# gray_img = cv2.cvtColor(Img, cv2.COLOR_BGR2GRAY)
# print(gray_img)
# cv2.imshow('gray_bill', gray_img)
# Img = cv2.imread('bill.png', 0)
# print(Img)
# cv2.imshow('bill', Img)
# cv2.waitKey(0)

#cv2.waitKey(2000)

# cv2.destroyAllWindows()

# #step 2:
# import cv2
#
# # Black and White (gray scale)
# img = cv2.imread('bill.png', 0)
# resized_image = cv2.resize(img, (650, 500))
# cv2.imshow('bill', resized_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#step 3:

import cv2

# Create a CascadeClassifier Object
face_cascade = cv2.CascadeClassifier('cascade_frontface_default.xml')

# Reading the image as it is
img = cv2.imread('1.png')
gray_img = cv2.imread("1.png", 0)
# Reading the image as gray scale image
# gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(gray_img)
cv2.imshow("gray_bill",gray_img)
# Search the co-ordintes of the image
faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.05, minNeighbors=5)
for x, y, w, h in faces:
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

resized = cv2.resize(img, (int(img.shape[1] / 2), int(img.shape[0] / 2)))

cv2.imshow("Gray", resized)

cv2.waitKey(0)

cv2.destroyAllWindows()