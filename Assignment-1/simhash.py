import sys
import requests
import re
from bs4 import BeautifulSoup


# create 64-bit hash of a word
def make_word_code(w):
    mul = 53
    limit = 2**64
    code = 0
    step = 1

    for ch in w:
        code = (code + ord(ch) * step) % limit
        step = (step * mul) % limit

    return code


# get text and count words
def fetch_words(link):
    head = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(link, headers=head)

    data = BeautifulSoup(res.text, "html.parser")

    if data.body is None:
        return {}

    content = data.body.get_text().lower()
    word_list = re.findall(r"[a-z0-9]+", content)

    count_map = {}
    for item in word_list:
        if item in count_map:
            count_map[item] += 1
        else:
            count_map[item] = 1

    return count_map


# build 64-bit simhash
def build_hash(word_map):
    score = [0] * 64

    for key in word_map:
        freq = word_map[key]
        code = make_word_code(key)

        index = 0
        while index < 64:
            if (code >> index) & 1:
                score[index] += freq
            else:
                score[index] -= freq
            index += 1

    result_hash = 0
    pos = 0
    while pos < 64:
        if score[pos] > 0:
            result_hash |= (1 << pos)
        pos += 1

    return result_hash

# calculate matching bits
def compare_hashes(a, b):
    temp = a ^ b
    diff_count = bin(temp).count("1")
    return 64 - diff_count

if len(sys.argv) != 3:
    print("Usage: python simhash.py <URL1> <URL2>")
    sys.exit()

first = sys.argv[1]
second = sys.argv[2]

try:
    words_first = fetch_words(first)
    words_second = fetch_words(second)

    hash_first = build_hash(words_first)
    hash_second = build_hash(words_second)

    print("\nSimhash 1:", hash_first)
    print("Simhash 2:", hash_second)

    same = compare_hashes(hash_first, hash_second)
    print("\nMatching Bits:", same)

except Exception as err:
    print("Error:", err)