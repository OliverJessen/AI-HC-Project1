import pygame
import sys
import random
import time
import csv
import os

# Main directory folder
main_dir = os.getcwd()

# Current directory folder
this_dir = os.path.dirname(__file__)

# Data folder path
data_dir = os.path.join(this_dir, 'data')

# print(main_dir)
# print(this_dir)
# print(data_dir)

#-----------------------------------------------

import pygame

Words = ['cat', 'dog', 'car', 'pen', 'box', 'cup', 'tap']
PRESENTATION_TIME = 1000  # ms

pygame.init()
pygame.display.set_caption('Free Recall Experiment')
screen = pygame.display.set_mode((1280, 720))
font = pygame.font.Font(None, 74)
clock = pygame.time.Clock()

# Present words once
for word in Words:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            pygame.quit()
            exit()

    screen.fill((255, 255, 255))  # Clear screen
    pygame.draw.circle(screen, (0, 0, 255), (640, 360), 50)  # optional

    text = font.render(word, True, (0, 0, 0))
    rect = text.get_rect(center=(640, 360))
    screen.blit(text, rect)

    pygame.display.flip()
    pygame.time.delay(PRESENTATION_TIME)

# --- Collect typed input ---
user_input = ''
prompt = 'Type your recall and press Enter when done:'

collecting = True
while collecting:
    screen.fill((255, 255, 255))

    # Render prompt
    prompt_surface = font.render(prompt, True, (0, 0, 0))
    prompt_rect = prompt_surface.get_rect(center=(640, 250))
    screen.blit(prompt_surface, prompt_rect)

    # Render current input
    input_surface = font.render(user_input, True, (0, 0, 255))
    input_rect = input_surface.get_rect(center=(640, 360))
    screen.blit(input_surface, input_rect)

    pygame.display.flip()
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            collecting = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                collecting = False  # finish input
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            else:
                user_input += event.unicode  # append typed character

# --- final output ---

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
    word_list_surface = font.render('Words were: ' + ', '.join(Words), True, (0, 0, 0))
    word_list_rect = word_list_surface.get_rect(center=(640, 250))
    screen.blit(word_list_surface, word_list_rect)
    final_surface = font.render('You typed: ' + user_input, True, (0, 0, 0))
    final_rect = final_surface.get_rect(center=(640, 360))
    screen.blit(final_surface, final_rect)
    accuracy_surface = font.render(f'Accuracy: {accuracy:.2f}%', True, (0, 0, 0))
    accuracy_rect = accuracy_surface.get_rect(center=(640, 470))
    screen.blit(accuracy_surface, accuracy_rect)
    pygame.display.flip()

# --- Save to CSV ---

os.makedirs(data_dir, exist_ok=True)
csv_file = os.path.join(data_dir, 'free_recall_results.csv')

# Split brugerens input til en liste
user_words_list = user_input.strip().split()

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
        writer.writerow(['test', 'true_words', 'user_words'])  # header

    writer.writerow([test_id, true_words_str, user_words_str])

print(f"Data gemt i {csv_file} (test {test_id})")
