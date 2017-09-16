# -*- coding: UTF-8 -*-
import numpy as np
import cv2
try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
import os
import json
import boto3
from botocore.client import Config
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import sys
import subprocess
from tempfile import gettempdir

polly = boto3.client('polly')
reko = boto3.client('rekognition')

ACCESS_KEY_ID = ''
ACCESS_SECRET_KEY = ''
BUCKET_NAME = 'ycai'

os.environ['AWS_ACCESS_KEY_ID']=ACCESS_KEY_ID
os.environ['AWS_SECRET_ACCESS_KEY']=ACCESS_SECRET_KEY

def upload_to_s3(img_name):
    data = open(img_name, 'rb')
    s3 = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        config=Config(signature_version='s3v4')
    )
    s3.Bucket(BUCKET_NAME).put_object(Key=img_name, Body=data)
    print ("Done uploading image to S3")

def label_detection(img_name):
    response = reko.detect_labels(Image={'S3Object':{'Bucket':BUCKET_NAME,'Name':img_name}},MinConfidence=75)
    print('Detected labels for ' + img_name)
    labels = []
    for label in response['Labels']:
        labels.append(label['Name'])
        print (label['Name'] + ' : ' + str(label['Confidence']))
    label_res = ''
    if len(labels) >= 2:
        label_res = labels[1]
    text = "There is a " + label_res
    return text, label_res

def face_detection(img_name):
    response = reko.detect_faces(Image={'S3Object':{'Bucket':BUCKET_NAME,'Name':img_name}},Attributes=['ALL'])
    print('Detected faces for ' + img_name)
    for faceDetail in response['FaceDetails']:
        if faceDetail is None:
            continue
        # get emotion
        emotion = ''
        if 'Emotions' in faceDetail:
            emotion = faceDetail['Emotions'][0]['Type']
        # get gender
        gender = ''
        if 'Gender' in faceDetail:
            gender = faceDetail['Gender']['Value']
        # get age
        age = ''
        if 'AgeRange' in faceDetail:
            age = 'between ' + str(faceDetail['AgeRange']['Low']) + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old'
        text = 'This is a %s %s %s ' % (emotion, gender, age)
        # print(json.dumps(faceDetail, indent=4, sort_keys=True))
        return text

def text_to_voice(text):
    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text=text, OutputFormat="mp3",
                                            VoiceId="Joanna")
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)

    # Access the audio stream from the response
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = os.path.join(gettempdir(), "speech.mp3")
            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                sys.exit(-1)
    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)

    # Play the audio using the platform's default player
    if sys.platform == "win32":
        os.startfile(output)
    else:
        # the following works on Mac and Linux. (Darwin = mac, xdg-open = linux).
        opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, output])


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    img_name = 'capture.png'

    while(True):
        # capture frame-by-frame
        ret, frame = cap.read()
        # add a rectangle area to place the target
        x1, y1, x2, y2 = 300, 100, 900, 600
        upper_left = (x1, y1)
        bottom_right = (x2, y2)
        frame = cv2.rectangle(frame, upper_left, bottom_right, (0,255,0), 5)
        # display the resulting frame
        cv2.imshow('frame',frame)
        key = cv2.waitKey(1) & 0xFF 
        # text reading mode
        if key == ord("r"):        
            saved_img = frame[y1:y2, x1:x2].copy()            
            cv2.imwrite(img_name, saved_img) 
            text = pytesseract.image_to_string(Image.open(img_name))  
            if text is not None and text.strip() != "":
               text_to_voice(text)        
            else:
                print 'no text detected'
        # object detection mode
        if key == ord("s"):        
            saved_img = frame[y1:y2, x1:x2].copy()            
            cv2.imwrite(img_name, saved_img) 
            upload_to_s3(img_name)
            text, label = label_detection(img_name)
            print 'label is: ' + label
            if label == 'Person' or label == 'People' or lable == 'Human':
                text = face_detection(img_name)
            if label != '':
                text_to_voice(text)
            
        # press 'q' to quit
        if key == ord('q'):
            break

    # when everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    # delete temp image file
    # os.remove(img_name)
