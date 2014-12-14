## Simple Cipher Decoder

To run the decoder, pass the text file you want to decode as the command line argument.
For example: 

`>> python decoder.py "encrypted.txt"`

Make sure quad_scores.json is in the same directory as decoder.py

The decoder will preserve spacing and returns, but does not keep any punctuation.

quad_scores.json is a dictionary of roughly 2,5000,000 English quadgrams where the values are the log of a quadgram's relative frequency. The original file of quadgram counts was taken from http://practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/