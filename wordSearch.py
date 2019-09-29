import json
import queue
import copy

alphabet = "abcdefghijklmnopqrstuvwxyz"
alphabet_index = {}
for x in range(0, 26):
    alphabet_index[alphabet[x]] = x

class TrieNode:
    def __init__(self):
        self.children = [None]*26
        self.endOfWord = False

    def has_child(self, character):
        char = str(character)
        lowerCase = char.lower()
        return self.children[alphabet_index[lowerCase]] != None
    
    def return_child(self, character):
        char = str(character)
        lowerCase = char.lower()
        return self.children[alphabet_index[lowerCase]]
    

#Trie retrieval data structure. Allowed for fast lookups of words based on prefixes and "in place checking" of what word can be obtained from a given position
class Trie: 
    def __init__(self):
        self.rootNode = TrieNode()
        
    def root_has_child(self, char):
        return self.rootNode.has_child(char)

    def search(self, word):
        trieCrawler = self.rootNode
        for x in range(len(word)):
            currentChar = alphabet_index[word[x]]
            if trieCrawler.children[currentChar] != None:
                trieCrawler = trieCrawler.children[currentChar]
            else:
                return False
        
        if trieCrawler.endOfWord == True:
            return True
        
        return False

    def insert(self, word):
        trieCrawler = self.rootNode
        for x in range(len(word)):
            currentChar = alphabet_index[word[x]]
            if trieCrawler.children[currentChar] != None:
                trieCrawler = trieCrawler.children[currentChar]
            else:
                trieCrawler.children[currentChar] = TrieNode()
                trieCrawler = trieCrawler.children[currentChar]
        trieCrawler.endOfWord = True

class wordPath:
    def __init__(self, inputTrie, startX, startY, startChar):
        self.currentTrieNode = inputTrie
        self.totalWord = startChar.lower()
        self.currentX = startX
        self.currentY = startY
        #IMPORTANT: used x and y tiles are in parallel
        self.usedX = [startX]
        self.usedY = [startY]

    

    def already_visited(self, nextX, nextY):
        for i in range(0, len(self.usedX)):
            if self.usedX[i] == nextX and self.usedY[i] == nextY:
                return True
        return False

    def add_tile(self, newX, newY, newChar):
        self.currentTrieNode = self.currentTrieNode.return_child(newChar)
        self.totalWord += newChar.lower()
        self.currentX = newX
        self.currentY = newY
        self.usedX.append(newX)
        self.usedY.append(newY)
    

class wordSearcher:
    def __init__(self):
        self.gameInfo = json.load(open("input.json"))
        self.mainTrie = Trie()
        #Initilize the word tree
        for words in self.gameInfo['wordList']:
            self.mainTrie.insert(words.lower())
        self.foundWords = set()

    def search_words(self):
        #Keep a running a queue of potential paths containing words, BFS of possible valid paths
        for row in range(0, len(self.gameInfo['gameBoard'])):
            for tile in range(0, len(self.gameInfo['gameBoard'][row])):
                runningQueue = queue.Queue()
                newCharacter = self.gameInfo['gameBoard'][row][tile]
                if self.mainTrie.root_has_child(newCharacter) == True:
                    runningQueue.put(wordPath(self.mainTrie.rootNode.return_child(newCharacter), tile, row, newCharacter))
                while(runningQueue.empty() == False):
                    currentWordPath = runningQueue.get()
                    if(currentWordPath.currentTrieNode.endOfWord == True):
                        self.foundWords.add(currentWordPath.totalWord)
                    currentXpos = currentWordPath.currentX
                    currentYpos = currentWordPath.currentY
                    newXpos = []
                    newYpos = []
                    #Look right
                    if(currentXpos < self.gameInfo['columnCount'] - 1):
                        newXpos.append(currentXpos + 1)
                        newYpos.append(currentYpos)
                        
                    #Look left
                    if(0 < currentXpos):
                        newXpos.append(currentXpos - 1)
                        newYpos.append(currentYpos)
                    #Look down
                    if(currentYpos < self.gameInfo['rowCount'] - 1):
                        newXpos.append(currentXpos)
                        newYpos.append(currentYpos + 1)
                    #Look up
                    if(0 < currentYpos):
                        newXpos.append(currentXpos)
                        newYpos.append(currentYpos - 1)
                    #Look lower right
                    if(currentXpos < self.gameInfo['columnCount'] - 1 and currentYpos < self.gameInfo['rowCount'] - 1):
                        newXpos.append(currentXpos + 1)
                        newYpos.append(currentYpos + 1)
                    #Look upper right
                    if(currentXpos < self.gameInfo['columnCount'] - 1 and 0 < currentYpos):
                        newXpos.append(currentXpos + 1)
                        newYpos.append(currentYpos - 1)
                    #Look lower left
                    if(0 < currentXpos and currentYpos < self.gameInfo['rowCount'] - 1):
                        newXpos.append(currentXpos - 1)
                        newYpos.append(currentYpos + 1)
                    #Look upper left
                    if(0 < currentXpos and 0 < currentYpos):
                        newXpos.append(currentXpos - 1)
                        newYpos.append(currentYpos - 1)
                    
                    for i in range(0, len(newXpos)):
                        possibleCharacter = self.gameInfo['gameBoard'][newYpos[i]][newXpos[i]]
                        #Make sure you are making a completely make a new and seperate copy to put in queue
                        tempPath = copy.deepcopy(currentWordPath)
                        if(tempPath.currentTrieNode.has_child(possibleCharacter) == True and tempPath.already_visited(newXpos[i], newYpos[i]) == False):
                            tempPath.add_tile(newXpos[i], newYpos[i], possibleCharacter)
                            runningQueue.put(tempPath)
        
        
        sortedList = sorted(self.foundWords)
        for x in sortedList:
            print(x)


testWordSearcher = wordSearcher()
testWordSearcher.search_words()
