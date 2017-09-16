# -*- coding: UTF-8 -*-
import boto3
from botocore.client import Config

img_name = 'capture.png'

ACCESS_KEY_ID = 'AKIAIWH2EOBTPPCFVZ2Q'
ACCESS_SECRET_KEY = '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'
BUCKET_NAME = 'ycai'

data = open(img_name, 'rb')

s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4')
)
s3.Bucket(BUCKET_NAME).put_object(Key=img_name, Body=data)
print ("Done uploading image to S3")

#--------------------------- label detection ------------------
fileName=img_name
bucket=BUCKET_NAME
client=boto3.client('rekognition')
response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':fileName}},MinConfidence=75)
print('Detected labels for ' + fileName)
labels = []
for label in response['Labels']:
	labels.append(label['Name'])
	print (label['Name'] + ' : ' + str(label['Confidence']))
label_res = labels[1]
text = "This is a " + label_res

#--------------------------- face detection -------------------
import json
response = client.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':fileName}},Attributes=['ALL'])
print('Detected faces for ' + fileName)
for faceDetail in response['FaceDetails']:
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
	text = 'This is a %s %s %s' % (emotion, gender, age)
	print(json.dumps(faceDetail, indent=4, sort_keys=True))

# read texts




#-------------------------- text to voice -----------------------
import os
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import sys
import subprocess
from tempfile import gettempdir


os.environ['AWS_ACCESS_KEY_ID']='AKIAIWH2EOBTPPCFVZ2Q'
os.environ['AWS_SECRET_ACCESS_KEY']='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'


polly = boto3.client('polly')
# test = polly.describe_voices()
# print test

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
    # Note: Closing the stream is important as the service throttles on the
    # number of parallel connections. Here we are using contextlib.closing to
    # ensure the close method of the stream object will be called automatically
    # at the end of the with statement's scope.
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
