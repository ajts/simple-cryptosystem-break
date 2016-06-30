## Overview

Python script to break a simple cyrptosystem. The cryptosystem consists of a key of that is repeated until it matches the length of some given plaintext. A bitwise XOR is performed between the two strings to produce a ciphertext. For this project, keys are assumed to include only English letters and be valid English words or phrases, although may still work if words are slightly misspelled. This script doesn't  output the exact key, but outputs likely keys to a file. This file can then be inspected and with some problem solving and intuition the key can be determined.

## Running

Must have Python 2.7 installed. The script must have permission to write to the directory it is in. Commands take the following form:

    python decrypt.py file_name flag

This command will perform some function using the given file as input. The file must be a single line on ciphertext consisting of letters and numbers. The function will depend on the format and value of the flag. The flag can the number `0`, a negative number, a positive number, or a string of characters.

* `0`: Outputs a list of the most likely key lengths for some given ciphertext
* Negative number (`-k`): Decrypts the ciphertext using words from a dictionary. Looks for words that are length `k`. The most likely keys are written a file.
* Positive number (`k`): Generates keys of length `k` and uses those to decrypt the ciphertext. The most likely keys are written to a file.
* String of characters (`key`): `key` is repeated until it matches the length of the ciphertext. A bitwise XOR is then performed between the two and is printed to the screen. This can be used either for encryption or decryption.
