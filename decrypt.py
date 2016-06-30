import os
from fractions import gcd
from encode import *
import sys
import re

data = ""

# Dictionary of words found on OSX 10.11.5. Different dictionaries can
# imported here. If running a different version, path may have to be changed.
# If running on a different platform, path will most likey have to be changed.
fp = open("/usr/share/dict/words", "r");
wordList = list(fp)
fp.close()

# Valid starts to English words. Probably not as strict as could be.
# Used to determine which permutations of keys are invalid.
key_regex = re.compile("(bl|br|ch|cl|cr|dr|fl|fr|gl|gr|pl|"
    + "pr|sc|sh|sk|sl|sm|sn|sp|st|sw|th|tr|tw|wh|wr|)[aeiouy]+|"
    + "(sch|scr|shr|sph|spl|spr|squ|str|thr)[aeiouy]*|"
    + "[aeiou][^aeiou]|[^aeiou][aeiou]|[aeiou]+")

# Outputs a list of possible key lengths. Array is ordered
# from most likly key length to least likely.
def freqMatchKeyLength(ciphertext):
    n = len(ciphertext)
    keylength = 0
    matches = list()
    # Iterate through all shifts of the ciphertext. Compare the original
    # ciphertext to the shifted ciphertext and keep track of the shift amount
    # and the number of letters that match. The more matches, the more likely
    # that the shift amount is a multiple of the key length
    for i in range(1, n - 1):
        shiftedCT = ""
        roundMatches = 0
        for j in range(len(ciphertext)):
            shiftedCT += ciphertext[(len(ciphertext) - i + j) % len(ciphertext)]
        for j in range(len(ciphertext)):
            if ciphertext[j] == shiftedCT[j]:
                roundMatches += 1
        matches.append({"index": i, "matches": roundMatches})
    sortedMatches = sorted(matches, key = lambda k: k["matches"], reverse=True)
    gcdFreq = {}
    # Determine the gcd between the three shifts with the highest matches
    # and the rest of the top ten. Rank the gcds based on how often they
    # occur.
    for i in range(3):
        for j in range(10):
            if i == j:
                continue
            candidate = gcd(sortedMatches[i]["index"], sortedMatches[j]["index"])
            if candidate in gcdFreq:
                gcdFreq[candidate] += 1
            else:
                gcdFreq[candidate] = 1
    print sorted(gcdFreq, key=gcdFreq.get, reverse=True)

# Returns a list of lists containing letters that have
# been encrypted with the same letter
def groupColumns(keylength, ciphertext):
    groups = [list() for i in range(keylength)]
    for i in range(len(ciphertext)):
        groups[i % keylength].append(ciphertext[i])
    return groups

# Returns a dictionary of letters and their frequency
# given a list of letters
def computeFreq(column):
    freq = dict.fromkeys(alphabet, 0)
    for letter in column:
        freq[letter] += 1
    return freq

# Writes possible passwords to a file
def solveKey(keylength, ciphertext):
    print "Working..."
    passwordFile = open("pw_" + sys.argv[1], "w")
    groups = groupColumns(keylength, ciphertext)
    freqs = list()
    key = ""
    for group in groups:
        freq = computeFreq(group)
        sortedFreq = sorted(freq, key = freq.get, reverse=True)
        freqs.append(sortedFreq)
    tryKey(freqs, 0, "", keylength, passwordFile, ciphertext)
    passwordFile.close()
    print "Done"

# 13 most common letters in English. Used for figuring out the password
commonLetters = ['e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'l',
    'd','c','u']

# Generates permutations of possible keys. Assumes that the most freqent letter
# that appears in a column maps to the most common letter in English.
def tryKey(freqs, index, key, keylength, file, ciphertext):
    if index == len(freqs):
        print key, "\r",
        pt = decrypt(key, ciphertext)
        digitCount = 0
        for letter in pt:
            if letter.isdigit():
                digitCount += 1
        if digitCount < 5:
            file.write(key + "\n")
            file.write(pt + "\n\n")
    else:
        for j in range(1):
            for k in range(13):
                keyNew = alphabet[charVals[freqs[index][j]] ^ charVals[commonLetters[k]]]
                partialPT = decrypt(key + keyNew, ciphertext[:len(key + keyNew)])
                if keyNew.isdigit():
                    continue
                # check is the string of plaintext characters that would result from
                # decrypting with the current key
                check = ""
                for i in range(len(ciphertext)):
                    if i % keylength == index:
                        check += ciphertext[i]
                check = decrypt(keyNew, check)
                # Check if the plaintext is valid at this point (no numbers, starts correctly)
                if (any(char.isdigit() for char in check)) or (len(key) > 3 and not key_regex.match(key)) or (len(partialPT) > 3 and not key_regex.match(partialPT)):
                    continue
                key += keyNew
                tryKey(freqs, index + 1, key, keylength, file, ciphertext)
                key = key[:-1]

# XOR's each character in the key with each character in the ciphertext.
# Can be used to encrypt or decrypt
def decrypt(key, ciphertext):
    buff = ""
    for i in range(len(ciphertext)):
        if(ciphertext[i] != '\n'):
            buff += alphabet[charVals[ciphertext[i]] ^ charVals[key[i % len(key)]]]
    return buff

# Another method of breaking the cryptosystem, repeatedly tries keys
# from a list of English words
def checkKeys(ciphertext, keylength):
    print "Checking keys..."
    passwordFile = open("pw_" + sys.argv[1], "w")
    for key in wordList:
        candidate = key[:len(key)-1]
        # print candidate
        if(len(candidate) == keylength):
            pt = decrypt(candidate.lower(), ciphertext)
            if not any(char.isdigit() for char in pt):
                passwordFile.write("key: " + candidate + "\n")
                passwordFile.write(pt + "\n\n")
    passwordFile.close()

filename = sys.argv[1]
fp = open(filename, "r")
data = fp.read()
fp.close()

flag = sys.argv[2]
if flag.isdigit() and flag == "0":
    print "Finding keylength..."
    freqMatchKeyLength(data)
elif flag[0] == "-" and int(flag) < 0:
    print "Using wordlist..."
    checkKeys(data, abs(int(flag)))
elif flag.isdigit():
    print "Solving key..."
    solveKey(int(flag), data)
else:
    print "Decrypting..."
    print decrypt(flag, data)
