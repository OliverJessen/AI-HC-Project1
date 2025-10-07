import pygame
import sys
import random
import time
import csv
import os

# Experimental condition
experiment_condition = "chunking"

# Main directory folder
main_dir = os.getcwd()

# Current directory folder
this_dir = os.path.dirname(__file__)
# Path to the CSV file with words
project_root = os.path.dirname(this_dir)  # Go up one level from Free Recall
words_csv_path = os.path.join(project_root, 'Data', 'memory_nouns_4plus.csv')

# Data folder path for output
data_dir = os.path.join(project_root, 'Experiment_Output')

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
Words = random.sample(all_words, min(7, len(all_words)))  # Select 7 random words

#-----------------------------------------------

import pygame

PRESENTATION_TIME = 1000  # ms per letter
BREAK_TIME = 500 # ms - break between letters

pygame.init()
pygame.display.set_caption('Serial Recall Experiment')
screen = pygame.display.set_mode((1280, 720))

font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 48)
clock = pygame.time.Clock()

# --- Start Screen with Button ---
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
    title_text = font.render('Serial Recall Experiment', True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(640, 250))
    screen.blit(title_text, title_rect)
    
    # Instructions
    instruction_text = button_font.render('You will see 7 letters in sequence.', True, (100, 100, 100))
    instruction_rect = instruction_text.get_rect(center=(640, 350))
    screen.blit(instruction_text, instruction_rect)
    
    instruction_text2 = button_font.render('Type them back in the SAME ORDER.', True, (100, 100, 100))
    instruction_rect2 = instruction_text2.get_rect(center=(640, 390))
    screen.blit(instruction_text2, instruction_rect2)
    
    start_text = button_font.render('Press SPACE to start', True, (0, 0, 0))
    start_rect = start_text.get_rect(center=(640, 450))
    screen.blit(start_text, start_rect)
    
    pygame.display.flip()
    clock.tick(30)

# Present letters one by one
for word in Words:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            pygame.quit()
            exit()

    screen.fill((255, 255, 255))  # Clear screen

    text = font.render(word, True, (0, 0, 0))
    rect = text.get_rect(center=(640, 360))
    screen.blit(text, rect)

    pygame.display.flip()
    pygame.time.delay(PRESENTATION_TIME)

    # Add break - show blank screen
    screen.fill((255, 255, 255))
    pygame.display.flip()
    pygame.time.delay(BREAK_TIME)

# --- Collect typed input in sequence ---
user_sequence = ''  # Store the sequence as entered
prompt = 'Type the letters in the same order (no spaces):'

collecting = True
while collecting:
    screen.fill((255, 255, 255))

    # Render prompt
    prompt_surface = button_font.render(prompt, True, (0, 0, 0))
    prompt_rect = prompt_surface.get_rect(center=(640, 200))
    screen.blit(prompt_surface, prompt_rect)

    # Render current input with spacing for readability
    display_sequence = ' '.join(user_sequence.upper())
    input_surface = font.render(display_sequence, True, (0, 0, 255))
    input_rect = input_surface.get_rect(center=(640, 300))
    screen.blit(input_surface, input_rect)
    
    # Show progress
    progress_text = f"Word {len(user_sequence) + 1}/7" if len(user_sequence) < 7 else "Press Enter to finish"
    progress_surface = pygame.font.Font(None, 32).render(progress_text, True, (100, 100, 100))
    progress_rect = progress_surface.get_rect(center=(640, 400))
    screen.blit(progress_surface, progress_rect)

    pygame.display.flip()
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            collecting = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                collecting = False  # Finish when Enter is pressed
            elif event.key == pygame.K_BACKSPACE:
                user_sequence = user_sequence[:-1]
            elif len(user_sequence) < 7 and event.unicode.isalpha():
                user_sequence += event.unicode.upper()

# Convert to list for analysis
user_letters = list(user_sequence.upper())

# --- Analysis ---
print('You typed:', user_sequence.upper())
print('Original sequence:', ''.join(Letters))

# Position-by-position analysis
correct_positions = 0
position_analysis = []

for i in range(max(len(Words), len(user_letters))):
    if i < len(Words) and i < len(user_letters):
        correct = Words[i] == user_letters[i]
        if correct:
            correct_positions += 1
        position_analysis.append({
            'position': i+1,
            'correct_letter': Words[i] if i < len(Words) else '',
            'user_letter': user_letters[i] if i < len(user_letters) else '',
            'correct': correct
        })
        print(f'Position {i+1}: {Words[i] if i < len(Words) else "?"} vs {user_letters[i] if i < len(user_letters) else "?"} - {"✓" if correct else "✗"}')
    elif i < len(Words):
        position_analysis.append({
            'position': i+1,
            'correct_letter': Words[i],
            'user_letter': '',
            'correct': False
        })
        print(f'Position {i+1}: {Words[i]} vs (missing) - ✗')
    else:
        position_analysis.append({
            'position': i+1,
            'correct_letter': '',
            'user_letter': user_letters[i],
            'correct': False
        })
        print(f'Position {i+1}: (extra) vs {user_letters[i]} - ✗')

# Accuracy scores
position_accuracy = correct_positions / len(Words) * 100 if Words else 0
item_accuracy = len(set(user_letters).intersection(set(Words))) / len(Words) * 100 if Words else 0

print(f'Position Accuracy: {position_accuracy:.2f}% ({correct_positions}/{len(Words)} correct positions)')
print(f'Item Accuracy: {item_accuracy:.2f}% (letters recalled regardless of position)')

# --- Display Results ---
Running = True
while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
    
    screen.fill((255, 255, 255))
    
    # Original sequence
    original_label = pygame.font.Font(None, 36).render('Original sequence:', True, (0, 0, 0))
    original_label_rect = original_label.get_rect(center=(640, 150))
    screen.blit(original_label, original_label_rect)
    
    original_sequence = ' '.join(Words)
    original_surface = pygame.font.Font(None, 48).render(original_sequence, True, (0, 0, 0))
    original_rect = original_surface.get_rect(center=(640, 190))
    screen.blit(original_surface, original_rect)
    
    # User sequence
    user_label = pygame.font.Font(None, 36).render('Your sequence:', True, (0, 0, 0))
    user_label_rect = user_label.get_rect(center=(640, 250))
    screen.blit(user_label, user_label_rect)
    
    user_display = ' '.join(user_letters) if user_letters else '(none)'
    user_surface = pygame.font.Font(None, 48).render(user_display, True, (0, 0, 255))
    user_rect = user_surface.get_rect(center=(640, 290))
    screen.blit(user_surface, user_rect)
    
    # Accuracy
    position_acc_surface = pygame.font.Font(None, 36).render(f'Position Accuracy: {position_accuracy:.2f}%', True, (0, 0, 0))
    position_acc_rect = position_acc_surface.get_rect(center=(640, 350))
    screen.blit(position_acc_surface, position_acc_rect)
    
    item_acc_surface = pygame.font.Font(None, 36).render(f'Item Accuracy: {item_accuracy:.2f}%', True, (100, 100, 100))
    item_acc_rect = item_acc_surface.get_rect(center=(640, 390))
    screen.blit(item_acc_surface, item_acc_rect)
    
    pygame.display.flip()

# --- Save to CSV ---
os.makedirs(data_dir, exist_ok=True)
csv_file = os.path.join(data_dir, 'serial_recall_results.csv')

# Count existing runs
if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
    with open(csv_file, 'r', encoding='utf-8') as f:
        num_runs = sum(1 for _ in f) - 1  # -1 for header
else:
    num_runs = 0

test_id = num_runs + 1

# Convert sequences to strings with brackets and commas to match free recall format
original_sequence_str = "[" + ", ".join(Words) + "]"
user_sequence_str = "[" + ", ".join(list(user_sequence.upper())) + "]" if user_sequence else "[]"

# Write to CSV
file_exists_and_has_content = os.path.exists(csv_file) and os.path.getsize(csv_file) > 0

with open(csv_file, 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)

    if not file_exists_and_has_content:
                writer.writerow(['trial', ' condition', ' presented_words', ' recalled_words'])

    writer.writerow([test_id, experiment_condition, original_sequence_str, user_sequence_str])

print(f"Data saved to {csv_file} (test {test_id})")

pygame.quit()