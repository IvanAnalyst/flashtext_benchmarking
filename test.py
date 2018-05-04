from flashtext.keyword import KeywordProcessor
import random
import string
import re
import time


def get_word_of_length(str_length):
    # generate a random word of given length
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(str_length))

# generate a list of 100K words of randomly chosen size
all_words = [get_word_of_length(random.choice([3, 4, 5, 6, 7, 8])) for i in range(100000)]

print('Count  | FlashText | Custom1   | Custom2   | Regex    ')
print('------------------------------------------------------')
for keywords_length in range(1, 10002, 1000):
    # chose 5000 terms and create a string to search in.
    all_words_chosen = random.sample(all_words, 5000)
    story = ' '.join(all_words_chosen)

    # get unique keywords from the list of words generated.
    unique_keywords_sublist = list(set(random.sample(all_words, keywords_length)))
    
    # compile regex
    # source: https://stackoverflow.com/questions/6116978/python-replace-multiple-strings
    rep = dict([(key, '_keyword_') for key in unique_keywords_sublist])
    compiled_re = re.compile("|".join([k for k in rep.keys()]))

    # add keywords to flashtext
    keyword_processor = KeywordProcessor()
    for keyword in unique_keywords_sublist:
        keyword_processor.add_keyword(keyword, '_keyword_')

    # time the modules
    start = time.time()
    story1 = keyword_processor.replace_keywords(story)
    end1 = time.time()
    
    story2 = ' '.join(rep.get(word, word) for word in story.split())
    end2 = time.time()
    
    story3 = ' {} '.format(story)
    for k, v in rep.items():
        story3 = story3.replace(' {} '.format(k), ' {} '.format(v))
    end3 = time.time()
    
    story4 = compiled_re.sub(lambda m: rep[m.group(0)], story)
    end4 = time.time()
    
    print(str(story1 == story2), str(story1 == story3.strip()), str(story1 == story4))
    print(str(keywords_length).ljust(6), '|',
          "{0:.5f}".format(end1 - start).ljust(9), '|',
          "{0:.5f}".format(end2 - end1).ljust(9), '|',
          "{0:.5f}".format(end3 - end2).ljust(9), '|',
          "{0:.5f}".format(end4 - end3).ljust(9))
