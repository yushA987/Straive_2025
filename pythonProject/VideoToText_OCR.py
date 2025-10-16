import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

cap = cv2.VideoCapture("sample_video.avi")

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    config = "--psm 6"  # Suitable for detecting block of text
    text = pytesseract.image_to_string(binary_image, config=config)

    if text.strip():  # Check if text is detected
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the frame with OCR text
    cv2.imshow("Text Detection", frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
