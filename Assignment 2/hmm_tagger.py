import os
import re
import random
import math
import sys
import numpy as np

#takes the test file name
test_file = sys.argv[1]
#takes the output file from tast 1
output_file = sys.argv[2]

#before tagging, from the output file, we re-create the same dictionaries as we did in the 1st task.
dic_word_tag = {}
dic_tag_previous = {}
dic_tag = {}


#start reading output file to fill in the dictionaries
with open(output_file) as f:
    content = f.readlines()


for text in content:
	sentence = text.split(' ')
	if sentence[0] == '1': #means im reading dic_tag
		dic_tag[sentence[1]] = float(sentence[2])

	elif sentence[0] == '2': #means im reading dic_tag_previous
		dic_tag_previous[(sentence[1], sentence[2])] = float(sentence[3])

	else:	#means im reading dic_word_tag
		dic_word_tag[(sentence[1], sentence[2])] = float(sentence[3])


#now we start reading test file to assign tags for each token
with open(test_file) as f:
    content2 = f.readlines()

#list of sentences keeps each sentences in the test file
list_of_sentence = []
#sentence is to keep each token in the same sentence orderly
sentence = []
#b is only for checking if im at the last line in the document.
b = 0

for text in content2:
	b=b+1
	line = text.split('\t')
	if len(line) > 2 and b < len(content2): #if the line is not '\n' and we are not at the last line in the test file
		if line[1] != '_':
			sentence.append(line[1].lower()) 
	elif b == len(content2):	#if we are at the last line in the test file
		list_of_sentence.append(sentence)
		sentence = []
	else:						#if we are at the line between 2 sentences, '\n'
		list_of_sentence.append(sentence)
		sentence = []


#we should remove 'END' tag since we do not use it, and
#add 'START' tag at the beginning
tags = list(dic_tag.keys())
tags.remove('START')
tags.remove('END')
tags.insert(0, 'START') 


#we keep the vocabulary as a set
def vocabulary():
	list1 = dic_word_tag.keys()
	list2 = []
	for keys in list1:
		list2.append(keys[0])

	return set(list2)

vocab = vocabulary()


#this function returns the path, it is actually the serial tags assigned to each token in one sentences.
#backpointer is the matrix created while viterbi algorithm running
#N is the number of tags, L is the number of tokens in the current sentence.
def taglist(backpointer, N, L):
	path = []
	current_tag = backpointer[N][L-1]
	current_tag = current_tag.decode("utf-8")

	index = tags.index(current_tag)
	path.append(current_tag)

	for i in range(1, L):
		current_tag = backpointer[index][L-i]
		current_tag = current_tag.decode("utf-8")
		index = tags.index(current_tag)
		path.append(current_tag)

	return path


path_list = [] #this is a list of all paths for all sentences in the given test file. 
			   #the paths are in the same order with the list_of_sentences.




def viterbi(sentence_):
	N = len(tags)
	L = len(sentence_)

	viterbi = np.zeros((N+1, L))
	backpointer = np.chararray((N+1,L),itemsize=10)
	backpointer[:] = ''

	#INITIALIZATION
	for i in range(1, N):
		current_tag = tags[i]
		if (current_tag, 'START') in dic_tag_previous:
			if (sentence_[0], current_tag) in dic_word_tag:
				num = (dic_tag_previous[(current_tag, 'START')]/dic_tag['START'])*(dic_word_tag[(sentence_[0], current_tag)]/dic_tag[current_tag])
				viterbi[i][0] = num
		else:
			viterbi[i][0] = 0.00001 #if the first word is not in the training set, then its likelihood is pretty small.


	backpointer[i][0] = ''

	for i in range(1,L):
		for j in range(1, N):
			max_prob = 0
			max_tag = ''
			max_tag_prob = 0

			for k in range(1, N):
				current_tag = tags[j]
				previous_tag = tags[k]
				current_word = sentence_[i]
				prob = 0

				if((current_word, current_tag) in dic_word_tag.keys()) and ((current_tag, previous_tag) in dic_tag_previous.keys()):

					prob = viterbi[k][i-1]*(dic_tag_previous[(current_tag, previous_tag)]/dic_tag[previous_tag])*(dic_word_tag[(current_word, current_tag)]/dic_tag[current_tag])

		
					tag_prob = viterbi[k][i-1]*(dic_tag_previous[(current_tag, previous_tag)]/dic_tag[previous_tag])*(dic_word_tag[(current_word, current_tag)]/dic_tag[current_tag])

				elif (current_tag, previous_tag) in dic_tag_previous.keys():
					 #if the current word is not in vocab
					 prob = viterbi[k][i-1]*(dic_tag_previous[(current_tag, previous_tag)]/dic_tag[previous_tag])
					 tag_prob = viterbi[k][i-1]*(dic_tag_previous[(current_tag, previous_tag)]/dic_tag[previous_tag])
				else:
					prob = 0
					tag_prob = 0

				if max_prob < prob:
					max_prob = prob
				if max_tag_prob < tag_prob:
					max_tag_prob = tag_prob
					max_tag = previous_tag

			viterbi[j][i] = max_prob
			backpointer[j][i] = max_tag

		max_prob = 0
		max_tag = ''

	for i in range(1, N):
		#print(len(tags), i)

		current_tag = tags[i]
		if ('END', current_tag) in dic_tag_previous.keys():
			prob = viterbi[i][L-1]*(dic_tag_previous[('END', current_tag)]/dic_tag['END'])
		else:
			prob = 0
		if max_prob < prob:
			max_prob = prob
			max_tag = current_tag
	
	viterbi[N][L-1] = max_prob
	backpointer[N][L-1] = max_tag

#path is actually the tag list in order for the current sentence.
	path = taglist(backpointer,N,L)
	path_list.append(path)



#for each sentence in the list, we call viterbi to find its serial of tag.
for sentence_ in list_of_sentence:
	viterbi(sentence_)



#this is to create output2.txt file
#it writes the paths in path_list into the file, so that we are able to reach the assigned sentences in the evaluation part.
def write_to_output(path_list, list_of_sentence):
	f = open('output2.txt','w')
	number = len(path_list)

	for i in range(0, number):
		sentence = list_of_sentence[i]
		path = path_list[i]
		path.reverse()

		number2 = len(sentence)

		for j in range(0, number2):
			f.write(sentence[j])
			f.write('|')
			f.write(path[j])
			f.write('\n')

		f.write('\n')

write_to_output(path_list, list_of_sentence)

f_2 = open('vocabulary.txt','w')

for word in vocab:
	f_2.write(word)
	f_2.write('\n')

f_2.close()

