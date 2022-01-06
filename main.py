import sys

# create a program that goes through a list of words and matches them to certain criteria (can not have certain letters)
# the program should print out the words that match the criteria
def main(banned_letters = '', partialWord = '_____', contains_letters = ''):
    if len(partialWord) != 5:
        print('partialWord must be 5 characters long')
        return
    # create a list of words
    # open the file 'five_characters.txt' and save each line to a list
    file = open('five_characters.txt', 'r')
    words = []
    for line in file:
        words.append(line.strip())
    
    # create a list of letters that are not allowed
    forbiddenLetters = set(banned_letters)
    # create a list to hold the words that match the criteria
    matchingWords = []
    # loop through the words
    for word in words:
        if set(word).isdisjoint(forbiddenLetters) and set(contains_letters).issubset(set(word)):
            match = True
            for i in range(len(partialWord)):
                if partialWord[i] != '_':
                    if partialWord[i] != word[i]:
                        match = False
                        break
            if match:
                matchingWords.append(word)
    # print the matching words
    print(matchingWords)

def questions():
    # ask the user for the letters that are not allowed
    banned_letters = input('Enter the letters that are not allowed: ')
    # ask the user for the letters that must be in the word
    contains_letters = input('Enter the letters that must be in the word: ')
    # ask the user for the partial word
    partialWord = input('Enter the partial word: ')
    # call the main function
    main(banned_letters, partialWord, contains_letters)

if __name__ == '__main__':
    #check if argv is passed
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        questions()
        