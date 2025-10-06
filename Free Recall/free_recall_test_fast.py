import pygame
import sys
import random
import time
import csv
import os

Experiment_condition = "fast"  

# Main directory folder
main_dir = os.getcwd()

# Current directory folder
this_dir = os.path.dirname(__file__)

# Data folder path
data_dir = os.path.join(this_dir, 'data')

# Path to the CSV file with words 
project_root = os.path.dirname(this_dir)
words_csv_path = os.path.join(project_root, 'Data', 'memory_nouns_4plus.csv')

# Load words from CSV
def load_words_from_csv(csv_path):
    words = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header if present
            for row in reader:
                if row:  # Make sure row is not empty
                    words.append(row[0])  # Assuming words are in first column
    except FileNotFoundError:
        print(f"Warning: Could not find {csv_path}")
    return words

# Load words and select a random subset
all_words = load_words_from_csv(words_csv_path)
Words = random.sample(all_words, min(15, len(all_words)))  # Select 15 random words

#-----------------------------------------------

import pygame

# Words = ['cat', 'dog', 'car', 'pen', 'box', 'cup', 'tap']
PRESENTATION_TIME = 500  # ms , change to 500 when testing for quicker runs
BREAK_TIME = 0 # ms - break between words, change to 50 or 0 when testing for quicker runs

pygame.init()
pygame.display.set_caption('Free Recall Experiment')
screen = pygame.display.set_mode((1280, 720))

font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 48)  # Add this line
clock = pygame.time.Clock()

# Start Screen with Button

waiting_for_start = True

while waiting_for_start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                waiting_for_start = False

    screen.fill((255, 255, 255))  # Clear screen
    
    # Title
    title_text = font.render('Free Recall Experiment', True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(640, 300))
    screen.blit(title_text, title_rect)
    
    # Instructions
    instruction_text = button_font.render('Press SPACE to start', True, (100, 100, 100))
    instruction_rect = instruction_text.get_rect(center=(640, 400))
    screen.blit(instruction_text, instruction_rect)
    
    pygame.display.flip()
    clock.tick(30)

# Present words once
for word in Words:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            pygame.quit()
            exit()

    screen.fill((255, 255, 255))  # Clear screen
    # pygame.draw.circle(screen, (0, 0, 255), (640, 360), 50)  # optional

    text = font.render(word, True, (0, 0, 0))
    rect = text.get_rect(center=(640, 360))
    screen.blit(text, rect)

    pygame.display.flip()
    pygame.time.delay(PRESENTATION_TIME)

    # Add break - show blank screen
    screen.fill((255, 255, 255))
    pygame.display.flip()
    pygame.time.delay(BREAK_TIME)  # Shows blank screen for 0.5 seconds

# Collect typed input
user_words_list = []  # Store individual words
current_word = ''
prompt = 'Type your recall and press Enter when done:'

collecting = True
while collecting:
    screen.fill((255, 255, 255))

    # Render prompt
    prompt_surface = font.render(prompt, True, (0, 0, 0))
    prompt_rect = prompt_surface.get_rect(center=(640, 150))
    screen.blit(prompt_surface, prompt_rect)

    # Render current input
    input_surface = font.render(current_word, True, (0, 0, 255))
    input_rect = input_surface.get_rect(center=(640, 250))
    screen.blit(input_surface, input_rect)

    # Render list of already entered words
    if user_words_list:
        words_text = "Words entered: " + ", ".join(user_words_list)
        # Just use small font always
        words_surface = pygame.font.Font(None, 32).render(words_text, True, (100, 100, 100))
        words_rect = words_surface.get_rect(center=(640, 350))
        screen.blit(words_surface, words_rect)

    pygame.display.flip()
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            collecting = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if current_word.strip():  # If there's a word entered
                    user_words_list.append(current_word.strip())
                    current_word = ''  # Clear for next word
                else:  # If empty input, finish
                    collecting = False
            elif event.key == pygame.K_BACKSPACE:
                current_word = current_word[:-1]
            else:
                current_word += event.unicode  # append typed character

# Convert back to space-separated string for compatibility with existing code
user_input = ' '.join(user_words_list)

# Final output

# compare with original list
print('You typed:', user_input)
print('Original words:', Words)
for word in Words:
    if word in user_input.split():
        print(f'Correctly recalled: {word}')
    else:
        print(f'Missed: {word}')

# Accuracy score
recalled_words = set(user_input.split())
correct_recall = recalled_words.intersection(set(Words))
accuracy = len(correct_recall) / len(Words) * 100
print(f'Accuracy: {accuracy:.2f}%')

Running = True
while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
    screen.fill((255, 255, 255))
    
# First line - "Words were:"
    words_label = pygame.font.Font(None, 36).render('Words were:', True, (0, 0, 0))
    words_label_rect = words_label.get_rect(center=(640, 200))
    screen.blit(words_label, words_label_rect)
    
    # Second line - just the words
    words_only = ', '.join(Words)
    words_surface = pygame.font.Font(None, 36).render(words_only, True, (0, 0, 0))
    words_rect = words_surface.get_rect(center=(640, 240))
    screen.blit(words_surface, words_rect)
    
    # Your typed words
    typed_text = 'You typed: ' + user_input
    final_surface = pygame.font.Font(None, 36).render(typed_text, True, (0, 0, 0))
    final_rect = final_surface.get_rect(center=(640, 320))
    screen.blit(final_surface, final_rect)
    
    # Accuracy
    accuracy_surface = pygame.font.Font(None, 36).render(f'Accuracy: {accuracy:.2f}%', True, (0, 0, 0))
    accuracy_rect = accuracy_surface.get_rect(center=(640, 400))
    screen.blit(accuracy_surface, accuracy_rect)
    pygame.display.flip()

# Save to CSV

os.makedirs(data_dir, exist_ok=True)
csv_file = os.path.join(data_dir, 'free_recall_results.csv')

# Split brugerens input til en liste

user_words_for_csv = user_input.strip().split()  # Use different variable name

# Konverter til streng med klammeparenteser
true_words_str = "[" + ", ".join(Words) + "]"
user_words_str = "[" + ", ".join(user_words_list) + "]"

# Tæl hvor mange runs der allerede er i filen
if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
    with open(csv_file, 'r', encoding='utf-8') as f:
        num_runs = sum(1 for _ in f) - 1  # -1 for header
else:
    num_runs = 0

test_id = num_runs + 1  # næste testnummer

# Skriv til CSV
file_exists_and_has_content = os.path.exists(csv_file) and os.path.getsize(csv_file) > 0

with open(csv_file, 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)

    if not file_exists_and_has_content:
        writer.writerow(['test', 'condition', 'true_words', 'user_words'])  # header

    writer.writerow([test_id, Experiment_condition,true_words_str, user_words_str])

print(f"Data gemt i {csv_file} (test {test_id})")
