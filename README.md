# File-Compression

Python script that uses Huffman Coding for compressing files.

### How does it work?
-> Enter path of the file that you want to conmpress.

-> The script will make a compressed binary file in respond to the given file.

    Binary file will be made by allocating memory with respect to 
    frequency of each character. For eg. more memory will be given 
    to the most frequent character.
    
    This is done by storing each character of the given file 
    in a hashmap and make a heap out of it, then make a 
    binary tree of characters with most frequent characters
    at top nodes and as we travel towards the leave nodes the 
    frequency decreases. After which we transverse through 
    the tree and assign each character a binary code in order 
    to make a binary file. We add padding at the end of the codes
    (in order to make the codes multiple of 8). Then convert 
    those binary codes to bytes and store into a binary file.
    
-> The script also makes a decompressed file with provided binary file.
    
    Read the binary file and after each binary code we search it
    into the hashmap for corresponding character. The process will 
    be continued till the end of the file and a new decompressed file 
    will be created.
