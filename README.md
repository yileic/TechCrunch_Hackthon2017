# Surrounding Describer for Blind People

## What it does
This is a tool to help blind people know about their surrounding things by using a camera.
It has 3 major functions:
  1. read out text signs by pressing 'r'
    (example use case: the road signs in the street can be recognized by using this tool)
  2. describe what an object is by pressing 's'
    (example use case: an object that is far or not able to be recognized by touching can be described by using this tool)
  3. describe a person's facial expression, age and gender etc by pressing 's'
    (example use case: a person who is not talking may not be easily identified by a blind person, use this tool to describe that person)


## How we built it
We use amazon web serivce to do object/facial recognition and text-to-speec service to speak surrounding things to the users.  


## Challenges we ran into
We tried to detect the harzard surronding by the users and sent out the sms messages.  However, it will cost lots of time to train a new image harzard recognition model.


## Accomplishments that we're proud of
By using this project, we build eyes for blind people to understand more about the world. 


## What we learned
We learned how to use AMS service to upload S3 images and transformed those images into beautiful speech. 


## What's next for Surrounding Describer for Blind People
The blind people can conduct certain command when using this app. The image 
