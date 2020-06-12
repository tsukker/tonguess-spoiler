import os
import pickle


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


def read_words(filepath):
    if not os.path.isfile(filepath):
        return []
    with open(filepath, 'r') as f:
        lines = f.readlines()
    words = [
        line[:-1] if line[-1] == '\n' else line for line in lines
        if len(line) > 0 and line[0] != '#'
    ]
    return words


def write_words(filepath, words):
    with open(filepath, 'w') as f:
        f.write('\n'.join(words) + '\n')


def load_cache(filepath):
    if not os.path.isfile(filepath):
        return dict()
    with open(filepath, 'rb') as f:
        cache = pickle.load(f)
    return cache


def dump_cache(filepath, cache):
    with open(filepath, 'wb') as f:
        pickle.dump(cache, f)


if __name__ == '__main__':
    pass
