import random


def get_all_words():
    file = open('five_characters.txt', 'r')
    words = []
    for line in file:
        words.append(line.strip())
    return words


ALL_5_LETTER_WORDS = get_all_words()


def choose_word(words, banned_letters = set(), partial_word = '_____', contains_letters = set()):
    random_index = random.randrange(len(words))
    return words[random_index]


def choose_random_word(words, banned_letters = set(), partial_word = '_____', contains_letters = set()):
    random_index = random.randrange(len(words))
    return words[random_index]


#TODO finish this
def optimized_choose_word(words = ALL_5_LETTER_WORDS, banned_letters = set(), partial_word = '_____', contains_letters = set()):
    guess_totals = {}
    counter = 0
    for guess in random.sample(words, min(len(words), 20)):
    #for guess in ALL_5_LETTER_WORDS:
        total = 0
        #for possible_secret_word in ALL_5_LETTER_WORDS:
        for possible_secret_word in random.sample(words, min(len(words), 20)):
            #if counter % 1000 == 0:
                #print(guess, possible_secret_word)
            banned_letters, partial_word, contains_letters = test_word(guess, possible_secret_word)
            possible_words = get_possible_words(banned_letters, partial_word, contains_letters)
            total += len(possible_words)
            counter += 1
        guess_totals[guess] = total
        #print(guess_totals)
    result = min(guess_totals, key=guess_totals.get)
    print(f'Our guess will be: {result}')
    return result

#TODO add testing
#TODO optimize this with iterators
#TODO optimize all of our functions (can leave out returning words when we just want length)
#TODO decompose things into functions better


def choose_word_with_least_letters(words, banned_letters, partial_word, contains_letters):
    least_letters = len(words[0])
    for word in words:
        letters_not_in_sets =  set(word) - banned_letters - contains_letters - set(partial_word)
        if len(letters_not_in_sets) < least_letters:
            least_letters = len(letters_not_in_sets)
    
    least_words = []
    for word in words:
        letters_not_in_sets =  set(word) - banned_letters - contains_letters - set(partial_word)
        if len(letters_not_in_sets) == least_letters:
            least_words.append(word)

    #print(least_words)
    return choose_random_word(least_words)


def average_solve_iterations(total_runs = 10):
    total_iterations = 0
    for run_number in range(total_runs):
        words = ALL_5_LETTER_WORDS
        _, its = solve(choose_word_func = optimized_choose_word, secret_word = choose_random_word(words))
        total_iterations += its
        print(f'Finished run {run_number+1} / {total_runs}')
        print(f'Iterations: {its}')
    print(f'Average iterations: {total_iterations / total_runs}')


def solve(choose_word_func = choose_word, secret_word = 'tiger'):
    banned_letters = set()
    partial_word = '_____'
    contains_letters = set()

    iterations = 0

    possible_words = ALL_5_LETTER_WORDS
    while ('_' in partial_word):
        possible_words = get_possible_words(possible_words, banned_letters, partial_word, contains_letters)
        if len(possible_words) == 1:
            return possible_words[0], iterations + 1
        if len(possible_words) == 0:
            print("NO SOLUTIONS")
            return None, iterations + 1
        guess = choose_word_func(possible_words, banned_letters, partial_word, contains_letters)
        new_banned_letters, new_partial_word, new_contains_letters = test_word(guess, secret_word)

        banned_letters = banned_letters.union(new_banned_letters)
        contains_letters = contains_letters.union(new_contains_letters)
        partial_word = join_partial_words(partial_word, new_partial_word)

        iterations += 1

        print(f'Iteration {iterations}, possible words: {len(possible_words)}, guess: {guess}, partial word: {partial_word}')
        print(f'Banned letters: {banned_letters}, contains letters: {contains_letters}')
        if len(possible_words) < 50:
            print(possible_words)

    return partial_word, iterations


def get_possible_words(words = ALL_5_LETTER_WORDS, banned_letters = set(), partial_word = '_____', contains_letters = set()):
    if len(partial_word) != 5:
        print('partial_word must be 5 characters long')
        return
    
    forbidden_letters = set(banned_letters)
    matching_words = []
    for word in words:
        if set(word).isdisjoint(forbidden_letters) and contains_letters.issubset(set(word)):
            match = True
            for i in range(len(partial_word)):
                if partial_word[i] != '_':
                    if partial_word[i] != word[i]:
                        match = False
                        break
            if match:
                matching_words.append(word)
    return matching_words



def test_word(word, secret_word):
    new_partial_word = ''
    banned_letters = set(word) - set(secret_word)
    contains_letters = set(word).intersection(set(secret_word))
    for i in range(len(word)):
        if word[i] == secret_word[i]:
            new_partial_word += word[i]
        else:
            new_partial_word += '_'
    return banned_letters, new_partial_word, contains_letters


def join_partial_words(p_word1, p_word2):
    print(p_word1, p_word2)
    result = ''
    for l1, l2 in zip(p_word1, p_word2):
        if l1 == '_' and l2 == '_':
            result += '_'
        elif l1 == '_' and l2 != '_':
            result += l2
        elif l1 != '_' and l2 == '_':
            result += l1
        elif l1 == l2:
            result += l1
        else:
            print(f'ERROR: both partial words cannot have different letters {p_word1} - {p_word2}')
            raise Exception('Invalid partial words')
    return result


if __name__ == '__main__':
    average_solve_iterations()
        