import itertools
import random
import string
import sys
import time


def call(s):
    print(s, flush=True)
    ans = tuple(map(int, input().split(' ')))
    return ans


def groups(mode, candidates, word):
    ret = dict()
    for cand in candidates:
        get_cnt = 0
        touch_cnt = 0
        for i in range(mode):
            if word[i] == cand[i]:
                get_cnt += 1
            elif word[i] in cand:
                touch_cnt += 1
        key = (get_cnt, touch_cnt)
        if key not in ret:
            ret[key] = []
        ret[key].append(cand)
    return ret


def calc_score(mode, candidates, word):
    if word[1:] == 'ABC':
        print(f'calc_score {word}', file=sys.stderr)
    gs = groups(mode, candidates, word)
    sizes = [len(val) for val in gs.values()]
    return (max(sizes), word)


def turn(mode, candidates, word=None):
    best_word = ""
    best_score = len(candidates)
    if len(candidates) < 10:
        print('candidates: ', end='')
        print(candidates)
    if len(candidates) == 1:
        best_word = candidates[0]
        best_score = calc_score(mode, candidates, best_word)
    elif word is not None:
        best_word = word
        best_score = calc_score(mode, candidates, best_word)
    else:
        l = 1
        for i in range(mode):
            l *= (26 - i)
        results = [None] * l
        for i, word in enumerate(
                map(lambda tup: ''.join(tup),
                    itertools.permutations(string.ascii_uppercase, mode))):
            results[i] = calc_score(mode, candidates, word)
        best_score, best_word = min(results)
    print(f'word: {best_word}, score: {best_score}', file=sys.stderr)
    best_groups = groups(mode, candidates, best_word)
    key = call(best_word)
    next_candidates = best_groups[key]
    if key == (4, 0):
        next_candidates = []
    return next_candidates


if __name__ == '__main__':
    with open('dictionary.txt', 'r') as f:
        lines = f.readlines()
    lines = [line[:-1] if line[-1] == '\n' else line for line in lines]
    argc = len(sys.argv)
    mode = 4
    if argc >= 2:
        if sys.argv[1] == '3':
            mode = 3
    candidates = [line for line in lines if len(line) == mode]
    first_word = {4: 'DARE'}[mode]
    print(random.choice(candidates), flush=True)
    candidates = turn(mode, candidates, first_word)
    while (len(candidates) > 0):
        candidates = turn(mode, candidates)
    print('finish')
