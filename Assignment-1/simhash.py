import sys
import requests
import re
from bs4 import BeautifulSoup

# hash(s) = sum( s[i] * p^i ) mod m
def word_hash(word):
    p = 53
    m = 2**64
    h = 0

    for i in range(len(word)):
        h = (h + ord(word[i]) * (p ** i)) % m

    return h

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

except Exception as err:

    print("Error:", err)
