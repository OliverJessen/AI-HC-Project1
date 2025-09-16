import pygame
import sys
import random
import time
import csv
import os
from datetime import datetime

# -----------------------------
# Paths / data folder
# -----------------------------
THIS_DIR = os.path.dirname(__file__) if "__file__" in globals() else os.getcwd()
DATA_DIR = os.path.join(THIS_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# -----------------------------
# Experiment constants
# -----------------------------
LIST_LEN = 20
SLOW_PRESENT_MS = 1000     # baseline / "normal" presentation (supports LTM/primacy)
FAST_PRESENT_MS = 300      # faster presentation (impairs primacy, not recency)
ISI_MS = 250               # blank between words
DELAY_SEC = 15             # for "delay only" and "secondary task (filled delay)"
FONT_SIZE_MAIN = 64
FONT_SIZE_SMALL = 32
WIN_W, WIN_H = 1280, 720

# Word pool (simple, concrete, easy-to-type)
WORD_POOL = [
    "cat","dog","car","pen","box","cup","tap","sun","map","tree","bird","book","shoe","door","lamp","ring",
    "fish","milk","star","chair","house","apple","train","plane","phone","glass","coin","key","plate","bread",
    "clock","mouse","plant","river","stone","paper","spoon","watch","shirt","table","cable","pizza","couch",
    "towel","shirt","sofa","drum","flute","crown","brush","paint","wheel","stick","rope","cloud","rain","snow",
    "horse","goat","sheep","candy","lemon","peach","grape","berry","water","juice","chair","bench","field",
    "beach","island","forest","desert","valley","mountain","bridge","street","alley","garden","window","letter",
    "piano","guitar","violin","camera","radio","ticket","pillow","blanket","helmet","rocket","planet","comet",
    "candle","mirror","basket","butter","honey","tomato","garlic","ginger","onion","carrot","pepper","salt"
]

# -----------------------------
# Pygame setup
# -----------------------------
pygame.init()
pygame.display.set_caption("Free Recall Experiment")
screen = pygame.display.set_mode((WIN_W, WIN_H))
clock = pygame.time.Clock()
font_main = pygame.font.Font(None, FONT_SIZE_MAIN)
font_small = pygame.font.Font(None, FONT_SIZE_SMALL)

# -----------------------------
# Utilities
# -----------------------------
def draw_center_text(text, y=None, font=font_main, color=(0,0,0)):
    if y is None:
        y = WIN_H // 2
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(WIN_W//2, y))
    screen.blit(surf, rect)
    return rect

def wait_for_keypress(valid_keys=None):
    """Block until a keydown; returns the key."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if valid_keys is None or event.key in valid_keys:
                    return event.key
        clock.tick(60)

def show_instructions():
    screen.fill((255,255,255))
    draw_center_text("Free Recall – vælg en betingelse:", y=120)
    lines = [
        "1) Baseline (20 ord, normal hastighed, ingen forsinkelse)",
        "2) Hurtig præsentation (impairer primacy / LTM)",
        "3) Sekundær WM-opgave i pausen (impairer recency / WM)",
        "4) Kun forsinkelse (blank i 15s; recency intakt)",
        "Tryk [1]-[4] for at vælge. [ESC] for at afslutte."
    ]
    y = 220
    for ln in lines:
        draw_center_text(ln, y=y, font=font_small)
        y += 40
    pygame.display.flip()

def pick_condition():
    show_instructions()
    while True:
        key = wait_for_keypress()
        if key == pygame.K_ESCAPE:
            pygame.quit(); sys.exit(0)
        if key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
            return {pygame.K_1: "baseline", pygame.K_2: "fast",
                    pygame.K_3: "secondary_task", pygame.K_4: "delay_only"}[key]

def sample_word_list(n=LIST_LEN):
    # random sample without replacement
    return random.sample(WORD_POOL, n)

def present_list(words, present_ms, isi_ms=ISI_MS):
    """Show words sequentially. Returns list of (word, onset_time_s)."""
    shown = []
    for w in words:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit(0)

        screen.fill((255,255,255))
        draw_center_text(w)
        pygame.display.flip()
        onset = time.time()
        pygame.time.delay(present_ms)
        shown.append((w, onset))

        # ISI blank
        screen.fill((255,255,255))
        pygame.display.flip()
        pygame.time.delay(isi_ms)
    return shown

def run_delay(seconds, filled=False):
    """If filled=True, run a simple secondary WM task (impairs recency).
       Otherwise just blank countdown (delay only)."""
    start = time.time()
    correct = 0
    total_targets = 0

    while True:
        elapsed = time.time() - start
        remaining = max(0, int(seconds - elapsed))
        if remaining <= 0:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit(0)

        screen.fill((255,255,255))
        if filled:
            # Oddball detection: stream of digits; press SPACE when digit is odd
            digit = random.randint(1,9)
            is_target = (digit % 2 == 1)
            if is_target:
                total_targets += 1

            draw_center_text("SEKUNDÆR OPGAVE (WM):", y=160, font=font_small)
            draw_center_text("Tryk [SPACE], når tallet er ULIGE.", y=200, font=font_small)
            draw_center_text(f"Tid tilbage: {remaining}s", y=260, font=font_small)
            draw_center_text(str(digit), y=360, font=font_main)

            pygame.display.flip()

            t0 = time.time()
            responded = False
            # each digit stays ~0.8s
            while time.time() - t0 < 0.8:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit(); sys.exit(0)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit(); sys.exit(0)
                        if event.key == pygame.K_SPACE and not responded:
                            responded = True
                            if is_target:
                                correct += 1
                clock.tick(60)
        else:
            # Delay only (blank countdown)
            draw_center_text("Vent venligst…", y=280, font=font_small)
            draw_center_text(f"Tid tilbage: {remaining}s", y=340, font=font_small)
            pygame.display.flip()
            pygame.time.delay(250)

    return {"wm_correct": correct, "wm_targets": total_targets}

def collect_free_recall():
    """Free order text input; Enter to finish."""
    user_input = ""
    prompt1 = "Skriv alle ord, du kan huske (valgfri rækkefølge)."
    prompt2 = "Tryk [ENTER] for at afslutte. [BACKSPACE] for at slette. [ESC] for at afbryde."

    collecting = True
    recall_start = time.time()
    while collecting:
        screen.fill((255,255,255))
        draw_center_text(prompt1, y=200, font=font_small)
        draw_center_text(prompt2, y=240, font=font_small)

        # wrapped display of input
        draw_center_text(user_input, y=360, font=font_main, color=(0,0,128))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit(0)
                elif event.key == pygame.K_RETURN:
                    collecting = False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
        clock.tick(60)
    recall_end = time.time()
    return user_input, recall_end - recall_start

def tokenize(s):
    # lower, split by whitespace and punctuation-friendly
    raw = s.lower().replace(",", " ").replace(";", " ").replace("\n", " ")
    toks = [t.strip() for t in raw.split() if t.strip() != ""]
    return toks

def score_recall(target_words, recalled_tokens):
    target_set = set(w.lower() for w in target_words)
    recalled_set = set(recalled_tokens)
    correct = sorted(list(target_set.intersection(recalled_set)))
    accuracy = len(correct) / len(target_words)

    # Serial-position scoring: per position recall (1 if recalled)
    pos_hits = []
    target_lc = [w.lower() for w in target_words]
    for i, w in enumerate(target_lc):
        pos_hits.append(1 if w in recalled_set else 0)

    # Primacy: positions 1-4 (0..3), Recency: positions 17-20 (16..19)
    primacy_idx = list(range(0, 4))
    recency_idx = list(range(len(target_words)-4, len(target_words)))
    primacy = sum(pos_hits[i] for i in primacy_idx) / len(primacy_idx)
    recency = sum(pos_hits[i] for i in recency_idx) / len(recency_idx)

    return {
        "accuracy": accuracy,
        "correct": correct,
        "pos_hits": pos_hits,
        "primacy": primacy,
        "recency": recency
    }

def draw_serial_position_curve(pos_hits):
    """Simple bar plot in pygame (1=hit, 0=miss) for 20 positions."""
    screen.fill((255,255,255))
    draw_center_text("Serial Position Curve (hit=1, miss=0)", y=80, font=font_small)

    n = len(pos_hits)
    margin = 100
    plot_w = WIN_W - 2*margin
    plot_h = 400
    x0 = margin
    y0 = 560  # baseline y
    bar_w = plot_w / n * 0.8
    step = plot_w / n

    # axes
    pygame.draw.line(screen, (0,0,0), (x0, y0), (x0+plot_w, y0), 2)
    pygame.draw.line(screen, (0,0,0), (x0, y0), (x0, y0 - plot_h), 2)

    for i, hit in enumerate(pos_hits):
        h = int(hit * (plot_h - 10))
        x = int(x0 + i*step + (step - bar_w)/2)
        y = y0 - h
        pygame.draw.rect(screen, (0,0,0), (x, y, int(bar_w), h))
        # x labels every 5th
        if (i+1) % 5 == 0 or i in (0, n-1):
            lbl = font_small.render(str(i+1), True, (0,0,0))
            screen.blit(lbl, (x, y0 + 5))

    pygame.display.flip()

def save_csv(row_dict):
    csv_path = os.path.join(DATA_DIR, "free_recall_results.csv")
    header = [
        "timestamp","participant_id","condition","list_words","typed_recall",
        "list_len","presentation_ms","isi_ms","delay_sec","secondary_task",
        "recall_duration_s","accuracy","primacy","recency","pos_hits",
        "wm_correct","wm_targets"
    ]
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row_dict)

# -----------------------------
# Main flow
# -----------------------------
def main():
    # Optional: collect participant ID
    participant_id = "P001"

    condition = pick_condition()
    if condition == "baseline":
        presentation_ms = SLOW_PRESENT_MS
        delay_sec = 0
        secondary = False
    elif condition == "fast":
        presentation_ms = FAST_PRESENT_MS
        delay_sec = 0
        secondary = False
    elif condition == "secondary_task":
        presentation_ms = SLOW_PRESENT_MS
        delay_sec = DELAY_SEC
        secondary = True
    elif condition == "delay_only":
        presentation_ms = SLOW_PRESENT_MS
        delay_sec = DELAY_SEC
        secondary = False
    else:
        pygame.quit(); sys.exit(0)

    # Ready screen
    screen.fill((255,255,255))
    draw_center_text(f"Betingelse: {condition}", y=250, font=font_small)
    draw_center_text("Tryk en vilkårlig tast for at starte præsentationen.", y=310, font=font_small)
    pygame.display.flip()
    wait_for_keypress()

    # Make word list (20 items)
    words = sample_word_list(LIST_LEN)

    # Present list
    presented = present_list(words, presentation_ms, ISI_MS)

    # Post-list delay (optional): either blank (delay only) or secondary WM task (filled delay)
    wm_stats = {"wm_correct": 0, "wm_targets": 0}
    if delay_sec > 0:
        wm_stats = run_delay(delay_sec, filled=secondary)

    # Free recall
    typed, recall_dur = collect_free_recall()
    recalled_tokens = tokenize(typed)
    results = score_recall(words, recalled_tokens)

    # Show results summary
    screen.fill((255,255,255))
    draw_center_text(f"Akkurathed: {results['accuracy']*100:.1f}%", y=200, font=font_main)
    draw_center_text(f"Primacy (1-4): {results['primacy']*100:.1f}%   |   Recency (17-20): {results['recency']*100:.1f}%", y=280, font=font_small)
    draw_center_text(f"Korrekt (n={len(results['correct'])}): {', '.join(results['correct'])}", y=340, font=font_small)
    draw_center_text("Tryk en vilkårlig tast for serial-position graf.", y=420, font=font_small)
    pygame.display.flip()
    wait_for_keypress()

    # Serial position curve
    draw_serial_position_curve(results["pos_hits"])
    draw_center_text("Tryk [ESC] for at afslutte eller en vilkårlig tast for at gemme og afslutte.", y=120, font=font_small)
    pygame.display.flip()
    key = wait_for_keypress()

    # Save CSV
    row = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "participant_id": participant_id,
        "condition": condition,
        "list_words": " ".join(words),
        "typed_recall": typed,
        "list_len": LIST_LEN,
        "presentation_ms": presentation_ms,
        "isi_ms": ISI_MS,
        "delay_sec": delay_sec,
        "secondary_task": int(secondary),
        "recall_duration_s": round(recall_dur, 3),
        "accuracy": round(results["accuracy"], 4),
        "primacy": round(results["primacy"], 4),
        "recency": round(results["recency"], 4),
        "pos_hits": " ".join(map(str, results["pos_hits"])),
        "wm_correct": wm_stats.get("wm_correct", 0),
        "wm_targets": wm_stats.get("wm_targets", 0),
    }
    save_csv(row)

    # Final screen
    screen.fill((255,255,255))
    draw_center_text("Data gemt til: data/free_recall_results.csv", y=300, font=font_small)
    draw_center_text("Tak! Luk vinduet eller tryk [ESC].", y=360, font=font_small)
    pygame.display.flip()

    # Exit loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit(0)
        clock.tick(60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pygame.quit()
