from collections import Counter

def most_frequent_word(text):
    #textToList = text.split()
    #counterWord = Counter(textToList)
    #maximum = max(counterWord.values())
    #return "\n".join([k for k,v in counterWord.items() if v == maximum])
    return Counter(text.split()).most_common(1)[0][0]