import pytest
import wordle


def test_get_all_words():
	assert len(wordle.ALL_5_LETTER_WORDS) == 12653


def test_choose_word():
	assert wordle.choose_word(wordle.ALL_5_LETTER_WORDS) in wordle.get_all_words()


def test_choose_random_word():
	assert wordle.choose_random_word(wordle.ALL_5_LETTER_WORDS) in wordle.get_all_words()


#def test_optimized_choose_word(words, banned_letters, partial_word, contains_letters):
#	assert wordle.choose_optimized_word() in wordle.get_all_words()


#def choose_word_with_least_letters(words, banned_letters, partial_word, contains_letters):
#	assert wordle.choose_word_with_least_letters() in wordle.get_all_words()

'''
def average_solve_iterations(total_runs = 10):
    total_iterations = 0
    for run_number in range(total_runs):
        words = get_possible_words()
        _, its = solve(choose_word_func = optimized_choose_word, secret_word = choose_random_word(words))
        total_iterations += its
        print(f'Finished run {run_number+1} / {total_runs}')
        print(f'Iterations: {its}')
    print(f'Average iterations: {total_iterations / total_runs}')


'''



def test_get_possible_words():
	def sub_test(words, bl, pw, cl, expected_words):
		assert sorted(wordle.get_possible_words(words, bl, pw, cl)) == sorted(expected_words)
	sub_test(wordle.ALL_5_LETTER_WORDS, set(), '_____', set(), wordle.ALL_5_LETTER_WORDS) # big example, should equal all words
	sub_test(wordle.ALL_5_LETTER_WORDS, set('eat'), 'fo_g_', set(), ['foggy', 'forgo']) # some of each
	sub_test(wordle.ALL_5_LETTER_WORDS, set('eario'), 'b___t', set(), ['blunt', 'bundt', 'butut']) # lots of banned_letters
	sub_test(wordle.ALL_5_LETTER_WORDS, set(), 'fa_ts', set(), ['facts', 'farts', 'fasts', 'fauts']) # lots of partial word
	sub_test(wordle.ALL_5_LETTER_WORDS, set(), '_____', set('ekdif'), ['fiked']) # lots of contains_letters
	sub_test(
		['peaze', 'pedal', 'pelma', 'pelta', 'pepla', 'petal'],
		set('cvmgysrn'), 'pel_a', set('elap'),
		['pelta']
	)
	sub_test(
		['palea', 'palet', 'patte', 'peaze', 'pelma', 'pelta', 'pepla', 'petal', 'plate', 'pleat', 'potae'],
		set('rgyshiunmkbcd'), 'pel_a', set('pael'),
		['pelta']
	)



def test_test_word():
	def sub_test_word(test_word, secret_word, expected_banned_letters, expected_new_partial_word, expected_contains_letters):
		bl, npw, cl = wordle.test_word(test_word, secret_word)
		assert sorted(list(bl)) == sorted(list(expected_banned_letters))
		assert npw == expected_new_partial_word
		assert sorted(set(cl)) == sorted(list(expected_contains_letters))

	sub_test_word('germs', 'tiger', {'m', 's'}, '_____', {'g', 'e', 'r'}) # no hits
	sub_test_word('audio', 'audit', {'o'}, 'audi_', {'a', 'u', 'd', 'i'}) # some hits
	sub_test_word('audio', 'audio', {}, 'audio', {'a', 'u', 'd', 'i', 'o'}) # correct guess
	sub_test_word('eagle', 'aglee', {}, '____e', {'e', 'a', 'g', 'l'}) # no banned letters
	sub_test_word('germs', 'attap', {'g', 'e', 'r', 'm', 's'}, '_____', {}) # no correct letters



def test_join_partial_words():
	assert wordle.join_partial_words('_____', '_____') == '_____'
	assert wordle.join_partial_words('abc__', '_____') == 'abc__'
	assert wordle.join_partial_words('_____', '_abc_') == '_abc_'
	assert wordle.join_partial_words('a_c__', '_b_d_') == 'abcd_'
	assert wordle.join_partial_words('a_c_e', '_b_d_') == 'abcde'
	with pytest.raises(Exception) as exc_info:
		assert wordle.join_partial_words('a____', 'b____') == '_____'
	exception_raised = exc_info.value
	assert exception_raised.args[0] == 'Invalid partial words'


def test_solve():
	def test_choose_word_function(choose_word_func):
		solution, _ = wordle.solve(choose_word_func = wordle.choose_word, secret_word = 'tiger')
		assert solution == 'tiger'
		solution, _ = wordle.solve(choose_word_func=choose_word_func, secret_word='texts')
		assert solution == 'texts'
		solution, _ = wordle.solve(choose_word_func=choose_word_func, secret_word='farms')
		assert solution == 'farms'
		solution, _ = wordle.solve(choose_word_func=choose_word_func, secret_word='pelta')
		assert solution == 'pelta'
		solution, _ = wordle.solve(choose_word_func=choose_word_func, secret_word='abaya')
		assert solution == 'abaya'
	test_choose_word_function(wordle.choose_random_word)
