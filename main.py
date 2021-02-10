# used Huffman Coding 

import os
import heapq

class BinaryTreeNode :
    def __init__ (self, value, freq) :
        self.value = value
        self.freq = freq
        self.left, self.right = None, None

    def __lt__ (self, node) :
        return self.freq < node.freq

    def __eq__ (self, node) :
        return self.freq == node.freq


class FileCompression :

    def __init__ (self, path) :
        self.path = path
        self.__heap = []
        self.__binaryCodes = {}
        self.__removeBinaryCodes = {}
    
    def __frequencyDictionary (self, text) :
        freqDict = {}
        for char in text :
            freqDict[char] = freqDict.get(char, 0) + 1
        
        return freqDict

    def __buildHeap (self, freqDict) :
        for value in freqDict :
            freq = freqDict[value]
            node = BinaryTreeNode(value, freq)
            heapq.heappush(self.__heap, node)

    def __buildTree (self) :
        while len(self.__heap) > 1 :
            node1 = heapq.heappop(self.__heap)
            node2 = heapq.heappop(self.__heap)
            freqSum = node1.freq + node2.freq
            newNode = BinaryTreeNode(None, freqSum)
            newNode.left = node1
            newNode.right = node2
            heapq.heappush(self.__heap, newNode)

    def __buildBinaryCodesHelper (self, node, currBits) :
        if node is None :
            return

        if node.value is not None :
            self.__binaryCodes[node.value] = currBits
            self.__removeBinaryCodes[currBits] = node.value
            return

        self.__buildBinaryCodesHelper(node.left, currBits+"0")
        self.__buildBinaryCodesHelper(node.right, currBits+"1")

    def __buildBinaryCodes (self) :
        root = heapq.heappop(self.__heap)
        self.__buildBinaryCodesHelper(root, "")

    def __getEncodedText (self, text) :
        encodedText = ""
        for char in text :
            encodedText += self.__binaryCodes[char]
        
        return encodedText

    def __getPaddedEncodedText (self, encodedText) :
        paddedAmount = 8 - (len(encodedText)%8)

        for _ in range(paddedAmount) :
            encodedText += "0"
        
        paddedInfo = "{0:08b}".format(paddedAmount)
        paddedEncodedText = paddedInfo + encodedText

        return paddedEncodedText

    def __getIntList (self, paddedEncodedText) :
        intList = []

        for i in range(0, len(paddedEncodedText), 8) :
            byte = paddedEncodedText[i:i+8]
            intList.append(int(byte, 2))

        return intList

    def compress (self) :

        # get file from path
        fileName, _ = os.path.splitext(self.path)
        outputPath = fileName + ".bin"

        with open(self.path, "r+") as file, open(outputPath, "wb") as output :
            text = file.read()
            text.rstrip()

            # make dictionary to store frequency of each letter
            freqDict = self.__frequencyDictionary(text)

            # construct heap of binary tree node
            self.__buildHeap(freqDict)

            # construct binary tree from heap
            self.__buildTree()

            # create binary codes from binary tree
            self.__buildBinaryCodes()

            # create encoded text from binary codes
            encodedText = self.__getEncodedText(text)

            # add padding to encoded text 
            paddedEncodedText = self.__getPaddedEncodedText(encodedText)

            # creating list of integers from 8 bits
            intList = self.__getIntList(paddedEncodedText)

            # converting the integer list to bytes
            finalBytes = bytes(intList)

            # write on output file
            output.write(finalBytes)

        return outputPath

    def __removePadding (self, text) :
        paddedInfo = text[:8]
        paddedAmount = int(paddedInfo, 2)

        text = text[8:]
        actualText = text[:-1*paddedAmount] 

        return actualText

    def __decodeText (self, text) :
        decodedText = ""
        currBits = ""

        for bit in text :
            currBits += bit
            if self.__removeBinaryCodes.get(currBits) is not None :
                char = self.__removeBinaryCodes[currBits]                
                decodedText += char
                currBits = ""
        
        return decodedText

    def decompress (self, input_path) :

        # get file from path 
        fileName, _ = os.path.splitext(input_path)
        outputPath = fileName + "_decompressed.txt"

        with open(input_path, "rb") as file, open(outputPath, "w") as output :
            bitString = ""
            byte = file.read(1)
            while byte :
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, "0")
                bitString += bits
                byte = file.read(1) 
            
            # remove padding from end of the text
            actualText = self.__removePadding(bitString)

            # convert binary codes to char
            decompressedText = self.__decodeText(actualText)

            output.write(decompressedText)


path = input()
file = FileCompression(path)

compressedFilePath = file.compress()

file.decompress(compressedFilePath)
