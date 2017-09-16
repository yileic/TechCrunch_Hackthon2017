# Surrounding Describer for Blind People

## What it does
This is a tool to help blind people know about their surrounding things by using a camera.
It has 3 major functions:
  1. read out text signs by pressing 'r'
    (example use case: the street signs can be recognized by using this tool)
  2. describe what an object is by pressing 's'
    (example use case: an object that is far or not able to be recognized by touching can be described by using this tool)
  3. describe a person's facial expression, age and gender etc by pressing 's'
    (example use case: a person who is not talking may not be easily identified by a blind person, use this tool to describe that person)


## How we built it
We used Amazon Rekognition API to do image analysis, Polly API to transform text to speech, opencv and pytesseract to do text detection. 


## Challenges we ran into
The Rekognition API does not have text recognition function, thus to be able to read out detected text in the surroundings, we used opencv and pytesseract libs. We encountered some difficulties using a local image in Rekognition, thus we use scripts to upload it to amazon S3 first and then do recognition to bypass using local images directly. The detection accuracy is not very good due to background noises, so we added a rectangle in the camera vision to get a focused area.


## What's next for Surrounding Describer for Blind People
The blind people can conduct certain commands when using this app. For example, when dangerous situation is detected, make a call.
