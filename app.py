import snowballstemmer
import numpy as np

import re 
from collections import Counter
from itertools import groupby

class Text_sum:
    
    def __init__(self, filename, lang, sent_len):
        self.filename = filename
        self.lang = lang
        self.sent_len = sent_len
        
    def load_file(self):
        """Load file as a list of sentences."""
        self.text = list(set(open(self.filename).read().splitlines()))
        self.remove_punctuation()

    def remove_punctuation(self):
        """Remove punctuation from text."""
        text_without_punctuation = [re.sub(r'[^\w\s]','',i) for i in self.text]
        self.stemming(text_without_punctuation)

    def stemming(self, text_without_punctuation):
        """Stemming text"""
        
        if self.lang == 2:
            stemmer = snowballstemmer.RussianStemmer()
        else:
            stemmer = snowballstemmer.EnglishStemmer()
        
        self.stemmed_text = []
        for sentence in text_without_punctuation:
            self.stemmed_text.append(" ".join([stemmer.stemWord(i) for i in sentence.split()]))
        self.remove_stop_words()

    def remove_stop_words(self):
        """Turn list of sentences to list of words
        and remove stop words.
        """
        words_list = []

        for i in self.stemmed_text:
            words_list.extend(i.split())

        if self.lang == 2:
            stop_words = set(open('stop_words/russian.txt').read().splitlines()) 
        else:
            stop_words = set(open('stop_words/english.txt').read().splitlines()) 
            
        words_list = [i for i in words_list if not i in stop_words]

        self.count_words(words_list)
        
    def count_words(self, words_list):
        """Calculate the frequency of use of a word in the text."""
        counts = dict(Counter(words_list))
        self.calculate_words_weights(counts)

    def calculate_words_weights(self, counts):
        """Calculate weight of each word in normalized text."""
        len_of_dict = len(counts)

        for key, value in counts.items():
            counts[key] = round(value / len_of_dict,3)
        
        self.word_to_weight(counts)
    
    def word_to_weight(self, counts):
        """Create new list from stemmed_text list by replacing words with their weights."""
        int_list = []

        for i in self.stemmed_text:
            for j in i.split():
                try:
                    int_list.append(counts[j])
                except:
                    int_list.append(0)
            else:
                int_list.append('-')

        a_ = groupby(int_list, lambda x: x == '-')
        int_list = [list(group) for k, group in a_ if not k]
        
        self.calculate_sentences_weights(int_list)

    def calculate_sentences_weights(self, int_list):
        """Create new list with the sum of words weights within every sentence"""
        sentence_weights = []
        for i in int_list:
            sentence_weights.append(sum(i))
        
        self.get_index(sentence_weights)
            
    def get_index(self, sentence_weights):
        """Get indexes of sentences with the biggest weight"""
        arr = np.array(sentence_weights)
        indexes = arr.argsort()[-self.sent_len:][::-1]
        self.display(indexes)
        
    def display(self, indexes):
        """Display the original text sentences with given indexes"""
        for i in indexes:
            with open('text_sum.txt', 'a') as f:
                f.write(f'{self.text[i]}\n')
            
if __name__ == "__main__":
    lang = int(input('Choose language: 1 for English or 2 for Russian: '))
    sent_len = int(input('How many sentences do you want in summorized text 1 maybe 2 or more?: '))
    filename = input('Write text file name e.x. news.txt: ')
    
    try:
        print('Processing...')
        Text_sum(filename=filename, lang=lang, sent_len=sent_len).load_file()
        print("Text Summary Done Successfully,\nCheck text_sum.txt file")
    except Exception as erorr:
        print(erorr)