import pickle

# Name Input
firstName = input('First Name:')
lastName = input('Last Name:')
minSubWordSize = int(input('Minimum size for subword (enter integer please):'))

name = str.lower(firstName + lastName)

# Blank dict to use in future to track set of words and what letters they contain
blankAlpha = {"a":0, "b":0, "c":0, "d":0, "e":0, "f":0, "g":0, 
"h":0, "i":0, "j":0, "k":0, "l":0, "m":0, "n":0, "o":0, "p":0, 
"q":0, "r":0, "s":0, "t":0, "u":0, "v":0, "w":0, "x":0, "y":0, "z":0}

# Function to break down words into letters
def breakWord(word):
    letterDict = blankAlpha.copy()
    for letter in word:
        letterDict[letter] += 1
    return letterDict

# Array to track all words in dictionary and sort them by length
# Note: index 1 is of words with length 1, index 2 for length 2 etc.
sortedDict = [['']] * 32

recompile = False  # Can re-compile data by setting to true
if recompile: 
    with open('./dictionary.txt') as f:
        for line in f:
            word = line.strip()
            sortedDict[len(word)] = sortedDict[len(word)] + [word]  
    with open("./compiledDictionary", 'wb') as fp:
        pickle.dump(sortedDict, fp)
else:
    with open("./compiledDictionary", 'rb') as fp:
        sortedDict = pickle.load(fp)

#function to recursively find the anagram of a given word
#starting with words with the length of the key word, then working down and filling in any gaps as needed
def findAnagram(word):
    #trackign what words used
    words = []
    wordAlpha = breakWord(word)

    #looking for the word with same length
    if len(word) < len(sortedDict):
        for loopWord in sortedDict[len(word)]:
            if breakWord(loopWord) == wordAlpha:
                breakWord(loopWord)
                return [loopWord]

    #now breakign word down into subwords
    #first making all permutations of the current string to then break up
    rearrangeOptions = rearrange(word)
    for option in rearrangeOptions:
        #taking the bigest sub word we can to split the string, but not letting there be any 1 letter words
        #only splitting into two, because we can always recursively split each half into more
        for i in range(len(option) - 2): 
            word1 = option[0:i+2]
            word2 = option[i+2:]

            #skipping these words if either subword would be 1 letter
            if len(word1) == 1 or len(word2) == 1 or len(word1) < minSubWordSize or len(word2) < minSubWordSize: 
                continue

            #solving subwords
            solved1 = findAnagram(word1)
            solved2 = findAnagram(word2)

            #returning nothing if either subword had no solutions
            if len(solved1) == 0 or len(solved2) == 0:
                continue
            
            return solved1 + solved2
    return []

def rearrangeLight(word):
    options = []
    for i in range(len(word) - 2): 
        word1 = word[0:i+2]
        word2 = word[i+2:]

        if len(word1) == 1 or len(word2) == 1:
            continue
        options.append(word2 + word1)
    return options

def rearrangeDeep(word):
    if len(word) <= 1:
        return [word]

    options = []
    for i in range(len(word)):
        subOptions = rearrangeDeep(word[:i] + word[i+1:])
        for subOption in subOptions:    
            options.append(word[i] + subOption)
    return options

def rearrange(word):
    if len(word) >= 7:
        return rearrangeLight(word)
    else:
        return rearrangeDeep(word)    

print("Subwords are:", findAnagram(name))