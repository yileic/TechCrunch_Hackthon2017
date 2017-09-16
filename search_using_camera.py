# -*- coding: UTF-8 -*-
import numpy as np
import cv2
try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
import webbrowser
import os

# def process_img(img):
#     img_final = img.copy()
#     img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     ret, mask = cv2.threshold(img2gray, 180, 255, cv2.THRESH_BINARY)
#     image_final = cv2.bitwise_and(img2gray, img2gray, mask=mask)
#     ret, new_img = cv2.threshold(image_final, 180, 255, cv2.THRESH_BINARY_INV)
#     return new_img

cap = cv2.VideoCapture(0)
img_name = 'capture.png'

while(True):
    # capture frame-by-frame
    ret, frame = cap.read()
    # add a rectangle area to place the target text
    x1, y1, x2, y2 = 300, 300, 900, 500
    upper_left = (x1, y1)
    bottom_right = (x2, y2)
    # frame = cv2.rectangle(frame, upper_left, bottom_right, (0,255,0), 5)
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # frame = cv2.putText(frame, 'Place text inside the box and press \'s\'', 
    					# (300, 280), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)  
    # display the resulting frame
    cv2.imshow('frame',frame)

    key = cv2.waitKey(1) & 0xFF 
    # press 's' to save the image
    if key == ord("s"):
        
        saved_img = frame.copy()
        
        cv2.imwrite(img_name, saved_img) 
        text = pytesseract.image_to_string(Image.open(img_name))  
        if text is not None and text.strip() != "":
            text='+'.join(text.split())
            url = 'https://www.google.com/search?source=hp&q='+text
            try:
                webbrowser.open(url, new=2) 
            except UnicodeEncodeError:
                print 'url is: ' + url
        else:
            print 'no text detected'
    
    # press 'q' to quit
    if key == ord('q'):
        break

# when everything done, release the capture
cap.release()
cv2.destroyAllWindows()

# delete temp image file
# os.remove(img_name)

