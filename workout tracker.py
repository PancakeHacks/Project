import pygame
import sys
import cv2
import mediapipe as mp
import pyttsx3
import numpy as np
import trainer

# Initializing pygame
pygame.init()

# Defining size of game window
window_size = (900, 700)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Score Tracker with Workouts and Rewards")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
grey = (100, 100, 100)

# Fonts
font = pygame.font.Font(None, 48)  # Adjusted font size for title
small_font = pygame.font.Font(None, 24)  # Adjusted font size for small text
input_font = pygame.font.Font(None, 20)  # Adjusted font size for input text

# Workouts list
workouts = [
    "Squat",
    "Push Ups",
    "Curl"
]

last_click = ""

# Checkbox class to handle individual checkboxes
class Checkbox:
    global last_click
    def __init__(self, x, y, size, text):
        self.rect = pygame.Rect(x, y, size, size)
        self.checked = False
        self.text = text

    def draw(self, win):
        if self.checked:
            pygame.draw.rect(win, green, self.rect)
        else:
            pygame.draw.rect(win, red, self.rect, 2)
        
        # Render workout text
        text_surface = small_font.render(self.text, True, white)
        text_rect = text_surface.get_rect()
        text_rect.midleft = (self.rect.right + 10, self.rect.centery)
        win.blit(text_surface, text_rect)

    def click(self, pos):
        last_click = self.text
        if self.rect.collidepoint(pos):
            self.checked = not self.checked
            if self.checked:
                # Increase score when checkbox is checked
                increase_score(2)  # Adjust score increase amount as needed

# Initialize checkboxes for workouts
checkboxes = []
for index, workout in enumerate(workouts):
    checkbox = Checkbox(50, 100 + index * 50, 20, workout)  # Adjusted vertical positioning
    checkboxes.append(checkbox)

# Rewards input
reward_input = ""
input_active = False

# Rewards list
rewards = []

# Points and exchange rate
points = 0
exchange_rate = 2  # 2 points per reward

# Function to increase score
def increase_score(amount):
    global points
    points += amount


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
            
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark
                
                hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                angle = calculate_angle(hip, knee, ankle)
                
                if angle > 150:
                    stage = "up"
                if angle < 100 and stage == 'up':
                    stage = "down"
                    counter += 1
                    curr = counter

                if stage == "down" and counter == curr:
                    depth.append(angle)
                else:
                    thisRep = abs(min(depth) - 80)
                    difference += thisRep
                    depth = []

                    if thisRep > 40:
                        reader.say("That was too low, fix that or you could get hurt!")
                    elif thisRep > 20:
                        reader.say("Close, a little too low!")
                    else:
                        reader.say("You're doing great, keep it up!")
                    reader.runAndWait()

            except Exception as e:
                print(f"Error in squats: {e}")

            # Yield the frame for integration with Pygame
            yield image

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
    
    mp_pose = mp.solutions.pose
    cap = cv2.VideoCapture(1)

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        reader = pyttsx3.init()
        while cap.isOpened():
            ret, frame = cap.read()
            
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark

                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                angle = calculate_angle(shoulder, elbow, wrist)

                if angle > 160:
                    stage = "up"
                if angle < 100 and stage == 'up':
                    stage = "down"
                    counter += 1
                    curr = counter

                if stage == "down" and counter == curr:
                    depth.append(angle)
                else:
                    thisRep = abs(min(depth) - 80)
                    difference += thisRep
                    depth = []

                    if thisRep > 40:
                        reader.say("That was too low, fix that or you could get hurt!")
                    elif thisRep > 20:
                        reader.say("Close, a little too low!")
                    else:
                        reader.say("You're doing great, keep it up!")
                    reader.runAndWait()

            except Exception as e:
                print(f"Error in push-ups: {e}")

            # Yield the frame for integration with Pygame
            yield image

        cap.release()
        cv2.destroyAllWindows()

    score = difference // counter
    advice = trainer.feedback(score)
    reader.say(advice)
    reader.runAndWait()

    return advice




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
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark

                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                angle = calculate_angle(shoulder, elbow, wrist)

                if angle > 150:
                    stage = "down"
                if angle < 50 and stage == 'down':
                    stage = "up"
                    counter += 1
                    curr = counter
                    print(counter)

                if stage == "down" and counter == curr:
                    depth.append(angle)
                else:
                    thisRep = abs(min(depth) - 80)
                    difference += thisRep
                    depth = []

                    if thisRep > 40:
                        reader.say("That was too low, fix that or you could get hurt!")
                    elif thisRep > 20:
                        reader.say("Close, a little too low!")
                    else:
                        reader.say("You're doing great, keep it up!")
                    reader.runAndWait()

            except Exception as e:
                print(e)

            yield image

        cap.release()
        cv2.destroyAllWindows()

    score = difference // counter
    advice = trainer.feedback(score)
    reader.say(advice)
    reader.runAndWait()

    return advice



def calculate_angle(a, b, c):
    a = np.array(a)  # First point
    b = np.array(b)  # Mid point
    c = np.array(c)  # End point

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

def main():
    global reward_input, input_active, points, last_click

    clock = pygame.time.Clock()
    run_game = True

    # Initialize the generator for recording curls
    if last_click == "Squat":
        workout = record_squats()
    elif last_click == "Push Ups":
        workout = record_push_ups()
    elif last_click == "Curl":
        workout = record_curls()
    else:
        workout = None

    while run_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if clicking on checkboxes
                for checkbox in checkboxes:
                    checkbox.click(mouse_pos)
                # Check if clicking on reward
                for reward in rewards:
                    if reward["rect"].collidepoint(mouse_pos):
                        if points >= reward["points"]:
                            points -= reward["points"]
                            rewards.remove(reward)  # Remove reward from list
                            break  # Exit loop after one reward is clicked

                # Check if clicking on reward input box
                if box_width + gap_size + 50 <= mouse_pos[0] <= box_width + gap_size + 350 and gap_size + 50 <= mouse_pos[1] <= gap_size + 100:
                    input_active = True
                else:
                    input_active = False
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                        if reward_input:
                            # Split multiple rewards by commas
                            new_rewards = reward_input.split(',')
                            rewards.extend([{"name": reward.strip(), "points": 2} for reward in new_rewards if reward.strip()])
                            reward_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        reward_input = reward_input[:-1]
                    else:
                        reward_input += event.unicode

        # Clear screen
        window.fill(black)

        # Dimensions for boxes
        box_width = window_size[0] // 3
        box_height = window_size[1]

        # Calculate gaps between boxes
        gap_size = 20
        middle_gap = 2 * gap_size

        # Draw the workouts box
        pygame.draw.rect(window, grey, (gap_size, gap_size, box_width - middle_gap, box_height - 2 * gap_size))
        # Render workouts checklist
        workouts_title = font.render("Workouts", True, white)
        window.blit(workouts_title, (gap_size + 30, gap_size + 10))  # Adjusted position for title
        for checkbox in checkboxes:
            checkbox.draw(window)

        # Draw the rewards box
        pygame.draw.rect(window, grey, (box_width + gap_size, gap_size, box_width - middle_gap, box_height - 2 * gap_size))
        # Render rewards list
        reward_title = font.render("Rewards", True, white)
        window.blit(reward_title, (box_width + gap_size + 30, gap_size + 10))  # Adjusted position for title
        y_offset = gap_size + 60
        for index, reward in enumerate(rewards):
            reward_text = small_font.render(f"{index + 1}. {reward['name']} (-{reward['points']} points)", True, white)
            reward_text_rect = reward_text.get_rect()
            reward_text_rect.topleft = (box_width + gap_size + 60, y_offset)
            if reward_text_rect.bottom <= box_height - gap_size:
                reward["rect"] = pygame.Rect(box_width + gap_size + 50, y_offset, 300, 20)
                pygame.draw.rect(window, white, reward["rect"], 2)
                window.blit(reward_text, reward_text_rect)
            y_offset += 30  # Adjusted vertical spacing

        # Draw the score box
        pygame.draw.rect(window, grey, (2 * box_width + gap_size, gap_size, box_width - gap_size, box_height - 2 * gap_size))
        # Render score
        score_text = font.render(f"Score: {points}", True, white)
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (2 * box_width + gap_size + (box_width - gap_size) // 2, gap_size + 40)
        window.blit(score_text, score_text_rect)

        # Capture and display the camera feed
        try:
            if workout:
                frame = next(workout)
                # Resize the frame to fit within the window
                frame = cv2.resize(frame, (640, 480))  # Adjusted size
                frame = np.rot90(frame)  # Rotate frame if necessary
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
                frame = pygame.surfarray.make_surface(frame)
                window.blit(frame, (170, 180))  # Adjusted position
        except StopIteration:
            pass

        pygame.display.flip()
        clock.tick(30)  # Adjusted frame rate

    pygame.quit()




if __name__ == "__main__":
    main()
