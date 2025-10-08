#!/usr/bin/env python3
"""
Script to fix all incorrectly formatted lines in a CSV file.
Processes the entire file and outputs a corrected version.
"""

import re
import sys
import csv

def fix_csv_line(line):
    """
    Convert a CSV line from incorrect format to correct format.
    
    Handles various input formats:
    1. "[word, word, word]","[word, word, word]" -> "['word', 'word', 'word']","['word', 'word', 'word']"
    2. "[word, word, word]",[word word word] -> "['word', 'word', 'word']","['word', 'word', 'word']"
    """
    
    line = line.strip()
    if not line or line.startswith('trial'):  # Skip header and empty lines
        return line
    
    # Check if line is already properly formatted (contains single quotes around words)
    if "[''" in line or "['" in line:
        return line  # Already properly formatted, don't reprocess
    
    # Split the line carefully to handle quoted sections
    parts = []
    current_part = ""
    in_quotes = False
    
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
            current_part += char
        elif char == ',' and not in_quotes:
            parts.append(current_part.strip())
            current_part = ""
        else:
            current_part += char
    
    if current_part:
        parts.append(current_part.strip())
    
    if len(parts) < 4:
        return line  # Return unchanged if format is unexpected
    
    trial_id = parts[0]
    condition = parts[1]
    presented_part = parts[2]
    recalled_part = parts[3]
    
    # Fix presented words
    presented_fixed = fix_word_list(presented_part)
    
    # Fix recalled words  
    recalled_fixed = fix_word_list(recalled_part)
    
    # Reconstruct the line
    fixed_line = f'{trial_id},{condition},{presented_fixed},{recalled_fixed}'
    return fixed_line

def fix_word_list(word_part):
    """
    Fix a word list part, handling both quoted and unquoted formats.
    """
    word_part = word_part.strip()
    
    # Remove outer quotes if present
    if word_part.startswith('"') and word_part.endswith('"'):
        inner_content = word_part[1:-1]
    else:
        inner_content = word_part
    
    # Handle bracketed lists
    if inner_content.startswith('[') and inner_content.endswith(']'):
        words_str = inner_content[1:-1]  # Remove brackets
        
        # Handle mixed comma and space separation
        if ',' in words_str:
            # Split by commas first, then by spaces within each part
            words = []
            comma_parts = words_str.split(',')
            for part in comma_parts:
                # Split each comma part by spaces and add all words
                space_words = [word.strip() for word in part.split() if word.strip()]
                words.extend(space_words)
        else:
            # Space-separated: "word word word"
            words = [word.strip() for word in words_str.split() if word.strip()]
        
        # Format as list of quoted strings
        fixed_content = "[" + ", ".join(f"'{word}'" for word in words) + "]"
    else:
        # Not in brackets, assume space-separated
        words = [word.strip() for word in inner_content.split() if word.strip()]
        fixed_content = "[" + ", ".join(f"'{word}'" for word in words) + "]"
    
    return f'"{fixed_content}"'

def process_file(input_file, output_file=None, renumber=False, start_from=0):
    """
    Process an entire CSV file and fix formatting issues.
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file (if None, adds '_fixed' to input name)
        renumber: If True, renumber trials sequentially
        start_from: Starting number for renumbering (default 0)
    """
    if output_file is None:
        output_file = input_file.replace('.csv', '_fixed.csv')
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
    
    fixed_lines = []
    trial_counter = start_from
    
    for i, line in enumerate(lines):
        fixed_line = fix_csv_line(line.rstrip('\n\r'))
        
        # Renumber trials if requested and this is not the header line
        if renumber and i > 0 and not line.strip().startswith('trial'):
            # Split the line and replace the first part (trial number)
            parts = fixed_line.split(',', 1)
            if len(parts) >= 2:
                fixed_line = f"{trial_counter},{parts[1]}"
                trial_counter += 1
        
        fixed_lines.append(fixed_line)
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for line in fixed_lines:
            outfile.write(line + '\n')
    
    print(f"Fixed {len(fixed_lines)} lines")
    if renumber:
        print(f"Renumbered trials from {start_from} to {trial_counter - 1}")
    print(f"Original file: {input_file}")
    print(f"Fixed file: {output_file}")

def main():
    """Main function to process input and fix formatting."""
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python fix_csv_format.py <input_file.csv> [output_file.csv] [--renumber] [--start-from N]")
        print("  python fix_csv_format.py 'single_line_to_fix'")
        print()
        print("Options:")
        print("  --renumber       Renumber trials sequentially")
        print("  --start-from N   Start renumbering from N (default: 0)")
        print()
        
        # Test with example line
        test_line = '263,math,"[isle, peak, shoe, bush, flag, stew, crow, kite, barn, bowl, hero, bull, ring, clan, nail]",[isle peak boot bush flag stew crow bowl hero bull ring]'
        print("Testing with example line:")
        print(f"Input:  {test_line}")
        fixed_line = fix_csv_line(test_line)
        print(f"Output: {fixed_line}")
        return
    
    input_arg = sys.argv[1]
    
    # Check if it's a file or a single line
    if input_arg.endswith('.csv'):
        # It's a file - parse arguments
        args = sys.argv[1:]
        input_file = args[0]
        output_file = None
        renumber = False
        start_from = 0
        
        i = 1
        while i < len(args):
            if args[i] == '--renumber':
                renumber = True
            elif args[i] == '--start-from' and i + 1 < len(args):
                start_from = int(args[i + 1])
                i += 1  # Skip the next argument
            elif not args[i].startswith('--') and output_file is None:
                output_file = args[i]
            i += 1
        
        process_file(input_file, output_file, renumber, start_from)
    else:
        # It's a single line
        input_line = ' '.join(sys.argv[1:])
        fixed_line = fix_csv_line(input_line)
        print(f"Output: {fixed_line}")

if __name__ == "__main__":
    main()