import math
import os.path

# Includes functions used to turn a binary string into
# a string of numbers of letters. For this project, the following encoding
# scheme was used:
#   a: 00000, b: 00001, c: 00010, ..., z: 11001

# map from number to character
alphabet = ['a','b','c','d','e', 'f', 'g', 'h', 'i', 'j','k','l','m','n','o',
    'p','q','r','s','t','u','v','w','x','y','z', '0', '1', '2', '3','4','5']

# map from character to number
charVals = dict.fromkeys(alphabet, 0)
for letter, i in zip(alphabet, range(26)):
    charVals[letter] = i
for i in range(6):
    charVals[str(i)] = i + 26

def readFile(name):
    buff = []
    fp = open(name, "r")
    for line in fp:
        if line[0] != '\n':
            for i in range(len(line)):
                buff.append(int(line[i]))
    fp.close()
    return buff

def toDecimal(bitString):
    decimal = 0;
    for i in range(len(bitString)):
        decimal += bitString[i] * math.pow(2, len(bitString) - (i + 1))
    return int(decimal)

def decode(bitString):
    buff = []
    message = ""
    for i in range(len(bitString)):
        buff.append(bitString[i])
        if len(buff) == 5:
            index = toDecimal(buff)
            if index < 26:
                message += alphabet[toDecimal(buff)]
            else:
                message += str(index - 26)
            del buff[:]
    return message
