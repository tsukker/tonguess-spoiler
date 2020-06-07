import itertools
import os
import pickle
import random
import string
import sys
import time

cache = dict()


def call(s):
    print(s, flush=True)
    ans = input()
    ans_tup = tuple(map(int, [c for c in ans if c in string.digits]))
    print(f'answer: {ans_tup}')
    return ans_tup


def calc_match(called, ans):
    assert len(called) == len(ans)
    get_cnt = 0
    touch_cnt = 0
    for c1, c2 in zip(called, ans):
        if c1 == c2:
            get_cnt += 1
        elif c1 in ans:
            touch_cnt += 1
    return (get_cnt, touch_cnt)


def groups_of_word(mode, candidates, word):
    ret = dict()
    for cand in candidates:
        key = calc_match(word, cand)
        if key not in ret:
            ret[key] = []
        ret[key].append(cand)
    return ret


def calc_score(mode, candidates, word):
    if word[1:] == 'ABC':
        print(f'calc_score {word}', file=sys.stderr)
    gs = groups_of_word(mode, candidates, word)
    sizes = [len(val) for val in gs.values()]
    sizes = sorted(sizes, reverse=True)
    return (sizes, word)


def select_for_best(results):
    best = min(results)
    sizes, word = best
    if word[0] == '!':
        word = word[1:]
    return (sizes, word)


def search_all_words(mode, candidates):
    global cache
    fs_cand = frozenset(candidates)
    if fs_cand in cache:
        print('cache hit !!')
        return cache[fs_cand]
    l = 1
    for i in range(mode):
        l *= (26 - i)
    results = [None] * l
    for i, word in enumerate(
            map(lambda tup: ''.join(tup),
                itertools.permutations(string.ascii_uppercase, mode))):
        results[i] = calc_score(mode, candidates, word)
        if word in fs_cand:
            tmp, _ = results[i]
            results[i] = (tmp, f'!{word}')
    ret = sorted(results)[:100]
    if 40 < len(candidates):
        cache[fs_cand] = ret
    return ret


def turn(mode, candidates, word=None):
    best_word = ""
    best_score = len(candidates)
    print(f'number of candidates: {len(candidates)}')
    if len(candidates) < 10:
        print('candidates: ', end='')
        print(candidates)
    if len(candidates) in [1, 2]:
        best_word = candidates[0]
        best_score = calc_score(mode, candidates, best_word)
    elif word is not None:
        best_word = word
        best_score = calc_score(mode, candidates, best_word)
    else:
        results = search_all_words(mode, candidates)
        best_score, best_word = select_for_best(results)
    print(f'word: {best_word}, score: {best_score}', file=sys.stderr)
    best_groups = groups_of_word(mode, candidates, best_word)
    key = call(best_word)
    next_candidates = None
    while True:
        try:
            next_candidates = best_groups[key]
            break
        except:
            print('Got unexpected answer. Finish? y/n: ', end='', flush=True)
            line = input()
            if line == 'y':
                dump_cache(mode)
                sys.exit()
            else:
                key = call(best_word)
    if key == (4, 0):
        next_candidates = []
    return next_candidates


def read_words(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    words = [line[:-1] if line[-1] == '\n' else line for line in lines]
    return words


def generate_answer_word(mode, all_words):
    ng_words = read_words(f'ng_word_{mode}.txt')
    candidates = list(set(all_words) - set(ng_words))
    answer_word = random.choice(candidates)
    return answer_word


def load_cache(mode):
    global cache
    filepath = f'cache_{mode}.pickle'
    if not os.path.isfile(filepath):
        cache = dict()
        return
    with open(filepath, 'rb') as f:
        cache = pickle.load(f)
    return


def dump_cache(mode):
    global cache
    filepath = f'cache_{mode}.pickle'
    with open(filepath, 'wb') as f:
        pickle.dump(cache, f)


if __name__ == '__main__':
    argc = len(sys.argv)
    mode = 4
    if argc >= 2:
        if sys.argv[1] == '3':
            mode = 3
    load_cache(mode)
    all_words_34 = read_words('dictionary.txt')
    all_words = [word for word in all_words_34 if len(word) == mode]
    print(generate_answer_word(mode, all_words), flush=True)
    candidates = all_words
    first_word = None
    try:
        first_word = random.choice(read_words(f'first_word_{mode}.txt'))
    except:
        pass
    candidates = turn(mode, candidates, first_word)
    while (len(candidates) > 0):
        candidates = turn(mode, candidates)
    dump_cache(mode)
    print('finish')
