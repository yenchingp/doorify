import time
import cv2
from twilio.rest import Client

account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# To capture video from webcam.
cap = cv2.VideoCapture(0)
# To use a video file as input
# cap = cv2.VideoCapture('filename.mp4')

detect_once = False

while True:
    # Read the frame
    _, img = cap.read()
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 10)
    
    # If it is not a false positive
    if (len(faces) > 0) & (detect_once is True):
        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.imshow('img', img)
        # Send message
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body='Someone is at the door.',
            meida_url='',
            to='whatsapp:+6591465989'
        )
        print(message.sid)
        time.sleep(60)
        detect_once = False
        
    # If it may be a false positive
    elif (len(faces) > 0) & (detect_once is False):
        detect_once = True
        
    # Display view
    cv2.imshow('img', img)
    
    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break
        
# Release the VideoCapture object
cap.release()
