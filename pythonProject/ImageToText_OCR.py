import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image = cv2.imread("ocr1.jpg")
grey = cv2.imread("ocr1.jpg", 0)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Threshold
threshold, binary_image = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
print(threshold)
config = "--psm 6"
text = pytesseract.image_to_string(binary_image, config=config)

print("Extracted Text: ")
print(text)

cv2.waitKey(0)
cv2.destroyAllWindows()
