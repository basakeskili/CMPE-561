import os
import re
import random
import math
import sys
import numpy as np


#in this part, i read 5 different file to reach the previous data.
#vocabulary.txt stores the all words that have been seen before.
vocab = []
with open('vocabulary.txt') as vocab_file:
	vocab_list = vocab_file.readlines()

for word in vocab_list:
	vocab.append(word[:-1])

#to learn which post we are looking at, read post_cpost.txt file
with open('post_cpost.txt') as post_file:
	post_cpost = post_file.readlines()

if post_cpost == 'cpost' :
	num = 3
else :
	num = 4

#to recreate tagList, read tagList.txt file
with open('tagList.txt') as tag_file:
	lines = tag_file.readlines()

tagList = []
for tag in lines:
	tagList.append(tag[:-1])

#the file names for test and validation.
#test_output is the file that we've created in the training part.
#validation file is to compare our result and true ones.
test_output = sys.argv[1]
validation_file = sys.argv[2]

#test_tagList and valid_tagList keep the list of all tag-paths for all sentences in the same order.

test_tagList = []
valid_tagList = []

with open(test_output) as f:
	content_test = f.readlines()
with open(validation_file) as f2:
	content_validation = f2.readlines()

test_tag = []


for line in content_test:
	if line != '\n':
		word_tag = line.split('|')
		tag = word_tag[1]
		test_tag.append(tag[:-1])

	else:
		test_tagList.append(test_tag)
		test_tag = []


valid_tag = []
i = 0

for line2 in content_validation:
	i = i + 1

	text = line2.split('\t')

	if (len(text) > 2)  and (i < len(content_validation)):
		current_tag = text[3]

		current_word = text[1].lower()

		if current_word != '_' :
			valid_tag.append(current_tag)
	else:
		valid_tagList.append(valid_tag)
		valid_tag = []


N = len(tagList)
confusion_matrix = np.zeros((N,N))

length_ = len(valid_tagList)

tagList.remove('START')
tagList.remove('END')

true = 0
false = 0


for i in range (0, length_):
	get_len = len(valid_tagList[i])

	for j in range(0, get_len):
		get_tag_test = valid_tagList[i][j]
		get_tag_valid = test_tagList[i][j]

		index_test = tagList.index(get_tag_test)
		index_valid = tagList.index(get_tag_valid)

		confusion_matrix[index_valid][index_test] = confusion_matrix[index_valid][index_test]+1
		if(index_valid==index_test):
			true = true+1
		else:
			false+=1



print('Accuracy: ')
print(true/(true+false))

