import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import trainer

def calculate_angle(a,b,c):
    a = np.array(a) 
    b = np.array(b) 
    c = np.array(c) 
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle


def record_curls():
    feedback = ""
    difference = 0
    curr = 0
    depth = []
    counter = 0 
    stage = None
    mp_pose = mp.solutions.pose

    cap = cv2.VideoCapture(1)

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        reader = pyttsx3.init()
        while cap.isOpened():
            ret, frame = cap.read()
            

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        

            results = pose.process(image)
        

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            

            try:
                landmarks = results.pose_landmarks.landmark
                

                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                angle = calculate_angle(shoulder, elbow, wrist)
                
                if angle > 150:
                    stage = "down"
                if angle < 50 and stage =='down':
                    stage="up"
                    counter +=1
                    curr = counter
                    print(counter)

                if stage == "down" and counter == curr:
                    depth.append(angle)
                else:
                    thisRep = abs(min(depth) - 80)
                    difference+=thisRep
                    depth = []
                    
                    if thisRep > 40:
                        reader.say("That was too low, fix that or you could get hurt!")
                    elif thisRep > 20:
                        reader.say("Close, a little too low!")
                    else:
                        reader.say("You're doing great, keep it up!")
                    reader.runAndWait()
                        
            except:
                pass        
            
            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    
    score = difference // counter


    advice = trainer.feedback(score)
    reader.say(advice)
    reader.runAndWait()

    return advice




def record_squats():
    feedback = ""
    difference = 0
    curr = 0
    depth = []
    counter = 0 
    stage = None
    mp_pose = mp.solutions.pose
    cap = cv2.VideoCapture(1)

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        reader = pyttsx3.init()
        while cap.isOpened():
            ret, frame = cap.read()
            
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark
                
                hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                angle = calculate_angle(hip, knee, ankle)
                
                
                if angle > 150:
                    stage = "up"
                if angle < 100 and stage =='up':
                    stage="down"
                    counter +=1
                    curr = counter

                if stage == "down" and counter == curr:
                    depth.append(angle)
                else:
                    thisRep = abs(min(depth) - 80)
                    difference+=thisRep
                    depth = []
                    
                    if thisRep > 40:
                        reader.say("That was too low, fix that or you could get hurt!")
                    elif thisRep > 20:
                        reader.say("Close, a little too low!")
                    else:
                        reader.say("You're doing great, keep it up!")
                    reader.runAndWait()
                        
            except:
                pass           
            
            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


    score = difference // counter


    advice = trainer.feedback(score)
    reader.say(advice)
    reader.runAndWait()

    return advice



def record_push_ups():
    feedback = ""
    difference = 0
    curr = 0
    depth = []
    counter = 0 
    stage = None
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    cap = cv2.VideoCapture(1)

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        reader = pyttsx3.init()
        while cap.isOpened():
            ret, frame = cap.read()
            

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        

            results = pose.process(image)
        

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            

            try:
                landmarks = results.pose_landmarks.landmark
                

                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                angle = calculate_angle(shoulder, elbow, wrist)
                
                if angle > 160:
                    stage = "up"
                if angle < 100 and stage =='up':
                    stage="down"
                    counter +=1
                    curr = counter

                if stage == "down" and counter == curr:
                    depth.append(angle)
                else:
                    thisRep = abs(min(depth) - 80)
                    difference+=thisRep
                    depth = []
                    
                    if thisRep > 40:
                        reader.say("That was too low, fix that or you could get hurt!")
                    elif thisRep > 20:
                        reader.say("Close, a little too low!")
                    else:
                        reader.say("You're doing great, keep it up!")
                    reader.runAndWait()
                        
            except:
                pass        
        

            cv2.imshow('Mediapipe Feed', image)
                          
        

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    

    score = difference // counter


    advice = trainer.feedback(score)
    reader.say(advice)
    reader.runAndWait()

    return advice

advice = record_curls()
print(advice)