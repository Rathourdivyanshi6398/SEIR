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


# take two URLs from command line
try:
    url1 = sys.argv[1]
    url2 = sys.argv[2]

    print("Word Count Dictionary for URL 1:\n")
    word_counts1 = fetch_words(url1)
    for word, count in word_counts1.items():
        print(word, ":", count)

    print("Word Count Dictionary for URL 2:\n")
    word_counts2 = fetch_words(url2)
    for word, count in word_counts2.items():
        print(word, ":", count)

except IndexError:
    print("Please provide two URLs.")
except requests.exceptions.RequestException as e:
    print("Error fetching the page:", e)


'''
Currently, I have not been able to complete the remaining sections:
- Generating the Simhash for the document.
- Comparing the Simhash values of two different URLs.
- Calculating how many bits are common between them.

The rest of the implementation is still pending because I am having
difficulty understanding the Simhash algorithm and the bit-level
comparison process.
'''

