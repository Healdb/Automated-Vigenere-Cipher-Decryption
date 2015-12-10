import random
def mutateKeys(keys):
    alphabet="abcdefghijklmnopqrstuvwxyz"
    finishedKeys=[]
    for key in keys:
        index=random.randint(0,len(key)-1)
        key=key[:index]+alphabet[random.randint(0,len(alphabet)-1)]+key[index+1:]
        finishedKeys.append(key)
    return finishedKeys
def crossParents(p1,p2):
    p1A = p1[:(len(p1)/2)]
    p1B = p1[(len(p1)/2):]
    p2A = p2[:(len(p2)/2)]
    p2B = p2[(len(p2)/2):]
    C1=p1A+p2B
    C2=p1B+p2A
    return C1, C2
def generateKeys(number, keyLength):
    alphabet="abcdefghijklmnopqrstuvwxyz"
    i=0
    keys=[]
    while i<number:
        n=0
        newKey=""
        while n<keyLength:
            newKey+=alphabet[random.randint(0,len(alphabet)-1)]
            n+=1
        keys.append(newKey)
        i+=1
    return keys
def decrypt(cipherText, key):
    alphabet="abcdefghijklmnopqrstuvwxyz"
    i=0
    decipheredText=""
    for letter in cipherText:
        if i>len(key)-1:
            i=0
        alphabetIndex=alphabet.find(key[i].lower())
        tempAlphabet=alphabet.split(alphabet[alphabetIndex])
        tempAlphabet=alphabet[alphabetIndex]+tempAlphabet[1]+tempAlphabet[0]
        decipheredText+=alphabet[tempAlphabet.find(letter.lower())]
        i+=1
    return decipheredText
def sortValues(frequencies, letters):
    i=(len(frequencies)-1)
    while i>0:
        t=i
        while t>0:
            if frequencies[i]<frequencies[t-1]:
                temp = frequencies[t-1]
                tempLet = letters[t-1]
                frequencies[t-1]=frequencies[i]
                frequencies[i]=temp
                letters[t-1]=letters[i]
                letters[i]=tempLet
            t-=1
        i-=1
    return frequencies, letters
def encrypt(plainText, key):
    alphabet="abcdefghijklmnopqrstuvwxyz"
    i=0
    encipheredText=""
    for letter in plainText:
        if i>len(key)-1:
            i=0
        alphabetIndex=alphabet.find(key[i].lower())
        tempAlphabet=alphabet.split(alphabet[alphabetIndex])
        tempAlphabet=alphabet[alphabetIndex]+tempAlphabet[1]+tempAlphabet[0]
        decipheredText+=alphabet[tempAlphabet.find(letter.lower())]
        i+=1
    return encipheredText
def testFitness(decipheredText):
    alphabet="abcdefghijklmnopqrstuvwxyz"
    frequencies=[]
    letters=[]
    for letter in alphabet:
        count=0
        for compareLetter in decipheredText:
            if letter==compareLetter.lower():
                count+=1
        letters.append(letter)
        frequencies.append(count)
    sfrequencies, sletters = sortValues(frequencies, letters)
    return sletters, sfrequencies
def checkResolved(keys):
    i=1
    while i<len(keys):
        if(keys[i]!=keys[i-1]):
            return False
        i+=1
    return True
def getScore(standardL, extraL,standardF, extraF):
    score=0
    i=0
    for letter in standardL:
        t=0
        for l in extraL:
            if letter==l:
                score+=abs(standardF[i]-extraF[t])
            t+=1
        i+=1
##    i=0
##    for letter in standardL:
##        if letter==extraL[i]:
##            score-=1
##        i+=1
    return score
def runEvolution(maxGenerations,numParents, keyLength, cipherText):
    generation=0
    
    startingKeys=generateKeys(numParents,keyLength)

    text = file("huck.txt").read()
    text= text[(len(text)/2):]
    standardLetters, standardFrequencies=testFitness(text[:len(cipherText)])
    while generation<maxGenerations:
        parentScores=[]
        #print generation
        #print startingKeys
        for key in startingKeys:
            letters, frequencies = testFitness(decrypt(cipherText,key))
            parentScores.append(getScore(standardLetters,letters,standardFrequencies,frequencies))
        parentSortedScores, parentSortedKeys = sortValues(parentScores, startingKeys)
        i=0
        children=[]
        tempC=startingKeys[len(startingKeys)/2:]
        while i<len(startingKeys)/2:
            newIndex=random.randint(0,len(tempC)-1)
            c1,c2=crossParents(startingKeys[i],tempC[newIndex])
            tempC.remove(tempC[newIndex])
            children.append(c1)
            children.append(c2)
            i+=1
        children=mutateKeys(children)
        childrenScores=[]
        for key in children:
            letters, frequencies = testFitness(decrypt(cipherText,key))
            childrenScores.append(getScore(standardLetters,letters,standardFrequencies,frequencies))
        childrenSortedScores, childrenSortedKeys = sortValues(childrenScores, children)
        combinedScores = parentSortedScores+childrenSortedScores
        combinedKeys = parentSortedKeys+childrenSortedKeys
        trashScores, tempKeys = sortValues(combinedScores, combinedKeys)
        startingKeys = tempKeys[:numParents]
        #print trashScores[0]
        if(checkResolved(startingKeys)):
            break
        generation+=1
    return startingKeys[0]   
