#!/usr/bin/env python

import itertools

train_spam = ['send us your password', 'review our website', 'send your password', 'send us your account']
train_ham = ['Your activity report','benefits physical activity', 'the importance vows']
test_emails = {'spam':['renew your password', 'renew your vows'], 'ham':['benefits of our account', 'the importance of physical activity']}

spam_words = list(map(lambda x: x.strip(), " ".join(train_spam).split()))
ham_words  = list(map(lambda x: x.strip(), " ".join(train_ham).split()))
all_words = spam_words + ham_words

# We can count how many spam emails have the word “send” and divide that by the total number of spam emails 
for word in spam_words:

print(all_words)
