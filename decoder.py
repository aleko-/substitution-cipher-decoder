import re
import random
from collections import defaultdict
import json
import copy
import sys

if len(sys.argv) < 2:
    print "Please add the name of the encrypted file and try again"
    sys.exit()
elif len(sys.argv) > 2:
    print "Too many arguments used. Try again."
    sys.exit()
    
f = open(sys.argv[1], 'r')
original_decode = ''
for char in f.read():
    original_decode += char.lower()
f.close()
# Can take input text with all characters, but only preserves spacing and returns
original_decode = re.sub('[^a-zA-Z\s]+', '', original_decode)
to_decode = re.sub('[\W_]+', '', original_decode)

def collect_quadgrams(string):    
    """
    Returns a dictionary of all quadgrams in 
    the input string with their respective counts.
    """
    new_string = re.sub('[\W_]+', '', string)   # Remove spaces
    tokens = list(new_string)
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
    After the text is decoded, this function will apply 
    spaces to match the spacing of the encrypted text
    """
    idx = 0
    space_positions = []
    for char in original_decode:
        if char == " ":
            space_positions.append(('space', idx))
        elif char == '\n':
            space_positions.append(('return', idx))
        idx += 1

    str_list = []
    for char in input_string:
        str_list.append(char)
        
    for pos in space_positions:
        if pos[0] == 'space':
            str_list.insert(pos[1], ' ')
        else:
            str_list.insert(pos[1], '\n')
    
    output = ''
    for item in str_list:
        output += item
        
    return output

def generate_key():
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    key = list(alphabet)
    random.shuffle(key)    
    return "".join(key)
  
def decode(encoded):
    """
    Scores a decryption, then swaps two keys' values, 
    scores the new decryption, and compares the two scores.
    The best score is always remembered. This continues until
    the best score does not change after 2000 attempts in a row.
    """
    # Initialize variables
    quadgram_scores = json.load(open('quad_scores.json'))
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    key = generate_key()
    best_guess = ''
    high_score = float('-Inf')
    decode_dict = {}
    best_decode = ''
    no_improvement = 0
    iteration = 0
    
    # Set up seed decryption
    for i in range(26):
        decode_dict[alphabet[i]] = key[i]
        i += 1     
        
    # Main loop
    while no_improvement < 1000:
        iteration += 1
        decoded = ''
        score = 0
        
        for letter in to_decode:
            if letter in decode_dict:
                decoded += decode_dict[letter]
                        
        # Score the current key
        decoded_quadgrams = collect_quadgrams(decoded)
        
        for quadgram in decoded_quadgrams:
            if quadgram in quadgram_scores:
                score += quadgram_scores[quadgram]
            else:
                score += (-10.0)

        if score > high_score:
            high_score = score
            no_improvement = 0
            best_decode_dict = copy.copy(decode_dict)
            best_decode = decoded            
            sort_it = sorted(decode_dict.items(), key=lambda x: x[0])
            best_guess = ''
            for value in sort_it:
                best_guess += value[1]
                
            # shuffle dictionary
            a, b = random.choice(decode_dict.keys()), random.choice(decode_dict.keys())
            a_value, b_value = decode_dict[a], decode_dict[b]
            decode_dict[a] = b_value
            decode_dict[b] = a_value 
            
        else:
            # return to better key
            decode_dict = copy.copy(best_decode_dict)
            # shuffle dictionary
            no_improvement += 1
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
    optimum that returns the wrong decoded text.
    """
    best = [() for x in range(iterations)]
    for i in range(iterations):
        best[i] = decode(to_decode)
    sort_it = sorted(best, key=lambda x: x[0], reverse=True)
    return sort_it[0][1]
    
print "Decoding the text... this may take a minute:\n\n", best_decode(3)