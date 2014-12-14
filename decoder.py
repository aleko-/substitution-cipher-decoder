import re
import random
import json
import sys
import time

if len(sys.argv) < 2:
    print "Add the name of the encrypted file and try again"
    sys.exit()
elif len(sys.argv) > 2:
    print "Too many arguments used. Try again."
    sys.exit()

# Read in and preprocess text of the encrypted file
# Store original_decode to remember spacing and returns
original_encrypt = ''
with open(sys.argv[1], 'r') as f:
    for line in f:
        for char in line:
            original_encrypt += char.lower()
original_encrypt = re.sub('[^a-zA-Z\s]+', '', original_encrypt)
to_decode = re.sub('[^a-zA-Z]+', '', original_encrypt)

def collect_quadgrams(string):    
    """
    Returns a list of all quadgrams in the 
    input string with their respective frequencies.
    """
    tokens = list(string)
    tokens_length = len(tokens)
    quadgrams = []
    first, second, third, fourth = 0, 1, 2, 3

    for _ in range(0, tokens_length-3):
        quadgram = str(tokens[first]) + str(tokens[second]) + str(tokens[third]) + str(tokens[fourth])
        quadgrams.append(quadgram)
        first += 1
        second += 1
        third += 1
        fourth += 1

    return quadgrams

def put_spaces_back(input_string):
    """
    After the text is decoded, this function will apply spaces
    and returns to match the formatting of the encrypted text
    """
    idx = 0
    space_positions = []
    # Find positions of spaces and returns in original string
    for char in original_encrypt:
        if char == " ":
            space_positions.append(('space', idx))
        elif char == '\n':
            space_positions.append(('return', idx))
        idx += 1
    # Turn string into a list of chars
    str_list = []
    for char in input_string:
        str_list.append(char)   
    # Insert spaces and returns at the indices noted in space_positions
    for pos in space_positions:
        if pos[0] == 'space':
            str_list.insert(pos[1], ' ')
        else:
            str_list.insert(pos[1], '\n')
    # Turn list back to a string
    output = ''
    for item in str_list:
        output += item
        
    return output

def count(infile):
    """
    Creates a dictionary where the keys are alphabetic characters 
    that occur in the input text and the values are their frequencies.
    """
    # Build a string to work with   
    char_freqs = {}
    text = ''
    with open(infile, 'r') as f:
        for line in f:
            for char in line:
                text += char.lower()

    # Remove non-alphabetic characters 
    text = re.sub('[\W]+', '', text)        

    # Construct dictionary of character frequencies
    for letter in text:
        if letter in char_freqs:
            char_freqs[letter] += 1
        else:
            char_freqs[letter] = 1
    
    return char_freqs

def generate_key(input_dict):
    """
    Generates the alphabet in descending 
    order of the input text's frequency
    """
    freq_list = sorted(input_dict.items(), key=lambda x: x[1], reverse=True)
    key = ''
    for item in freq_list:
        key += str(item[0])
    # Account for text that doesn't include all 26 letters
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    for char in alphabet:
        if char not in key:
            key += char
    return key
  
def decode(encoded):
    """
    Scores a decryption, then swaps two item values in the decode 
    key, scores the new decryption, and compares the two scores.
    The best score is always remembered. This continues until
    the best score does not change after 1000 attempts in a row.
    """
    # Initialize variables
    quadgram_scores = json.load(open('quad_scores.json'))
    alphabet = 'etaoinsrhldcumfpgywbvkjxzq' # Descending order of expected frequency in English.
    key = generate_key(count(sys.argv[1]))
    high_score = float('-Inf')
    decode_dict = {}
    no_improvement = 0
    # Set up seed decryption
    for i in range(26):
        decode_dict[key[i]] = alphabet[i]
        i += 1     
    # Main loop
    while no_improvement < 1000:
        decoded = ''
        score = 0
        # Build decrypted string
        for letter in to_decode:
            if letter in decode_dict:
                decoded += decode_dict[letter]       
                           
        # Score the current decrypted string
        decoded_quadgrams = collect_quadgrams(decoded) 
        for quadgram in decoded_quadgrams:
            if quadgram in quadgram_scores:
                score += quadgram_scores[quadgram]
            else:
                score += (-10.0)

        if score > high_score:
            high_score = score
            best_decode_dict = decode_dict.copy()
            best_decode = decoded
            no_improvement = 0
        else:
            no_improvement += 1
            # Return to a better key
            decode_dict = best_decode_dict.copy()

        # Shuffle key
        a, b = random.choice(decode_dict.keys()), random.choice(decode_dict.keys())
        a_value, b_value = decode_dict[a], decode_dict[b]
        decode_dict[a] = b_value
        decode_dict[b] = a_value
        
    return high_score, put_spaces_back(best_decode)

def best_decode(iterations):
    """
    Runs decode() for specified number of iterations and
    returns the decoded text with the highest score. This
    function is useful to avoiding getting stuck in a local
    optimum that returns the wrong decrypted text.
    """
    best = [() for _ in range(iterations)]
    for i in range(iterations):
        best[i] = decode(to_decode)
        print "Iteration #%s \nbest score: %s \nPreview: %s" %(i+1, best[i][0], best[i][1][:100])
        print
    sort_it = sorted(best, key=lambda x: x[0], reverse=True)
    time.sleep(2)   # Better on the eyes
    print "Decoded text:"
    print
    return sort_it[0][1]

print "Decoding the text...\n\n", best_decode(2)