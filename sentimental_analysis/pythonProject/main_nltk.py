import string
from collections import Counter

import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer

text = open("read.txt", encoding = 'utf-8').read()
lower_case = text.lower()
cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))

tokenised_word = word_tokenize(cleaned_text, "english")

# removing the stop words
final_words = []
for word in tokenised_word:
    if word not in stopwords.words('english'):
        final_words.append(word)
#
# print(final_words)
lemma_words = []
for word in final_words:
    # print(word)
    # continue
    word = WordNetLemmatizer.lemmatize(word)
    lemma_words.append(word)

# emotion_list = []
# with open('sentiment.txt', 'r') as file:
#     for line in file:
#         clean_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
#         word, emotion = clean_line.split()
#
#         if word in lemma_words:
#             emotion_list.append(emotion)
# print(emotion_list)
# w = Counter(emotion_list)
# print(w)
#
# def sentiment_analyse(sentiment_text):
#     score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
#     print(score)
#
# sentiment_analyse(cleaned_text)
# fig, ax = plt.subplots()
# ax.bar(w.keys(), w.values())
# fig.autofmt_xdate()
# plt.savefig('graph.png')
# plt.show()