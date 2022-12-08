import re
import urllib.request              # know that it's additional module but i want to try to open seq file such way
import matplotlib.pyplot as plt

# I TASK

references = 'https://raw.githubusercontent.com/Serfentum/bf_course/master/15.re/references'
req = urllib.request.Request(references)

with urllib.request.urlopen(req) as ftp_search:
    sequence_data = str(ftp_search.read())                         # save content in str variable

pattern_ftp_search = re.compile(r"ftp\.[/.\w#]+")                  # pattern for all ftp protocols

with open('ftps.txt', 'w') as ftp:
    for line in re.findall(pattern_ftp_search, sequence_data):     # create file and record all findings
        ftp.write(line + '\n')

# TASKS WITH 2430AD file

with open('2430AD.txt', 'r') as regex_search:
    regex_search = regex_search.read().strip()
regex_search = regex_search.replace("\n\n", " ")                   # open another file and delete serve symbols


# II TASK

pattern_number_search = re.compile(r"(?:\d+\.\d+|\d+)")            # pattern for int and float number
print(*re.findall(pattern_number_search, regex_search))

# III TASK

pattern_aA_search = re.compile(r"\w*a\w*", flags=re.IGNORECASE)    # pattern for a/A-contained words
a_searcher = re.findall(pattern_aA_search, regex_search)
print(*a_searcher)

# IV TASK - pattern for exclamatory sentences

pattern_exclamatory_search = re.compile(r'''[A-Z]                  # start from capital letter - start of sentence
                                            [^.?;]+!               # later any symbols escape final untill !
                                         ''', re.VERBOSE)
exclamatory_searcher = re.findall(pattern_exclamatory_search, regex_search)
print(*exclamatory_searcher)

# V TASK - unique words

dictionary_counter = {}
pattern_word_search = re.compile(r'''\w+\.\w+\.?                   # find strange patterns (A.D., float, initials)
                                     |[A-Za-z\d']+                 # find standard words and numbers
                                  ''', re.IGNORECASE | re.VERBOSE)
word_searcher = re.findall(pattern_word_search, regex_search)

# note: - doesn't use in pattern because text contains n- and m- dash, but they don't distinguish

# count amount of every word
for word in word_searcher:
    if word.lower() in dictionary_counter:
        dictionary_counter[word.lower()] += 1
    else:
        dictionary_counter[word.lower()] = 1

# separate unique and divide by length
len_spread = {}
for key, value in dictionary_counter.items():
    if value == 1 and len(str(key)) in len_spread:
        len_spread[len(str(key))] += 1
    elif value == 1 and len(str(key)) not in len_spread:
        len_spread[len(str(key))] = 1

# sort by length and calculate fraction
words_fraction, letter_number = [], []
for key, value in sorted(len_spread.items()):
    letter_number += [key]
    words_fraction += [value / sum(len_spread.values())]

# graph
fig = plt.figure(figsize=[8, 5], dpi=700)

plt.bar(letter_number, words_fraction, color='turquoise')

plt.xlabel('Unique word length', size=16, fontstyle='italic')
plt.ylabel('Fraction', size=16, fontstyle='italic')
plt.title('Spread of unique words in text by their length', size=18, fontstyle='italic')

plt.savefig('Length_spread_plot.png')

# VI - brick language: find voice sounds and insert instead v_k_v

# English brick language


def brick_language(string):
    return re.sub(r"([aeiouy])", r"\1k\1", string, flags=re.IGNORECASE)

# Russian brick language


def brick_language_russian(string):
    return re.sub(r"([уеоаыиюёэя])", r"\1к\1", string, flags=re.IGNORECASE)


# VII - word counter

pattern_sentence_search = re.compile(r'''[\"\'\w ,:;()-]           # every symbols insite sentence
                                         +[.!?]                    # untill finall symbol
                                      ''', re.VERBOSE)
pattern_word_search = re.compile(r'''\w+\.\w+\.?|                  # search all words like previously
                                     [A-Za-z\d']+
                                  ''', re.VERBOSE | re.IGNORECASE)


def find_n_words_sentences(text, words_amount):
    answer = []
    sentence_searcher = re.findall(pattern_sentence_search, text)          # find sentences
    for sentence in sentence_searcher:
        new_word_searcher = re.findall(pattern_word_search, sentence)      # for every sentence find words
        if len(new_word_searcher) == words_amount:                         # count number of words
            answer += map(tuple, [new_word_searcher])                      # list of tuple
    return answer
