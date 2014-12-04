import re
import sys
from pprint import pprint

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
     
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Enter the text file as an argument and try again."
        sys.exit()
    pprint(count(sys.argv[1]))