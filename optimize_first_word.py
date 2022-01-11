import wordle
import json
import time
import random
import numpy as np


def find_optimal_first_words():
    guess_totals = {}
    counter = 0

    with open('first_guess_rankings.json', 'r') as file:
        data = json.load(file)
    
    for guess in wordle.ALL_5_LETTER_WORDS:
        if guess in data['words'].keys():
            continue
        max_remaining = 0
        max_word = ''
        min_remaining = float('inf')
        min_word = ''
        amounts = []
        start = time.time()
        #for possible_secret_word in ALL_5_LETTER_WORDS:
        for possible_secret_word in random.sample(wordle.ALL_5_LETTER_WORDS, 1265):
            if counter % 1000 == 0:
                print(f'After {counter} iterations we are on {guess}-{possible_secret_word}')
            banned_letters, partial_word, contains_letters = wordle.test_word(guess, possible_secret_word)
            possible_words = wordle.get_possible_words(wordle.ALL_5_LETTER_WORDS, banned_letters, partial_word, contains_letters)

            length = len(possible_words)
            amounts.append(length)
            if length < min_remaining:
                min_remaining = length
                min_word = possible_secret_word
            if length > max_remaining:
                max_remaining = length
                max_word = possible_secret_word
            counter += 1
        
        amounts = np.array(amounts)
        data['words'][guess] = {
            'mean': float(np.mean(amounts)),
            'median': int(np.median(amounts)),
            'total': int(np.sum(amounts)),
            'num_checked': amounts.size,
            'min': min_remaining,
            'min_word': min_word,
            'max': max_remaining,
            'max_word': max_word,
            'std': float(np.std(amounts))
        }

        data['total_run_time'] += time.time() - start

        json_object = json.dumps(data, indent = 4)
        with open('first_guess_rankings.json', 'w') as outfile:
            outfile.write(json_object)
        
    result = min(guess_totals, key=guess_totals.get)
    print(f'Our guess will be: {result}')
    return result

if __name__ == '__main__':
    find_optimal_first_words()