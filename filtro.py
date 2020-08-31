import nltk
import re

from nltk.corpus import stopwords
from nltk import word_tokenize
from string import punctuation

#HappyEmoticons
emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])

# Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])

#Emoji patterns
emoji_pattern = re.compile("["
         u"\U0001F600-\U0001F64F"  # emoticons
         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
         u"\U0001F680-\U0001F6FF"  # transport & map symbols
         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
         u"\U00002702-\U000027B0"
         u"\U000024C2-\U0001F251"
         "]+", flags=re.UNICODE)

#combine sad and happy emoticons
emoticons = emoticons_happy.union(emoticons_sad)


# stopword list to use
spanish_stopwords = stopwords.words('spanish')



# punctuation to remove
non_words = list(punctuation)
# we add spanish punctuation
non_words.extend(['¿', '¡'])
non_words.extend(map(str, range(10)))






def tokenize(text):
    # remove links from tweets
    text = re.sub(r"http\S+", "https", text)

    # remove punctuation
    text = ''.join([c for c in text if c not in non_words])
    # remove repeated characters
    text = re.sub(r'(.)\1+', r'\1\1', text)
    # tokenize
    text = emoji_pattern.sub(r'', text)
    tokens = word_tokenize(text)

    filtered_sentence = [w for w in tokens if not w in spanish_stopwords]
    frase=""
    for p in filtered_sentence:
        frase+=p+" "
    
    return frase


def tokenize2(text):
    # remove links from tweets
    text = re.sub(r"http\S+", "https", text)

    # remove punctuation
    text = ''.join([c for c in text if c not in non_words])
    # remove repeated characters
    text = re.sub(r'(.)\1+', r'\1\1', text)
    # tokenize

    tokens = word_tokenize(text)

    filtered_sentence = [w for w in tokens if not w in spanish_stopwords]
    frase=""
    for p in filtered_sentence:
        frase+=p+" "
   
    return frase


def filtrar_conEmojis_YstopWords(text):
    # remove links from tweets
    text = re.sub(r"http\S+", "https", text)

    # remove punctuation
    text = ''.join([c for c in text if c not in non_words])
    # remove repeated characters
    text = re.sub(r'(.)\1+', r'\1\1', text)
    # tokenize


    return text


def filtrar_constopWords(text):
    # remove links from tweets
    text = re.sub(r"http\S+", "https", text)

    # remove punctuation
    text = ''.join([c for c in text if c not in non_words])
    # remove repeated characters
    text = re.sub(r'(.)\1+', r'\1\1', text)
    text = emoji_pattern.sub(r'', text)



    return text

def filtrar_soft(sentences):


    words = tokenize(sentences)


    return words

def filtrar_soft_con_emojis(sentences):


    words = tokenize2(sentences)


    return words









