import random


def get_all_words():
    file = open('five_characters.txt', 'r')
    words = []
    for line in file:
        words.append(line.strip())
    return words


ALL_5_LETTER_WORDS = get_all_words()


def choose_word(words, banned_letters, partial_word, contains_letters):
    random_index = random.randrange(len(words))
    return words[random_index]


def average_solve_iterations(total_runs = 10):
    total_iterations = 0
    for _ in range(total_runs):
        words = get_possible_words()
        _, its = solve(secret_word = choose_random_word(words))
        total_iterations += its
    print(f'Average iterations: {total_iterations / total_runs}')


def solve(choose_word_func = choose_word, secret_word = 'tiger'):
    banned_letters = set()
    partial_word = '_____'
    contains_letters = set()

    iterations = 0

    while ('_' in partial_word):
        possible_words = get_possible_words(banned_letters, partial_word, contains_letters)
        possible_word = choose_word_func(possible_words, banned_letters, partial_word, contains_letters)
        new_banned_letters, new_partial_word, new_contains_letters = test_word(possible_word, secret_word)

        banned_letters = banned_letters.union(new_banned_letters)
        contains_letters = contains_letters.union(new_contains_letters)
        partial_word = join_partial_words(partial_word, new_partial_word)

        iterations += 1

    return partial_word, iterations


def get_possible_words(banned_letters = '', partial_word = '_____', contains_letters = ''):
    if len(partial_word) != 5:
        print('partialWord must be 5 characters long')
        return
    words = ALL_5_LETTER_WORDS
    
    forbidden_letters = set(banned_letters)
    matching_words = []
    for word in words:
        if set(word).isdisjoint(forbidden_letters) and set(contains_letters).issubset(set(word)):
            match = True
            for i in range(len(partial_word)):
                if partial_word[i] != '_':
                    if partial_word[i] != word[i]:
                        match = False
                        break
            if match:
                matching_words.append(word)
    return matching_words


def choose_random_word(words):
    random_index = random.randrange(len(words))
    return words[random_index]


def test_word(word, secret_word):
    new_partial_word = ''
    banned_letters = set(word) - set(secret_word)
    contains_letters = set(word).intersection(secret_word)
    for i in range(len(word)):
        if word[i] == secret_word[i]:
            new_partial_word += word[i]
        else:
            new_partial_word += '_'
    return banned_letters, new_partial_word, contains_letters


def join_partial_words(p_word1, p_word2):
    result = ''
    for l1, l2 in zip(p_word1, p_word2):
        if l1 == '_' and l2 == '_':
            result += '_'
        elif l1 == '_':
            result += l2
        else:
            result += l1
    return result


if __name__ == '__main__':
    average_solve_iterations()
        