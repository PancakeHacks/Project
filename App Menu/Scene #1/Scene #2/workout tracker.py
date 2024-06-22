import pygame
import sys

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
    "Bench Press",
    "Deadlift"
]

# Checkbox class to handle individual checkboxes
class Checkbox:
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
        text_rect.center = self.rect.center
        win.blit(text_surface, text_rect)

    def click(self, pos):
        if self.rect.collidepoint(pos):
            self.checked = not self.checked
            if self.checked:
                # Increase score when checkbox is checked
                increase_score(5)  # Adjust score increase amount as needed

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

def main():
    global reward_input, input_active, points

    clock = pygame.time.Clock()
    run_game = True

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
                if 400 <= mouse_pos[0] <= 700 and 50 <= mouse_pos[1] <= 100:
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
                window.blit(reward_text, reward_text_rect)
            y_offset += 30  # Adjusted vertical spacing

        # Draw the score box
        pygame.draw.rect(window, grey, (2 * box_width + gap_size, gap_size, box_width - gap_size, box_height - 2 * gap_size))
        # Render score
        score_text = font.render(f"Score: {points}", True, white)
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (2 * box_width + gap_size + (box_width - gap_size) // 2, gap_size + 40)
        window.blit(score_text, score_text_rect)

        # Render input box for new rewards
        pygame.draw.rect(window, grey, (box_width + gap_size + 50, gap_size + 50, 300, 50))
        pygame.draw.rect(window, white, (box_width + gap_size + 50, gap_size + 50, 300, 50), 2)
        input_text = input_font.render(reward_input, True, white)
        input_text_rect = input_text.get_rect()
        input_text_rect.topleft = (box_width + gap_size + 60, gap_size + 60)
        if input_text_rect.right <= box_width + gap_size + 300 - 10:  # Limit input text width
            window.blit(input_text, input_text_rect)

        # Render instructions for input box
        instruction_text = small_font.render("Type new rewards (comma-separated) and press Enter:", True, white)
        instruction_text_rect = instruction_text.get_rect()
        instruction_text_rect.topleft = (box_width + gap_size + 50, gap_size + 120)
        window.blit(instruction_text, instruction_text_rect)

        # Render exchange rate info
        exchange_text = small_font.render(f"Exchange rate: {exchange_rate} points per reward", True, white)
        exchange_text_rect = exchange_text.get_rect()
        exchange_text_rect.topleft = (box_width + gap_size + 50, gap_size + 180)
        window.blit(exchange_text, exchange_text_rect)

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
